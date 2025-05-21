from fastapi import FastAPI, HTTPException
import grpc
import image_generation_pb2
import image_generation_pb2_grpc
import os

app = FastAPI()

# Get gRPC server address from environment variable or use default
GRPC_SERVER = os.environ.get("GRPC_SERVER", "localhost:50051")

@app.get("/")
def read_root():
    return {"message": "Stable Diffusion API Gateway"}

@app.post("/generate")
async def generate_image(request: dict):
    try:
        # Create gRPC client
        channel = grpc.insecure_channel(GRPC_SERVER)
        stub = image_generation_pb2_grpc.ImageGeneratorStub(channel)
        
        # Default negative prompt
        default_negative = "mutated limbs, extra fingers, deformed face, misaligned eyes, unnatural expressions,incorrect proportions, awkward angles, misplaced elements,blurry, low resolution, pixelated, distorted, noisy"
        
        # Combine user negative prompt with default negative prompt if provided
        user_negative = request.get("negative_prompt", "")
        combined_negative = f"{user_negative}, {default_negative}" if user_negative else default_negative
        
        # Prepare request
        grpc_request = image_generation_pb2.GenerationRequest(
            prompt=request.get("prompt", ""),
            negative_prompt=combined_negative,
            num_inference_steps=request.get("num_inference_steps", 30),
            guidance_scale=request.get("guidance_scale", 7.5)
        )
        
        # Call gRPC service
        response = stub.GenerateImage(grpc_request)
        
        return {
            "status": response.status,
            "image": response.image,
            "prompt": response.prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=7861)
    uvicorn.run(app, host="0.0.0.0", port=7860)