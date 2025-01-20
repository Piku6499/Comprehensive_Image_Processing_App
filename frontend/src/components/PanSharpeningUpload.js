import React, { useState } from 'react';
import axios from 'axios';
import '../App.css'; 
import { useNavigate } from 'react-router-dom';

function PanSharpeningUpload() {
    const [rgbImage, setRgbImage] = useState(null);
    const [panImage, setPanImage] = useState(null);
    const [wavelet, setWavelet] = useState('haar');  // Default wavelet
    const [rgbPreview, setRgbPreview] = useState(null);
    const [panPreview, setPanPreview] = useState(null);
    const [generatedImage, setGeneratedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); 
    const waveletOptions = {
        "Haar": "haar",
        "Daubechies 1": "db1",
        "Daubechies 2": "db2",
        "Biorthogonal 1.1": "bior1.1",
        "Biorthogonal 2.2": "bior2.2",
        "Biorthogonal 4.4": "bior4.4",
        "Symlet": "sym2"
    };

    // Handle RGB image upload and create preview
    const handleRgbUpload = (e) => {
        const file = e.target.files[0];
        setRgbImage(file);

        const reader = new FileReader();
        reader.onloadend = () => {
            setRgbPreview(reader.result);  // Set preview for display
        };
        if (file) {
            reader.readAsDataURL(file);
        }
    };

    // Handle PAN image upload and create preview
    const handlePanUpload = (e) => {
        const file = e.target.files[0];
        setPanImage(file);

        const reader = new FileReader();
        reader.onloadend = () => {
            setPanPreview(reader.result);  // Set preview for display
        };
        if (file) {
            reader.readAsDataURL(file);
        }
    };

    //Handle Wavelet selection
    const handleWaveletChange = (e) => setWavelet(e.target.value);

    // Upload images to Flask server
    const handleUpload = async () => {
        if (!rgbImage || !panImage) {
            alert("Please upload both RGB and PAN images.");
            return;
        }

        const formData = new FormData();
        formData.append('rgb', rgbImage);
        formData.append('pan', panImage);
        formData.append('wavelet', wavelet);
        setLoading(true);

        try {
            const response = await axios.post(
                'http://localhost:5000/pansharpening',
                formData
            );
            setGeneratedImage(response.data.generated_image);
        } catch (error) {
            console.error('Error uploading images:', error);
            alert('Upload failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h1>Pan-Sharpening Image Generator</h1>

            <div className="upload-box">
                <label>Upload RGB Image (JPG, PNG, TIF)</label>
                <input type="file" accept="image/*" onChange={handleRgbUpload} />

                <label>Upload PAN Image (JPG, PNG, TIF)</label>
                <input type="file" accept="image/*" onChange={handlePanUpload} />
                <label>Select Wavelet</label>
                <select value={wavelet} onChange={handleWaveletChange}>
                    {Object.entries(waveletOptions).map(([name, value]) => (
                        <option key={value} value={value}>
                            {name}
                        </option>
                    ))}
                </select>
                <button onClick={handleUpload} disabled={loading}>
                    {loading ? 'Processing...' : 'Upload'}
                </button>
                {/* Back to Home Button */}
                
                <button onClick={() => navigate('/')} style={{ marginTop: '20px', backgroundColor: '#555' }}>
                Back to Home
                </button>
            </div>

            <div className="result-section">
                {rgbPreview && panPreview && (
                    <div>
                        <h2>Uploaded RGB and PAN Images</h2>
                        <img src={rgbPreview} alt="Uploaded RGB" style={{ width: '400px' }} />
                        <img src={panPreview} alt="Uploaded PAN" style={{ width: '400px' }} />
                    </div>
                )}

                {generatedImage && (
                    <div>
                        <h2>Generated Pan-Sharpened Image</h2>
                        <img src={`data:image/jpeg;base64,${generatedImage}`} alt="Pan-Sharpened Output" style={{ width: '500px' }} />
                    </div>
                )}
            </div> 
        </div>
    );
}

export default PanSharpeningUpload;
