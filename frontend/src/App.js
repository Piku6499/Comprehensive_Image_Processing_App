import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import Pix2PixUpload from './components/Pix2PixUpload';
import PanSharpeningUpload from './components/PanSharpeningUpload';
import HistogramUpload from './components/HistogramUpload';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/pix2pix" element={<Pix2PixUpload />} />
                <Route path="/pansharpening" element={<PanSharpeningUpload />} />
                <Route path="/Histogram" element={<HistogramUpload/>} />
            </Routes>
        </Router>
    );
}

export default App;
