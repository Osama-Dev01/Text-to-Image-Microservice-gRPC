import grpc
import time
import asyncio
import image_generation_pb2
import image_generation_pb2_grpc
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# gRPC client
def create_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return image_generation_pb2_grpc.ImageGeneratorStub(channel)

def generate_image(prompt, negative_prompt="", steps=50, guidance_scale=7.5):
    stub = create_stub()
    request = image_generation_pb2.GenerationRequest(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=steps,
        guidance_scale=guidance_scale
    )
    
    start_time = time.time()
    response = stub.GenerateImage(request)
    end_time = time.time()
    
    return end_time - start_time

async def test_concurrent_requests(num_requests, concurrency):
    prompts = [
        f"A photo of a {animal} in {place}" 
        for animal, place in zip(
            ['cat', 'dog', 'bird', 'rabbit', 'fox'] * 20,
            ['space', 'forest', 'ocean', 'mountains', 'city'] * 20
        )
    ][:num_requests]
    
    times = []
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        
        for prompt in prompts:
            tasks.append(
                loop.run_in_executor(
                    executor,
                    generate_image,
                    prompt
                )
            )
        
        for result in await asyncio.gather(*tasks):
            times.append(result)
    
    return times

async def run_performance_test():
    concurrency_levels = [1, 2, 4, 8]
    results = {}
    
    for concurrency in concurrency_levels:
        print(f"Testing with concurrency level: {concurrency}")
        times = await test_concurrent_requests(10, concurrency)
        results[concurrency] = times
        print(f"Average response time: {np.mean(times):.2f}s")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    
    for concurrency, times in results.items():
        plt.plot(range(1, len(times) + 1), times, label=f"Concurrency: {concurrency}")
    
    plt.xlabel("Request Number")
    plt.ylabel("Response Time (seconds)")
    plt.title("Response Time vs. Concurrency Level")
    plt.legend()
    plt.grid(True)
    plt.savefig("performance_results.png")
    plt.close()
    
    # Plot average response times
    avg_times = [np.mean(times) for times in results.values()]
    
    plt.figure(figsize=(8, 5))
    plt.bar(concurrency_levels, avg_times)
    plt.xlabel("Concurrency Level")
    plt.ylabel("Average Response Time (seconds)")
    plt.title("Average Response Time vs. Concurrency Level")
    plt.grid(True, axis='y')
    plt.savefig("avg_response_times.png")

if __name__ == "__main__":
    asyncio.run(run_performance_test())