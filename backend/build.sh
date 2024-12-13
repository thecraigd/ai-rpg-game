#!/bin/bash

# Clean up old artifacts
rm -rf dist ai-rpg-game.zip
docker rm lambda-container 2>/dev/null || true

# Build the Docker image
docker build --platform linux/amd64 --no-cache -t lambda-fastapi .

# Create a container and copy the files
docker create --name lambda-container lambda-fastapi
mkdir -p dist
docker cp lambda-container:/var/task/. dist/
docker rm lambda-container

# Create zip file
cd dist
zip -r ../ai-rpg-game.zip .
cd ..

# Verify zip contents
echo "Zip contents:"
unzip -l ai-rpg-game.zip | head -n 10