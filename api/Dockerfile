# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for TensorFlow, PyTorch, and others
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the Flask app
EXPOSE 8080

# Set the environment variable for Gunicorn
ENV PATH="/usr/local/bin:$PATH"

# Use Gunicorn to serve the app
CMD ["gunicorn", "-w", "4", "app:app"]
