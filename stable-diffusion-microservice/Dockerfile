FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch and CUDA
# RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install torch==2.3.0 torchvision==0.18.0 --extra-index-url https://download.pytorch.org/whl/cu118

# Copy proto files and generate gRPC code
COPY protos/ /app/protos/
COPY generate_grpc.py /app/
RUN pip install --no-cache-dir grpcio grpcio-tools
RUN python generate_grpc.py

# Install all dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gradio>=3.40.0 fastapi uvicorn

# Copy application code
COPY . /app/

# Expose ports
EXPOSE 7860

# Make start script executable
RUN chmod +x /app/start.sh

# Start the services
CMD ["/app/start.sh"]
