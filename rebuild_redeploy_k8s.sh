docker build -t kurrent_ocr-kurrent-api:latest .
minikube image load kurrent_ocr-kurrent-api:latest
kubectl rollout restart deployment kurrent-ocr-api
