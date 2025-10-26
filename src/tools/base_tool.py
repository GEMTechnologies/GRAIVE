"""
Base tool interface for all Graive tools.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """Abstract base class for all tools in the Graive system."""
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Args:
            parameters: Tool-specific parameters
            
        Returns:
            Execution result dictionary
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate tool parameters before execution.
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @property
    def schema(self) -> Dict[str, Any]:
        """
        Return the parameter schema for this tool.
        
        Returns:
            JSON schema describing expected parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {}
        }
