import React, { useState } from 'react';
import axios from 'axios';
import '../App.css'; 
import { useNavigate } from 'react-router-dom';
console.log('API URL:', process.env.REACT_APP_API_URL);

function ImageUpload() {
    const [image, setImage] = useState(null);
    const [previewImage, setPreviewImage] = useState(null);
    const [generatedImage, setGeneratedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); 


    // Handle image selection and preview
    const handleImageChange = (e) => {
        const file = e.target.files[0];
        setImage(file);

        const reader = new FileReader();
        reader.onloadend = () => {
            setPreviewImage(reader.result);
        };
        reader.readAsDataURL(file);
    };

    // Upload image and receive the generated result
    const handleUpload = async () => {
        if (!image) {
            alert("Please select an image first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', image);
        setLoading(true);  // Show loading while uploading

        try {
            const response = await axios.post('http://localhost:5000/pix2pix', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setGeneratedImage(response.data.generated_image);
        } catch (error) {
            console.error('Error uploading the image:', error);
            alert('Failed to upload. Please try again.');
        } finally {
            setLoading(false);  // Stop loading once done
        }
    };

    return (
        <div className="upload-container">
            <h1>Upload Image to See Map</h1>
            <div className="upload-box">
                <input type="file" accept="image/*" onChange={handleImageChange} />
                <button onClick={handleUpload} disabled={loading}>
                    {loading ? 'Uploading...' : 'Upload'}
                </button>

                {/* Back to Home Button */}
                <button onClick={() => navigate('/')} style={{ marginTop: '20px', backgroundColor: '#555' }}>
                Back to Home
                </button>
            </div>
            
            

            <div className="preview-section">
                {previewImage && (
                    <div className="image-preview">
                        <h2>Uploaded Image</h2>
                        <img src={previewImage} alt="Preview" />
                    </div>
                )}

                {generatedImage && (
                    <div className="image-result">
                        <h2>Generated Map</h2>
                        <img src={`data:image/jpeg;base64,${generatedImage}`} alt="Generated Map" />
                    </div>
                )}
            </div>
        </div>
    );
}

export default ImageUpload;
