from pydantic import BaseModel, Field, AliasChoices
from typing import List, Literal, Optional

class GraphNode(BaseModel):
    id: str = Field(..., description="Short unique ID (e.g., 'A', 'start').")
    label: str = Field(
        ..., 
        validation_alias=AliasChoices('label', 'name', 'text', 'content'),
        description="The text to display inside the node."
    )
    shape: Literal["box", "diamond", "circle", "cylinder"] = Field(
        default="box", 
        description="The visual shape of the node."
    )

class GraphEdge(BaseModel):
    # Added 'from' as an alias for source
    source: str = Field(
        ..., 
        validation_alias=AliasChoices('source', 'from', 'start', 'origin'),
        description="The ID of the origin node."
    )
    # Added 'to' as an alias for target
    target: str = Field(
        ..., 
        validation_alias=AliasChoices('target', 'to', 'end', 'destination'),
        description="The ID of the destination node."
    )
    label: Optional[str] = Field(
        None, 
        validation_alias=AliasChoices('label', 'text', 'relationship'),
        description="Optional text on the connector."
    )

class GraphData(BaseModel):
    title: str = Field(
        default="Generated Graph",
        validation_alias=AliasChoices('title', 'name', 'heading'),
        description="A concise title for the graph."
    )
    direction: Literal["TD", "LR", "BT", "RL"] = Field(
        default="TD", 
        description="TD (Top-Down) or LR (Left-to-Right)."
    )
    nodes: List[GraphNode]
    edges: List[GraphEdge]