# core/tool.py

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Callable, Union


@dataclass
class Parameter:
    """Defines a structured parameter for tools."""
    name: str
    type: str
    description: str
    enum: Optional[List[Union[str, int, float]]] = None  # Allowed values
    required: bool = True  # Defaults to required


    def to_dict(self) -> Dict:
        """Convert the parameter to a dictionary for tool metadata usage."""
        param_dict = {
            "type": self.type,
            "description": self.description,
        }
        if self.enum:
            param_dict["enum"] = self.enum
        return param_dict


@dataclass
class Tool:
    name: Optional[str] = field(default="")
    description: str = None
    function: Callable = None
    parameters: List[Parameter] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        "author": "",
        "version": "1.0",
        "category": "",
    })    
    
    
    def get_parameters_schema(self) -> Dict:
        """Generate a structured schema for the tool's parameters."""
        return {
            "type": "object",
            "properties": {p.name: p.to_dict() for p in self.parameters},
            "required": [p.name for p in self.parameters if p.required],
        }