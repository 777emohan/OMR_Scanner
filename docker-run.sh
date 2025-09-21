#!/bin/bash

# OMR Scanner Docker Run Script

echo "🐳 OMR Scanner Docker Setup"
echo "=========================="

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t omr-scanner:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p set1_papers set2_papers results logs

# Run the container
echo "🚀 Starting OMR Scanner container..."
docker run -d \
    --name omr-scanner \
    -p 8501:8501 \
    -v $(pwd)/set1_papers:/app/set1_papers \
    -v $(pwd)/set2_papers:/app/set2_papers \
    -v $(pwd)/answers:/app/answers \
    -v $(pwd)/results:/app/results \
    -v $(pwd)/excel_answer_keys:/app/excel_answer_keys \
    omr-scanner:latest

if [ $? -eq 0 ]; then
    echo "✅ OMR Scanner container started successfully!"
    echo "🌐 Access the application at: http://localhost:8501"
    echo "📊 View results at: http://localhost:8501/omr_results_dynamic.html"
    echo ""
    echo "📋 Useful commands:"
    echo "  View logs: docker logs omr-scanner"
    echo "  Stop: docker stop omr-scanner"
    echo "  Remove: docker rm omr-scanner"
else
    echo "❌ Failed to start container!"
    exit 1
fi
