"""
Shell Tool - Provides command-line access for system operations

This tool enables the agent to execute shell commands, install packages,
and perform system-level operations within the sandboxed environment.
"""

import subprocess
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class ShellTool(BaseTool):
    """
    Tool for executing shell commands in the sandboxed environment.
    """
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox"):
        """
        Initialize the shell tool.
        
        Args:
            sandbox_path: Path to the sandbox directory
        """
        self.sandbox_path = sandbox_path
        
    @property
    def name(self) -> str:
        return "shell"
    
    @property
    def description(self) -> str:
        return "Execute shell commands for system operations and package installation"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute",
                    "required": True
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum execution time in seconds",
                    "default": 30
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate that required parameters are present."""
        return "command" in parameters and isinstance(parameters["command"], str)
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a shell command.
        
        Args:
            parameters: Must contain 'command' key
            
        Returns:
            Dict with stdout, stderr, and return_code
        """
        command = parameters["command"]
        timeout = parameters.get("timeout", 30)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.sandbox_path
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "error": f"Command timed out after {timeout} seconds",
                "success": False
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
