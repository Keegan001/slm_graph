from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class GraphNode(BaseModel):
    id: str = Field(..., description="Short unique ID (e.g., 'A', 'start').")
    label: str = Field(..., description="The text to display inside the node.")
    shape: Literal["box", "diamond", "circle", "cylinder"] = Field(
        default="box", 
        description="The visual shape of the node."
    )

class GraphEdge(BaseModel):
    source: str = Field(..., description="The ID of the origin node.")
    target: str = Field(..., description="The ID of the destination node.")
    label: Optional[str] = Field(None, description="Optional text on the connector.")

class GraphData(BaseModel):
    title: str = Field(..., description="A concise title for the graph.")
    direction: Literal["TD", "LR", "BT", "RL"] = Field(
        default="TD", 
        description="TD (Top-Down) or LR (Left-to-Right)."
    )
    nodes: List[GraphNode]
    edges: List[GraphEdge]