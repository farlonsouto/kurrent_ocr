## 18th-Century German Kurrent OCR Wrapper

This project provides a specialized, locally-hosted API for transcribing 18th-century German handwritten records (
Kurrent script), specifically optimized for high-resolution scans from the Archion archives (e.g., Thuringia and
Hesse/Frankfurt regions).

## 🚀 Overview

Transcribing 18th-century parish records is a unique challenge due to the angular nature of Kurrentschrift, faded
iron-gall ink, and complex layout structures. This project wraps the state-of-the-art TrOCR model fine-tuned by the
University of Bern (dh-unibe/trocr-kurrent-XVI-XVII) within a containerized Python environment.

## 🛠 Tech Stack

* Model: dh-unibe/trocr-kurrent-XVI-XVII (Vision-Encoder-Decoder via Hugging Face)
* Framework: FastAPI (Python)
* Environment: Conda/Mamba with environment.yml
* Containerization: Docker + Docker Compose
* Orchestration: Kubernetes (K8s) with NVIDIA Device Plugin
* Image Processing: OpenCV & Pillow (for binarization and line segmentation)
* Microservices approach: Allows for maintain a clean boundary between any client application and the heavy
  machine-learning.

## 📁 Project Structure

kurrent-ocr/

├── conda/

│ └── environment.yml # Conda environment definition

├── docker/

│ ├── Dockerfile # Miniconda-based build

│ └── docker-compose.yml # Orchestration & Volume mounting

├── models/ # Local model weights (gitignored)

├── src/

│ ├── api/

│ │ └── main.py # FastAPI endpoints (OpenAI-compatible)

│ ├── core/

│ │ ├── segmenter.py # Page-to-line segmentation logic

│ │ └── inference.py # TrOCR model execution

│ └── utils/

│ └── image_prep.py # Binarization & Contrast enhancement

└── data/

    └── input/                # High-res script scans images for processing

## ⚙️ Key Features

* Single-Page Pipeline: Processes high-resolution scans by segmenting them into individual lines for high-accuracy HTR.
* Historical Script Optimization: Specialized in 16th-18th century Kurrent used in the Holy Roman Empire (Hesse,
  Thuringia, etc.).
* Local & Private: Runs entirely on your hardware. No data is sent to external APIs, ensuring the privacy of
  genealogical research.
* API Emulation: Provides a RESTful endpoint that can be easily integrated into custom research tools or frontend
  clients.

## 🚦 Getting Started## Prerequisites

* Docker & Docker Compose
* NVIDIA GPU (optional, but recommended for speed)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/farlonsouto/kurrent_ocr.git
   cd kurrent-ocr
   ```

2. Download the model:
   The model weights will be downloaded automatically into the models/ directory on the first run, or you can pre-fetch
   them using the huggingface-hub CLI.
3. Launch the Service (TARGETS can be either cpu or gpu, both in lower case):

   ```bash 
   docker compose build --build-arg TARGET=gpu
   ```

## ☸️ Enterprise Kubernetes Deployment

For production-scale environments or local cluster testing, follow these steps:

1. Local Baseline Setup
   To prepare your local Linux environment (Ubuntu 22.04) for a GPU-enabled Kubernetes test, run the baseline script.
   This script checks for NVIDIA drivers, installs kubectl, helm, minikube, and configures the NVIDIA Container Toolkit.
   Of course, as this script can fail, you must either fix it accordingly or install the kubernetes-related dependencies
   manually.

```bash
chmod +x setup/local_baseline_setup.sh
./setup/local_baseline_setup.sh
```

2. Running a Local K8s Test
   Once the baseline is established, validate the microservices stack (OCR API + UI) on top of Kubernetes:

Start a GPU-enabled Cluster:

```bash
minikube start --driver=docker --gpus=all
minikube addons enable nvidia-device-plugin
minikube addons enable ingress
```

3. Apply Manifests:

```bash
# Deploy Backend & Frontend
kubectl apply -f k8s/
```

## Usage

Submit a single Archion page for transcription via POST request:

```bash
curl -X POST "http://localhost:8000/transcribe-page" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path_to_archion_scan.jpg"
```

## 📜 Historical Context

In the 18th century, the regions of Hesse and Thuringia primarily used Kurrentschrift. This project addresses the "
zig-zag" vertical stroke ambiguity of letters like e, n, and m by using a transformer-based vision model that
understands the context of the entire word/line.

## ⚖️ License

This wrapper project is provided under the [MIT License]. Note that the underlying dh-unibe model and Archion images may
be subject to their own respective licenses and terms of use.


