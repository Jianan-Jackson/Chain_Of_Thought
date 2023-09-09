from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    name: str
    param_type: str
    description: str
    enum: Optional[List[str]] = field(default_factory=list)
    required: bool = False

    def __post_init__(self):
        assert self.param_type in {
            "string",
            "int",
        }, '''param_type must be one of "string" or "int"'''


class Function(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """name of this function"""

    @property
    @abstractmethod
    def description(self) -> str:
        """description for this function"""

    @property
    @abstractmethod
    def parameters(self) -> List[Parameter]:
        """parameters for this function"""

    @abstractmethod
    def execute(self, input: str) -> str:
        """run this function"""

    def __str__(self) -> str:
        return self.name + ": " + self.description

    def to_dict(self) -> dict:
        parameters_dict = {
            "type": "object",
            "properties": {
                parameter.name: {
                    "type": parameter.param_type,
                    "description": parameter.description,
                    "enum": parameter.enum,
                }
                for parameter in self.parameters
            },
            "required": [
                parameter.name for parameter in self.parameters if parameter.required
            ],
        }

        return {
            "name": self.name,
            "description": self.description,
            "parameters": parameters_dict,
        }
