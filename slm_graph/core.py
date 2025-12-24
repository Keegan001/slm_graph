import logging
import asyncio
from typing import Optional, List

import instructor
from llama_cpp import Llama

from .schema import GraphData
from .renderer import to_mermaid, run_mmdc

logger = logging.getLogger("slm_graph.core")

class EasyGraph:
    """The high-level API for slm-graph using local Llama-cpp inference."""

    def __init__(self, model_path: str, n_ctx: int = 2048):
        """
        Initializes the local inference engine.
        
        Args:
            model_path: Path to a GGUF format model file.
            n_ctx: Context window size for the model.
        """
        logger.info(f"Loading local model from {model_path}...")
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx, verbose=False)
        
        # Patch llama-cpp with Instructor for JSON extraction
        self.client = instructor.patch(
            create=self.llm.create_chat_completion,
            mode=instructor.Mode.JSON_SCHEMA
        )

    async def generate(
        self, 
        prompt: str, 
        output_name: str = "graph", 
        formats: Optional[List[str]] = None
    ) -> str:
        """Processes prompt, validates JSON, and renders graph files."""
        formats = formats or ["svg"]
        
        logger.info("Extracting graph structure using local SLM...")
        structured_data: GraphData = self.client(
            messages=[
                {"role": "system", "content": "Extract nodes and edges into a structured graph format."},
                {"role": "user", "content": prompt}
            ],
            response_model=GraphData,
        )

        mermaid_code = to_mermaid(structured_data)
        
        # Parallel file rendering
        tasks = [run_mmdc(mermaid_code, f"{output_name}.{fmt}") for fmt in formats]
        await asyncio.gather(*tasks)
        
        return mermaid_code

    def generate_sync(self, *args, **kwargs):
        """Synchronous entry point for the generate method."""
        return asyncio.run(self.generate(*args, **kwargs))