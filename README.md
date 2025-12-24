# SLM-Graph

SLM-Graph is a lightweight, production-grade Python library that transforms natural language descriptions into professional Mermaid.js diagrams. By embedding llama-cpp-python and using the Instructor pattern, it provides a reliable, self-contained way to generate structured graphs without external API dependencies or local server installations like Ollama.

## Key Features

- Self-Contained Inference: Uses llama-cpp-python directly in your Python process.

- Strict Schema Validation: Leverages Pydantic and Instructor to prevent AI hallucinations and ensure valid Mermaid syntax.

- Multi-Format Export: Generates SVG, PNG, and PDF exports in parallel.

- Professional Aesthetics: Automatically maps SLM output to optimized Mermaid flowchart layouts.

## Installation

1. Python Library

    ```pip install slm-graph```



2. System Rendering Dependency

    **You must have the Mermaid CLI installed for image and PDF generation:**

    ```npm install -g @mermaid-js/mermaid-cli```



3. Model Weight

    **To use the library, you need to download a Small Language Model in GGUF format.**

    Recommended Model:
    * [Llama-3.2-3B-Instruct-GGUF](https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF/resolve/main/llama-3.2-3b-instruct-q4_k_m.gguf?download=true)

## Setup Instructions:

1. Create a folder named models in your project root directory.

2. Download the .gguf file (e.g., Llama-3.2-1B-Instruct-Q4_K_M.gguf) from the links above.

3. Paste the file into the models/ folder.

## Quick Start
``` python
from slm_graph import EasyGraph
import asyncio

async def main():
    # Initialize with the path to your downloaded GGUF model
    eg = EasyGraph(model_path="models/Llama-3.2-1B-Instruct-Q4_K_M.gguf")

    # Generate graph files from a prompt
    await eg.generate(
        prompt="A customer places an order. If payment is successful, the warehouse ships it. If it fails, the order is cancelled.",
        output_name="order_process",
        formats=["svg", "png", "pdf"]
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Architecture

- `core.py`: Orchestrates local inference and Instructor patching.

- `schema.py`: Defines the data contract for nodes, edges, and graph types.

- `renderer.py`: Compiles Pydantic objects to Mermaid and handles CLI subprocesses.

## License

Distributed under the MIT License.