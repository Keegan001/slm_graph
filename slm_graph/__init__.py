"""
slm-graph: A lightweight Python library to generate graphs from natural 
language using Small Language Models and Mermaid.js.
"""

from .core import EasyGraph
from .schema import GraphData

__version__ = "0.1.0"
__all__ = ["EasyGraph", "GraphData"]