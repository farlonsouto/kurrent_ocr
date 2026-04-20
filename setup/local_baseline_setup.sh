#!/bin/bash
set -e

echo "=== 1. System Diagnostics ==="
echo "OS: $(lsb_release -ds)"
echo "Kernel: $(uname -r)"
echo "GPU Detected:"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv || echo "NVIDIA Driver not found!"

echo -e "\n=== 2. Installing Kubectl ==="
# 1. Get the latest stable version string
K8S_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)

# 2. Download using the variable (note the / after release)
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubectl"

# 3. Install (this uses sudo internally)
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl


echo "=== 3. Installing Helm ==="
# Package manager for K8s
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

echo "=== 4. Installing Minikube ==="
# Local Kubernetes cluster
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

echo "=== 5. Checking/Installing NVIDIA Container Toolkit ==="

# Check if the package is already installed
if dpkg -l | grep -q nvidia-container-toolkit; then
    echo "[INSTALLED] NVIDIA Container Toolkit is already present."
    # Extract and show the version
    CURRENT_VER=$(nvidia-ctk --version | head -n 1)
    echo "Version: $CURRENT_VER"
else
    echo "[MISSING] Installing NVIDIA Container Toolkit..."
    
    # 1. Setup GPG Key
    curl -fsSL https://github.io | \
        sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    
    # 2. Setup Repository
    curl -s -L https://github.io | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    # 3. Install
    sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
    
    # 4. Configure Runtime
    echo "Configuring Docker runtime for NVIDIA..."
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    echo "[SUCCESS] NVIDIA Container Toolkit installed."
fi


echo -e "\n=== Setup Complete ==="
echo "To start your ML-ready cluster, run:"
echo "minikube start --driver=docker --gpus=all"
echo "minikube addons enable nvidia-device-plugin"
echo "minikube addons enable ingress"

