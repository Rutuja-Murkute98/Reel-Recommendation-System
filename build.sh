#!/bin/bash

# Build script for Render deployment
# Install dependencies with --only-binary to avoid compilation

echo "Installing dependencies with pre-built wheels only..."
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: -r requirements.txt 2>/dev/null || pip install -r requirements.txt

echo "Creating models directory..."
mkdir -p models

echo "✓ Build complete!"
