"""
Graive AI - Core Agent Loop

The Agent Loop is the central processing unit where AI reasoning and decision-making occur.
It operates in a continuous cycle: Analyze → Think → Select Tool → Execute → Observe.
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class LoopState(Enum):
    """Represents the current state of the agent loop."""
    ANALYZING = "analyzing"
    THINKING = "thinking"
    SELECTING_TOOL = "selecting_tool"
    EXECUTING = "executing"
    OBSERVING = "observing"
    COMPLETED = "completed"
    ERROR = "error"


class AgentLoop:
    """
    The core agent loop that governs the flow of information and decision-making.
    
    This is the sole "agent" responsible for all planning, decision-making, and execution.
    It does not delegate to specialized sub-agents but rather dynamically leverages
    a comprehensive set of tools to execute tasks.
    """
    
    def __init__(self, orchestrator, context_manager):
        """
        Initialize the Agent Loop.
        
        Args:
            orchestrator: The tool orchestrator for executing actions
            context_manager: The context/knowledge base manager
        """
        self.orchestrator = orchestrator
        self.context = context_manager
        self.state = LoopState.ANALYZING
        self.iteration_count = 0
        self.max_iterations = 100
        
    def run(self, user_request: str) -> Dict[str, Any]:
        """
        Execute the main agent loop.
        
        Args:
            user_request: The user's request or task
            
        Returns:
            Dict containing the final result and execution metadata
        """
        self.context.add_user_message(user_request)
        
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            
            try:
                # Step 1: Analyze Context
                self.state = LoopState.ANALYZING
                analysis = self._analyze_context()
                
                # Step 2: Think and Plan
                self.state = LoopState.THINKING
                plan = self._think(analysis)
                
                # Check if task is complete
                if plan.get("is_complete", False):
                    self.state = LoopState.COMPLETED
                    return self._build_response(plan)
                
                # Step 3: Select Tool
                self.state = LoopState.SELECTING_TOOL
                tool_call = self._select_tool(plan)
                
                # Step 4: Execute via Orchestrator
                self.state = LoopState.EXECUTING
                result = self.orchestrator.execute(tool_call)
                
                # Step 5: Observe and Update Context
                self.state = LoopState.OBSERVING
                self._observe(result)
                
            except Exception as e:
                self.state = LoopState.ERROR
                return self._handle_error(e)
        
        return self._build_response({"error": "Maximum iterations reached"})
    
    def _analyze_context(self) -> Dict[str, Any]:
        """
        Analyze the current context including user intent and current state.
        
        Returns:
            Dict containing the analysis results
        """
        return {
            "user_intent": self.context.get_user_intent(),
            "current_state": self.context.get_current_state(),
            "task_progress": self.context.get_task_progress(),
            "available_tools": self.orchestrator.get_available_tools()
        }
    
    def _think(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formulate strategy, update task plan, and determine next logical step.
        
        Args:
            analysis: The context analysis
            
        Returns:
            Dict containing the plan and next steps
        """
        # This is where the LLM reasoning would occur
        # For now, this is a placeholder for the planning logic
        return {
            "next_action": "placeholder",
            "reasoning": "placeholder reasoning",
            "is_complete": False
        }
    
    def _select_tool(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Choose the most appropriate tool to execute the planned step.
        
        Args:
            plan: The current plan
            
        Returns:
            Dict containing the tool call specification
        """
        return {
            "tool_name": plan.get("next_action"),
            "parameters": plan.get("parameters", {})
        }
    
    def _observe(self, result: Dict[str, Any]) -> None:
        """
        Process the execution result and update the context.
        
        Args:
            result: The result from tool execution
        """
        self.context.add_observation(result)
    
    def _build_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build the final response to return to the user.
        
        Args:
            data: The response data
            
        Returns:
            Formatted response dictionary
        """
        return {
            "state": self.state.value,
            "iterations": self.iteration_count,
            "result": data,
            "context_summary": self.context.get_summary()
        }
    
    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """
        Handle errors that occur during execution.
        
        Args:
            error: The exception that occurred
            
        Returns:
            Error response dictionary
        """
        self.context.add_error(str(error))
        return {
            "state": LoopState.ERROR.value,
            "error": str(error),
            "iterations": self.iteration_count
        }
