import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Welcome to the Image Processing App</h1>
            <p>Select an image processing method:</p>

            <div className="options">
                <div className="option">
                    <img src="/images/pix2pix.png" alt="Pix2Pix Preview" className="task-preview" />
                    <button onClick={() => navigate('/pix2pix')}>
                        Satellite Image to Map
                    </button>
                </div>

                <div className="option">
                    <img src="/images/pansharpening.png" alt="Pan-Sharpening Preview" className="task-preview" />
                    <button onClick={() => navigate('/pansharpening')}>
                        Pan-Sharpening
                    </button>
                </div>

                <div className="option">
                    <img src="/images/histogram.jpg" alt="Histogram-specification Preview" className="task-preview" />
                    <button onClick={() => navigate('/histogram')}>
                        Image Contrasting
                    </button>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
