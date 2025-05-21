import gradio as gr
import requests
import base64
from PIL import Image
import io
import os

API_URL = "http://localhost:7860/generate"  # Update with your API URL when deployed

def generate_image(prompt, negative_prompt, steps, guidance_scale):
    try:
        response = requests.post(
            API_URL,
            json={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": steps,
                "guidance_scale": guidance_scale
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            image_bytes = base64.b64decode(data["image"])
            image = Image.open(io.BytesIO(image_bytes))
            return image, "Success!"
        else:
            return None, f"Error: {response.text}"
    except Exception as e:
        return None, f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# Stable Diffusion Image Generator")
    
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt", placeholder="A photo of a cat in space")
            negative_prompt = gr.Textbox(label="Negative Prompt", placeholder="blurry, bad quality")
            steps = gr.Slider(minimum=1, maximum=100, value=50, step=1, label="Inference Steps")
            guidance_scale = gr.Slider(minimum=1, maximum=20, value=7.5, step=0.1, label="Guidance Scale")
            generate_btn = gr.Button("Generate Image")
        
        with gr.Column():
            output_image = gr.Image(label="Generated Image")
            output_text = gr.Textbox(label="Status")
    
    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, negative_prompt, steps, guidance_scale],
        outputs=[output_image, output_text]
    )

if __name__ == "__main__":
    # Use the port specified by Hugging Face Spaces
    # Spaces typically uses port 7860 by default
    port = int(os.environ.get("PORT", 7860))
    
    # Set server_name to 0.0.0.0 to make it accessible outside the container
    demo.launch(server_port=port, server_name="0.0.0.0")
