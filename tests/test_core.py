import pytest
import os
import asyncio
from slm_graph import EasyGraph

@pytest.mark.asyncio
async def test_end_to_end_generation():
    # 1. Setup - Point to your local model
    model_path = "models/llama-3.2-3b-instruct-q4_k_m.gguf" # Update with your filename
    if not os.path.exists(model_path):
        pytest.skip("Model file not found, skipping inference test.")

    eg = EasyGraph(model_path=model_path)

    # 2. Execution
    output_name = "test_output"
    mermaid_code = await eg.generate(
        prompt="A simple login flow: User enters credentials -> Success -> Dashboard",
        output_name=output_name,
        formats=["svg"]
    )

    # 3. Assertions
    assert "flowchart" in mermaid_code.lower()
    assert os.path.exists(f"{output_name}.svg")

    # Cleanup
    if os.path.exists(f"{output_name}.svg"):
        os.remove(f"{output_name}.svg")