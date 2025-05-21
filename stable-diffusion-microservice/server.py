import grpc
import torch
from diffusers import StableDiffusionPipeline
import image_generation_pb2
import image_generation_pb2_grpc
from concurrent import futures
import base64
from io import BytesIO
import logging
import os

class ImageGeneratorServicer(image_generation_pb2_grpc.ImageGeneratorServicer):
    def __init__(self):
        # Determine device and appropriate dtype
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        # Set cache directory to a writable location
        os.environ["HF_HOME"] = "/tmp/huggingface"
        os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/transformers"
        os.environ["DIFFUSERS_CACHE"] = "/tmp/huggingface/diffusers"
        
        # Create cache directories with proper permissions
        os.makedirs("/tmp/huggingface", exist_ok=True)
        os.makedirs("/tmp/huggingface/transformers", exist_ok=True)
        os.makedirs("/tmp/huggingface/diffusers", exist_ok=True)
        
        # Try to load model from local cache first
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=dtype,
                safety_checker=None,  # Disable safety checker
                cache_dir="/tmp/huggingface"
            ).to(device)
            
            logging.info("Safety checker disabled to prevent false positives")
            logging.info(f"Model loaded using {device} with {dtype}")
        except Exception as e:
            logging.info(f"Model not found locally, downloading: {str(e)}")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=dtype,
                safety_checker=None,
                cache_dir="/tmp/huggingface"
            ).to(device)
            logging.info(f"Model downloaded and loaded successfully using {device} with {dtype}")

    def GenerateImage(self, request, context):
        try:
            logging.info(f"Received request with prompt: {request.prompt}")
            
            # Generate image
            image = self.pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                num_inference_steps=request.num_inference_steps,
                guidance_scale=request.guidance_scale
            ).images[0]
            
            # Convert to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return image_generation_pb2.GenerationResponse(
                status="success",
                image=img_str,
                prompt=request.prompt
            )
        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return image_generation_pb2.GenerationResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_generation_pb2_grpc.add_ImageGeneratorServicer_to_server(
        ImageGeneratorServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()






