# Use a lightweight Miniconda base
FROM continuumio/miniconda3:latest

# Install system dependencies for OpenCV and Image processing
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the environment file
COPY conda/environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Ensure the environment is used by updating the PATH
# (Replace 'archion-ocr' with the name inside your environment.yml)
ENV PATH /opt/conda/envs/archion-ocr/bin:$PATH

# Pre-set the Hugging Face cache directory to a persistent volume
ENV HF_HOME=/app/models/hf_cache

# Copy source code
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
