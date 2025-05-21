#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows, use: venv\Scripts\activate
source venv/bin/activate

# Install dependencies for both server and gateway
pip install -r requirements.server.txt -r requirements.gateway.txt

# Generate gRPC code
python generate_grpc.py

echo "Setup complete! Virtual environment is activated and dependencies are installed."