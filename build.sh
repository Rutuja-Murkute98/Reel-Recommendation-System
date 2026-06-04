#!/bin/bash
set -e

echo "Upgrading Python packaging tools..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating models directory..."
mkdir -p models

echo "Build complete."
