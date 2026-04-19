FROM pytorch/pytorch:2.2.2-cuda11.8-cudnn8-devel

# 1. Define the switch (default to gpu)
ARG TARGET=gpu

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy the entire conda folder so both files are available during build
COPY conda/ ./conda/

# 3. Use shell logic and the more memory-efficient 'update' command
RUN conda config --set solver libmamba && \
    if [ "$TARGET" = "gpu" ]; then \
        conda env update -n base -f conda/environment-gpu.yml; \
    else \
        conda env update -n base -f conda/environment-cpu.yml; \
    fi && \
    conda clean -afy

# Ensure the path matches the 'name' field in your yml files (assumed 'kurrent')
ENV PATH /opt/conda/envs/kurrent/bin:$PATH
ENV HF_HOME=/app/models/hf_cache

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
