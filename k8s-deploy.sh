#!/bin/bash

# OMR Scanner Kubernetes Deployment Script

echo "☸️  OMR Scanner Kubernetes Deployment"
echo "===================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Build and push Docker image (if registry is available)
echo "📦 Building Docker image..."
docker build -t omr-scanner:latest .

# Create namespace
echo "🏗️  Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap
echo "⚙️  Creating ConfigMap..."
kubectl apply -f k8s/configmap.yaml

# Create PVC
echo "💾 Creating PersistentVolumeClaim..."
kubectl apply -f k8s/pvc.yaml

# Create Deployment
echo "🚀 Creating Deployment..."
kubectl apply -f k8s/deployment.yaml

# Create Service
echo "🌐 Creating Service..."
kubectl apply -f k8s/service.yaml

# Create Ingress (optional)
echo "🔗 Creating Ingress..."
kubectl apply -f k8s/ingress.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/omr-scanner -n omr-scanner

if [ $? -eq 0 ]; then
    echo "✅ OMR Scanner deployed successfully!"
    echo ""
    echo "📋 Useful commands:"
    echo "  View pods: kubectl get pods -n omr-scanner"
    echo "  View services: kubectl get services -n omr-scanner"
    echo "  View logs: kubectl logs -f deployment/omr-scanner -n omr-scanner"
    echo "  Port forward: kubectl port-forward service/omr-scanner-service 8501:8501 -n omr-scanner"
    echo ""
    echo "🌐 Access the application:"
    echo "  kubectl port-forward service/omr-scanner-service 8501:8501 -n omr-scanner"
    echo "  Then open: http://localhost:8501"
else
    echo "❌ Deployment failed or timed out!"
    exit 1
fi
