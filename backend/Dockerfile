# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all backend files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask Port (5000)
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]

# # Base image for Python
# FROM python:3.10-slim

# # Set the working directory
# WORKDIR /app

# # Copy backend files to container
# COPY . .

# # Install dependencies
# RUN pip install -r requirements.txt

# # Expose Flask port
# EXPOSE 5000

# # Run Flask app
# CMD ["python", "app.py"]

