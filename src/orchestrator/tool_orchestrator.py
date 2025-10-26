"""
Graive AI - Tool Orchestrator

The intermediary layer that translates the Agent Loop's abstract tool selection
into concrete execution commands within the sandbox.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class ToolExecutionError(Exception):
    """Raised when a tool execution fails."""
    pass


class Tool(ABC):
    """Base class for all tools."""
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Args:
            parameters: Tool-specific parameters
            
        Returns:
            Execution result
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate tool parameters before execution.
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool description."""
        pass


class ToolOrchestrator:
    """
    Manages execution and I/O of all external capabilities.
    
    The orchestrator acts as the intermediary between the Agent Loop's
    high-level decisions and the low-level tool execution in the sandbox.
    """
    
    def __init__(self):
        """Initialize the tool orchestrator."""
        self.tools: Dict[str, Tool] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def register_tool(self, tool: Tool) -> None:
        """
        Register a new tool with the orchestrator.
        
        Args:
            tool: The tool instance to register
        """
        self.tools[tool.name] = tool
        
    def unregister_tool(self, tool_name: str) -> None:
        """
        Unregister a tool from the orchestrator.
        
        Args:
            tool_name: Name of the tool to unregister
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """
        Get list of all available tools and their descriptions.
        
        Returns:
            List of tool metadata
        """
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]
    
    def execute(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call from the Agent Loop.
        
        Args:
            tool_call: Dictionary containing tool_name and parameters
            
        Returns:
            Execution result
            
        Raises:
            ToolExecutionError: If tool execution fails
        """
        tool_name = tool_call.get("tool_name")
        parameters = tool_call.get("parameters", {})
        
        # Validate tool exists
        if tool_name not in self.tools:
            raise ToolExecutionError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        
        # Validate parameters
        if not tool.validate_parameters(parameters):
            raise ToolExecutionError(
                f"Invalid parameters for tool '{tool_name}'"
            )
        
        try:
            # Execute the tool
            result = tool.execute(parameters)
            
            # Record execution
            self._record_execution(tool_name, parameters, result, success=True)
            
            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }
            
        except Exception as e:
            # Record failure
            self._record_execution(
                tool_name, 
                parameters, 
                {"error": str(e)}, 
                success=False
            )
            
            raise ToolExecutionError(
                f"Tool '{tool_name}' execution failed: {str(e)}"
            )
    
    def _record_execution(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any],
        result: Dict[str, Any],
        success: bool
    ) -> None:
        """
        Record tool execution in history.
        
        Args:
            tool_name: Name of the executed tool
            parameters: Parameters used
            result: Execution result
            success: Whether execution was successful
        """
        self.execution_history.append({
            "tool": tool_name,
            "parameters": parameters,
            "result": result,
            "success": success
        })
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete execution history.
        
        Returns:
            List of execution records
        """
        return self.execution_history.copy()
    
    def clear_history(self) -> None:
        """Clear the execution history."""
        self.execution_history.clear()
