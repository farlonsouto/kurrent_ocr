FROM continuumio/miniconda3:latest

# 1. Define the switch (default to gpu)
ARG TARGET=gpu

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy the entire conda folder so both files are available during build
COPY conda/ ./conda/

# 3. Use shell logic to pick the file based on the TARGET arg
RUN conda config --set remote_read_timeout_secs 600 && \
    conda config --set remote_connect_timeout_secs 60 && \
    conda config --set remote_max_retries 5 && \
    if [ "$TARGET" = "gpu" ]; then \
        conda env create -f conda/environment-gpu.yml; \
    else \
        conda env create -f conda/environment-cpu.yml; \
    fi && \
    conda clean -afy

# Ensure the path matches the 'name' field in your yml files (assumed 'kurrent')
ENV PATH /opt/conda/envs/kurrent/bin:$PATH
ENV HF_HOME=/app/models/hf_cache

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
