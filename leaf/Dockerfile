# Use an official Python runtime with CUDA support for machine learning
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download YOLOv5 models (assuming they're not in the repository)
RUN mkdir -p /app/models
#  download models
RUN wget -O /app/models/type_predict.pt [URL_TO_TYPE_MODEL]
RUN wget -O /app/models/disease.pt [URL_TO_DISEASE_MODEL]

# export port
EXPOSE 5005

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]