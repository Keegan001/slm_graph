import logging
import asyncio
from typing import Optional, List, Any

import instructor
from llama_cpp import Llama

from .schema import GraphData
from .renderer import to_mermaid, run_mmdc

logger = logging.getLogger("slm_graph.core")

class DictToObject:
    """Wraps llama-cpp-python dicts into objects for instructor."""
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DictToObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DictToObject(b) if isinstance(b, dict) else b)

class EasyGraph:
    """Robust API for slm-graph with increased context and schema flexibility."""

    def __init__(self, model_path: str, n_ctx: int = 4096):
        """
        Initializes the local inference engine.
        Increased default n_ctx to 4096 to prevent context overflow.
        """
        logger.info(f"Loading model from {model_path} (n_ctx={n_ctx})...")
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx, verbose=False)
        
        def llama_cpp_create_wrapper(*args, **kwargs):
            kwargs['response_format'] = {"type": "json_object"}
            response_dict = self.llm.create_chat_completion(*args, **kwargs)
            return DictToObject(response_dict)

        self.client = instructor.patch(
            create=llama_cpp_create_wrapper,
            mode=instructor.Mode.JSON_SCHEMA
        )

    async def generate(
        self, 
        prompt: str, 
        output_name: str = "graph", 
        formats: Optional[List[str]] = None,
        max_retries: int = 3
    ) -> str:
        formats = formats or ["svg"]
        
        # Concise but strict system prompt to reduce token count
        system_msg = (
            "Generate a flowchart JSON. Required: 'title', 'nodes' (id, label), 'edges' (source, target). "
            "Output JSON only."
        )

        try:
            structured_data: GraphData = self.client(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Graph: {prompt}"}
                ],
                response_model=GraphData,
                max_retries=max_retries
            )

            mermaid_code = to_mermaid(structured_data)
            
            tasks = [run_mmdc(mermaid_code, f"{output_name}.{fmt}") for fmt in formats]
            await asyncio.gather(*tasks)
            
            return mermaid_code
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise

    def generate_sync(self, *args, **kwargs):
        return asyncio.run(self.generate(*args, **kwargs))