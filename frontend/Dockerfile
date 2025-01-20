# Use Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy frontend files
COPY . /app

# Install frontend dependencies
RUN npm install

# Build React app for production
RUN npm run build

# Expose frontend port (3000)
EXPOSE 3000

# Serve the app
CMD ["npm", "start"]


# # Base image for Node.js
# FROM node:20

# # Set working directory
# WORKDIR /app

# # Copy package files
# COPY package.json ./

# # Install dependencies
# RUN npm install

# # Copy rest of the files
# COPY . .

# # Build React app
# RUN npm run build

# # Serve the frontend with a lightweight server
# RUN npm install -g serve

# # Expose the frontend port
# EXPOSE 3000

# # Serve build directory
# CMD ["serve", "-s", "build"]
