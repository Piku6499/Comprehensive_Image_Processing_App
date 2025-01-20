import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function HistogramUpload() {
    const [inputImage, setInputImage] = useState(null);
    const [specifiedImage, setSpecifiedImage] = useState(null);
    const [resultImage, setResultImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); 
    const handleInputUpload = (e) => {
        setInputImage(e.target.files[0]);
    };

    const handleSpecifiedUpload = (e) => {
        setSpecifiedImage(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!inputImage || !specifiedImage) {
            alert("Please upload both images.");
            return;
        }

        const formData = new FormData();
        formData.append('input', inputImage);
        formData.append('specified', specifiedImage);
        setLoading(true);

        try {
            const response = await axios.post(
                'http://localhost:5000/histogram',
                formData
            );
            setResultImage(response.data.generated_image);
        } catch (error) {
            console.error('Error uploading images:', error);
            alert('Upload failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h1>Histogram Specification</h1>
            
            <div className="upload-box">
                <label>Upload Input Image</label>
                <input type="file" accept="image/*" onChange={handleInputUpload} />

                <label>Upload Specified Image</label>
                <input type="file" accept="image/*" onChange={handleSpecifiedUpload} />
            </div>

            <button onClick={handleUpload} disabled={loading}>
                {loading ? 'Processing...' : 'Upload'}
            </button>

            <button onClick={() => navigate('/')} style={{ marginTop: '20px', backgroundColor: '#555' }}>
                Back to Home
            </button>

            <div className="result-section">
                {inputImage && specifiedImage && (
                    <div>
                        <h2>Uploaded Images</h2>
                        <img src={URL.createObjectURL(inputImage)} alt="Input" width="300px" />
                        <img src={URL.createObjectURL(specifiedImage)} alt="Specified" width="300px" />
                    </div>
                )}

                {resultImage && (
                    <div>
                        <h2>Processed Image</h2>
                        <img src={`data:image/jpeg;base64,${resultImage}`} alt="Result" width="500px" />
                    </div>
                )}
            </div>
        </div>
    );
}

export default HistogramUpload;
