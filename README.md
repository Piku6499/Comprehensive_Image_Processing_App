
# Image Processing Web Application

## 🚀 Overview

![1](https://github.com/user-attachments/assets/1e469372-0ebc-46e3-86ea-4bf899a1a8f1)

This web application offers advanced image processing tasks including:
1. **Pix2Pix Image Transformation**
2. **Pan-Sharpening**
3. **Histogram Specification**

It provides a user-friendly interface built with **React** for the frontend and a robust backend powered by **Flask**. Users can securely interact with these features via JWT-based authentication, and data is stored using **MongoDB**.

---

## 🛠 Features
- **Pix2Pix Transformation:** Transform satellite images into maps using AI-based image-to-image translation.
- **Pan-Sharpening:** Enhance spatial resolution of satellite images.
- **Histogram Specification:** Match the histogram of one image to another for contrast enhancement.
- **User Authentication:** Secure login and signup using JWT.
- **Interactive UI:** Responsive React-based interface.
- **Dockerized:** Simplified deployment with Docker.

---

## 📁 Project Structure

![directory](https://github.com/user-attachments/assets/52fff4af-8b7d-4e71-bf40-9bc4b6f2d682)


## 🛠 Prerequisites
- **Node.js** (v16+)
- **Python** (v3.8+)
- **MongoDB** (Local or Atlas)
- **Docker** (Optional for deployment)

---

## 🔧 Installation & Setup

### 1. Clone the Repository
make git clone 
cd image_processing_app

### 2. Setup Backend
cd backend
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
### 3. Setup Frontend

cd frontend
npm install
npm start

## 🌐 Usage
Open the application at http://localhost:3000.
Sign up or log in.
Choose a processing task (Pix2Pix, Pan-Sharpening, Histogram Specification).
Upload images and view the processed results.

## 🐳 Docker Deployment
1. Build and Start Containers
docker-compose build
docker-compose up
2. Access Application
Frontend: http://localhost:3000
Backend API: http://localhost:5000

## 📂 API Endpoints
Authentication
POST /auth/signup - Create a new user.
POST /auth/login - Log in and receive a JWT token.
Image Processing
POST /pix2pix - Process an image using Pix2Pix.
POST /pansharpening - Perform pan-sharpening on uploaded images.
POST /histogram - Match histogram between images.

## 🛠 Technologies Used
Frontend: React, Axios
Backend: Flask, PyMongo
Database: MongoDB
Authentication: JWT
Image Processing: OpenCV, TensorFlow, PyWavelets
Deployment: Docker, Docker Compose

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for details.






