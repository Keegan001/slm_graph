import asyncio
import os
import shutil
import tempfile
import logging

logger = logging.getLogger("slm_graph.renderer")

def to_mermaid(data: "GraphData") -> str:
    """Converts a GraphData Pydantic object into a Mermaid flowchart string."""
    lines = [f"flowchart {data.direction}"]
    
    shapes = {
        "box": ("[", "]"),
        "diamond": ("{", "}"),
        "circle": ("((", "))"),
        "cylinder": ("[(", ")]")
    }

    for n in data.nodes:
        start, end = shapes.get(n.shape, ("[", "]"))
        lines.append(f'    {n.id}{start}"{n.label}"{end}')

    for e in data.edges:
        arrow = f" -- \"{e.label}\" --> " if e.label else " --> "
        lines.append(f'    {e.source}{arrow}{e.target}')

    return "\n".join(lines)

async def run_mmdc(mermaid_code: str, output_path: str):
    """Executes the Mermaid CLI to render the graph to a file."""
    if not shutil.which("mmdc"):
        raise EnvironmentError(
            "mermaid-cli (mmdc) not found. Please install via: npm install -g @mermaid-js/mermaid-cli"
        )

    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as tmp:
        tmp.write(mermaid_code)
        tmp_path = tmp.name

    try:
        process = await asyncio.create_subprocess_exec(
            "mmdc", "-i", tmp_path, "-o", output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(f"mmdc failed: {stderr.decode()}")
            raise RuntimeError(f"Mermaid rendering failed: {stderr.decode()}")
            
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)