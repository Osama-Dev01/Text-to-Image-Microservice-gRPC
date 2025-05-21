
# Stable Diffusion Image Generator

This project provides a Stable Diffusion model service via gRPC and REST API endpoints.

## Architecture

- **Backend**: gRPC server with Stable Diffusion pipeline
- **API Gateway**: FastAPI REST gateway that communicates with the gRPC server
- **Deployment**: Docker container on Hugging Face Spaces
- **CI/CD**: GitHub Actions for automatic deployment

## Setup Instructions

### Option 1: Using Docker Compose (Recommended)

1. Clone the repository
2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at https://Mahad871-text-to-image-generator.hf.space/generate

### Option 2: Local Development with Virtual Environment

#### On Linux/Mac:

```bash
# Create and activate virtual environment
./setup_venv.sh

# Start the services
./start.sh
```

#### On Windows:

```bash
# Create and activate virtual environment
setup_venv.bat

# Start the services
# You'll need to start the server and gateway separately
```

## REST API Endpoints

### POST /generate

Generates an image based on the provided prompt.

**Request Body:**

```json
{
  "prompt": "A photo of a cat in space",
  "negative_prompt": "blurry, bad quality",
  "num_inference_steps": 50,
  "guidance_scale": 7.5
}
```

**Response:**

```json
{
  "image": "base64_encoded_image_data"
}
```

## Testing with Postman

1. Open Postman and create a new request
2. Set the request type to POST
3. Enter the URL: `https://Mahad871-text-to-image-generator.hf.space/generate`
4. Go to the "Body" tab, select "raw" and "JSON"
5. Enter the request body as shown above
6. Click "Send" to test the API

## Deployment Options

### 1. Hugging Face Spaces (Docker)

This repository is configured for deployment on Hugging Face Spaces using Docker:

- The Space uses the Docker SDK (`sdk: docker` in the YAML frontmatter)
- The API is exposed on port 7860 (`app_port: 7860`)
- Deployment happens automatically via GitHub Actions

### 2. Local Development with Docker Compose

As described in the setup instructions.

## Model Information

This project uses Stable Diffusion models for image generation. The specific model can be configured in the server settings.

### Limitations and Ethical Considerations

- Generated images may reflect biases present in the training data
- The model may occasionally produce inappropriate or offensive content
- Image generation quality depends on the prompt and parameter settings
- The service requires significant GPU resources for optimal performance

## Hardware Requirements

This service requires a GPU for optimal performance. When deploying to Hugging Face Spaces, select at least a T4 GPU in the hardware settings for the Space. Although the service can run on CPU, it will be very slow.


