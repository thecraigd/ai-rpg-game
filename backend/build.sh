#!/bin/bash

# Clean old artifacts
rm -rf dist ai-rpg-game.zip
docker rm lambda-container 2>/dev/null || true

# Build Docker image with new requirements file
docker build --platform linux/amd64 --no-cache -t lambda-fastapi \
  --build-arg REQUIREMENTS_FILE=requirements-function.txt .

# Copy deployment files from container
docker create --name lambda-container lambda-fastapi
mkdir -p dist
docker cp lambda-container:/var/task/. dist/
docker rm lambda-container

# Remove any potential large packages that might have been copied
rm -rf dist/numpy* dist/pyarrow* dist/pygments* dist/PIL* dist/pillow*

# Package deployment files
cd dist
zip -r ../ai-rpg-game.zip .
cd ..

echo "Final package size:"
du -sh ai-rpg-game.zip