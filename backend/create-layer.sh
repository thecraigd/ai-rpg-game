#!/bin/bash

# Clean up any existing files
rm -rf layer-build lambda-layer.zip

# Create a temporary build directory
mkdir -p layer-build

# Create Dockerfile for layer building
cat > layer-build/Dockerfile << 'EOF'
FROM public.ecr.aws/lambda/python:3.9 as builder

# Install zip utility
RUN yum install -y zip unzip

# Create directory structure
RUN mkdir -p /opt/python/lib/python3.9/site-packages

# Copy requirements file
COPY requirements-layer.txt .

# Install dependencies
RUN pip install -r requirements-layer.txt -t /opt/python/lib/python3.9/site-packages/

# Remove unnecessary files
RUN find /opt/python -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/python -type d -name "docs" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/python -type f -name "*.pyc" -delete
RUN find /opt/python -type f -name "*.pyo" -delete

# Create zip file
RUN cd /opt && zip -r /tmp/lambda-layer.zip .

# List contents for verification
RUN unzip -l /tmp/lambda-layer.zip

# Start a new stage for copying
FROM alpine

COPY --from=builder /tmp/lambda-layer.zip /lambda-layer.zip

CMD ["cp", "/lambda-layer.zip", "/output/lambda-layer.zip"]
EOF

# Copy requirements file to build directory
cp requirements-layer.txt layer-build/

# Build the Docker image
echo "Building Docker image..."
docker build --platform linux/amd64 -t lambda-layer-builder layer-build/

# Copy the layer zip from the container
echo "Extracting layer zip..."
docker run --rm --platform linux/amd64 -v "$PWD":/output lambda-layer-builder

echo "Layer package size:"
du -sh lambda-layer.zip

# Verify contents
echo "Verifying layer contents..."
unzip -l lambda-layer.zip | grep python/lib/python3.9/site-packages/

# Clean up
rm -rf layer-build