FROM python:3.11-slim  

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (updated to include OpenCV requirements)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Create results directory
RUN mkdir -p /app/results

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
# In your Dockerfile, replace the pip install line with:
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]