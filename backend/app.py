from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from keras_preprocessing.image import img_to_array, array_to_img, load_img
import base64
import os
from io import BytesIO
import numpy as np
from model1.wavelet_transform import Wavelet_Transform
from model2.histogram import Hist_sp_contrast
import cv2
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load the Pix2Pix model
model = pickle.load(open("model/gen_model.pkl", "rb"))

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Encode the output image to base64
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


# Decode the uploaded image (RGB or Grayscale)
def decode_image(file, mode='rgb'):
    ext = file.filename.split('.')[-1].lower()

    # JPEG, PNG, TIFF (RGB)
    if ext in ['jpg', 'jpeg', 'png']:
        img = Image.open(file.stream)
        return np.array(img)

    # TIFF Handling for RGB or PAN
    elif ext in ['tif', 'tiff']:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        
        if mode == 'rgb':
            return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # RGB
        elif mode == 'pan':
            return cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)  # Grayscale for PAN
    
    else:
        raise ValueError("Unsupported file format")


# Root route to check API status
@app.route('/', methods=['GET'])
def home():
    return "Flask API is running!"


# --------- Pix2Pix Endpoint (For Satellite to Map) ----------- 
@app.route('/pix2pix', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"})

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        img = load_img(file_path, target_size=(256, 512))
        img_array = img_to_array(img)

        # Extract the satellite part
        sat_img = img_array[:, :256]
        sat_img = (sat_img - 127.5) / 127.5
        sat_img = np.expand_dims(sat_img, axis=0)

        # Generate map image using Pix2Pix model
        gen_img = model.predict(sat_img)
        gen_img = (gen_img + 1) / 2.0  # Rescale to [0, 1]
        gen_img = np.squeeze(gen_img, axis=0)
        gen_img_pil = array_to_img(gen_img)

        buffered = BytesIO()
        gen_img_pil.save(buffered, format="JPEG")
        gen_img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({
            "generated_image": gen_img_base64
        })


# --------- Pan-Sharpening Endpoint -----------
@app.route('/pansharpening', methods=['POST'])
def pansharpening():
    if 'pan' not in request.files or 'rgb' not in request.files:
        return jsonify({"error": "Pan and RGB images required"}), 400

    try:
        # Decode PAN (grayscale) and RGB images
        rgb_img = decode_image(request.files['rgb'], mode='rgb')
        pan_img = decode_image(request.files['pan'], mode='pan')

        # Ensure images match in size
        pan_img = np.array(pan_img)
        rgb_img = cv2.resize(rgb_img, (pan_img.shape[1], pan_img.shape[0]))
        selected_wavelet = request.form.get('wavelet', 'haar')  # Default to 'haar' if not provided
        # Debugging: Log shapes
        print(f"PAN Image: {pan_img.shape}, RGB Image: {rgb_img.shape}")

        # Apply Pan-Sharpening using wavelet transform
        wavelet_transform = Wavelet_Transform(pan_img, rgb_img, selected_wavelet)
        result_img = wavelet_transform.hsi_to_rgb()
        result_img = (result_img * 255).astype(np.uint8)

        return jsonify({"generated_image": encode_image(result_img)})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# --------- Histogram-specification Endpoint -----------
@app.route('/histogram', methods=['POST'])
def histogram_specification():
    if 'input' not in request.files or 'specified' not in request.files:
        return jsonify({"error": "Both input and specified images are required"}), 400

    input_img = decode_image(request.files['input'])
    specified_img = decode_image(request.files['specified'])

    # Ensure both images are grayscale
    input_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    specified_gray = cv2.cvtColor(specified_img, cv2.COLOR_BGR2GRAY)

    # Apply histogram specification
    hist_spec = Hist_sp_contrast(input_gray, specified_gray)
    result_img = hist_spec.op_spec_hist()

    # Encode and return the processed image
    result_img = (result_img * 255).astype(np.uint8)
    return jsonify({"generated_image": encode_image(result_img)})



if __name__ == '__main__':
    app.run(debug=True)
