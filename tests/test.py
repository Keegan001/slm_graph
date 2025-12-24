from slm_graph import EasyGraph
import asyncio

async def main():
    # Initialize with the path to your downloaded GGUF model
    eg = EasyGraph(model_path="models/llama-3.2-3b-instruct-q4_k_m.gguf")

    # Generate graph files from a prompt
    await eg.generate(
        prompt="A customer places an order. If payment is successful, the warehouse ships it. If it fails, the order is cancelled.",
        output_name="order_process",
        formats=["svg", "png", "pdf"]
    )

if __name__ == "__main__":
    asyncio.run(main())