"""
Basic usage example of the Graive AI agent system.

This example demonstrates how to initialize and use the core components
of the Graive agent to execute a simple task.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import AgentLoop
from src.orchestrator import ToolOrchestrator
from src.context import ContextManager
from src.tools.shell.shell_tool import ShellTool
from src.tools.file.file_tool import FileTool


def main():
    """Run a basic example of the Graive agent."""
    
    # Define the system prompt
    system_prompt = """
    You are Graive, an autonomous general AI agent designed to assist users
    by translating complex requests into actionable, iterative steps.
    You operate through a rigorous agent loop process with continuous analysis,
    strategic reasoning, tool selection, action execution, and observation.
    """
    
    # Initialize components
    print("Initializing Graive AI components...")
    context_manager = ContextManager(system_prompt)
    orchestrator = ToolOrchestrator()
    
    # Register tools
    print("Registering tools...")
    shell_tool = ShellTool()
    file_tool = FileTool()
    orchestrator.register_tool(shell_tool)
    orchestrator.register_tool(file_tool)
    
    # Create agent loop
    agent = AgentLoop(orchestrator, context_manager)
    
    # Display available tools
    print("\nAvailable tools:")
    for tool in orchestrator.get_available_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Example task
    user_request = "List the files in the current directory"
    print(f"\nUser request: {user_request}")
    
    # Note: This is a simplified example. In a real implementation,
    # the agent loop would use an LLM to reason about the task and
    # select appropriate tools dynamically.
    
    print("\nAgent loop initialized successfully!")
    print("The agent is ready to process tasks.")
    
    # Display context summary
    print("\nContext summary:")
    summary = context_manager.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
