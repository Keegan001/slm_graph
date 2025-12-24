import asyncio
import os
import shutil
import tempfile
import logging
import sys

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
    """
    Executes the Mermaid CLI to render the graph to a file.
    
    On Windows, we use shell=True to ensure npm-installed globals like 'mmdc' 
    are resolved correctly via the command prompt.
    """
    if not shutil.which("mmdc"):
        raise EnvironmentError(
            "mermaid-cli (mmdc) not found. Please install via: npm install -g @mermaid-js/mermaid-cli"
        )

    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False) as tmp:
        tmp.write(mermaid_code)
        tmp_path = tmp.name

    try:
        # On Windows, we often need to run through the shell to find 'mmdc'
        is_windows = sys.platform == "win32"
        
        if is_windows:
            # Construct the full command string for the shell
            cmd = f'mmdc -i "{tmp_path}" -o "{output_path}"'
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        else:
            process = await asyncio.create_subprocess_exec(
                "mmdc", "-i", tmp_path, "-o", output_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode()
            logger.error(f"mmdc failed: {error_msg}")
            raise RuntimeError(f"Mermaid rendering failed: {error_msg}")
            
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass