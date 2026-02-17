#!/bin/bash
set -e

# Define image names and contexts
REPO="jeremybradfordsr1"
PLATFORMS="linux/amd64,linux/arm64"

echo "Starting Multi-Arch Build & Push..."

# Ensure buildx builder exists
if ! docker buildx inspect p2c-builder > /dev/null 2>&1; then
    echo "Creating new buildx builder 'p2c-builder'..."
    docker buildx create --name p2c-builder --use
    docker buildx inspect --bootstrap
else
    echo "Using existing buildx builder 'p2c-builder'..."
    docker buildx use p2c-builder
fi

# 1. Frontend
echo "Building p2cfrontend..."
docker buildx build --platform $PLATFORMS -t $REPO/p2cfrontend:latest --push ./p2cfrontend

# 2. Proxy
echo "Building p2cproxy..."
docker buildx build --platform $PLATFORMS -t $REPO/p2cproxy:latest --push ./p2cproxy

# 3. API
echo "Building p2capi..."
docker buildx build --platform $PLATFORMS -t $REPO/p2capi:latest --push ./ScalableMssqlApi

# 4. Orchestrator
echo "Building orchestrator..."
docker buildx build --platform $PLATFORMS -t $REPO/orchestrator:latest --push ./P2CScripts

echo "All images built and pushed successfully!"
