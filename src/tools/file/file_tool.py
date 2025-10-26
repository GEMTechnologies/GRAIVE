"""
File Tool - Manages file system operations

This tool enables reading, writing, and editing files within the sandbox.
"""

import os
from typing import Dict, Any
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class FileTool(BaseTool):
    """
    Tool for file system operations in the sandboxed environment.
    """
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox"):
        """
        Initialize the file tool.
        
        Args:
            sandbox_path: Path to the sandbox directory
        """
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)
        
    @property
    def name(self) -> str:
        return "file"
    
    @property
    def description(self) -> str:
        return "Read, write, and edit files in the sandbox"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Action to perform: read, write, append",
                    "required": True
                },
                "path": {
                    "type": "string",
                    "description": "Path to the file",
                    "required": True
                },
                "content": {
                    "type": "string",
                    "description": "Content for write/append operations",
                    "required": False
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters."""
        if "action" not in parameters or "path" not in parameters:
            return False
        
        action = parameters["action"]
        if action in ["write", "append"] and "content" not in parameters:
            return False
            
        return action in ["read", "write", "append"]
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a file operation.
        
        Args:
            parameters: Must contain 'action' and 'path'
            
        Returns:
            Dict with operation result
        """
        action = parameters["action"]
        file_path = os.path.join(self.sandbox_path, parameters["path"])
        
        try:
            if action == "read":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "content": content,
                    "success": True
                }
                
            elif action == "write":
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(parameters["content"])
                return {
                    "message": "File written successfully",
                    "success": True
                }
                
            elif action == "append":
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(parameters["content"])
                return {
                    "message": "Content appended successfully",
                    "success": True
                }
                
        except FileNotFoundError:
            return {
                "error": f"File not found: {file_path}",
                "success": False
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
