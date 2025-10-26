"""
Graive AI - Context Manager

The persistent memory store containing all necessary information for the Agent Loop:
- System Prompt (identity, rules, constraints)
- Task Plan (structured breakdown of goals)
- Conversation History (record of interactions)
- Tool Observations (results from executed tools)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class Message:
    """Represents a single message in the conversation."""
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user', 'assistant', 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class TaskPlan:
    """Represents the structured breakdown of the current task."""
    
    def __init__(self, goal: str):
        self.goal = goal
        self.phases: List[Dict[str, Any]] = []
        self.current_phase = 0
        self.status = "pending"  # pending, in_progress, completed, failed
        
    def add_phase(self, phase_name: str, steps: List[str]) -> None:
        """Add a phase to the task plan."""
        self.phases.append({
            "name": phase_name,
            "steps": steps,
            "completed_steps": [],
            "status": "pending"
        })
    
    def complete_step(self, phase_index: int, step: str) -> None:
        """Mark a step as completed."""
        if phase_index < len(self.phases):
            self.phases[phase_index]["completed_steps"].append(step)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task plan to dictionary."""
        return {
            "goal": self.goal,
            "phases": self.phases,
            "current_phase": self.current_phase,
            "status": self.status
        }


class ContextManager:
    """
    Manages the context and knowledge base for the Agent Loop.
    
    This component maintains all persistent information needed for reasoning,
    including conversation history, task plans, and tool observations.
    """
    
    def __init__(self, system_prompt: str):
        """
        Initialize the context manager.
        
        Args:
            system_prompt: The system prompt defining agent identity and rules
        """
        self.system_prompt = system_prompt
        self.conversation_history: List[Message] = []
        self.task_plan: Optional[TaskPlan] = None
        self.observations: List[Dict[str, Any]] = []
        
        # Add system message
        self.add_system_message(system_prompt)
    
    def add_system_message(self, content: str) -> None:
        """Add a system message to the conversation history."""
        message = Message("system", content)
        self.conversation_history.append(message)
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation history."""
        message = Message("user", content)
        self.conversation_history.append(message)
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation history."""
        message = Message("assistant", content)
        self.conversation_history.append(message)
    
    def add_observation(self, observation: Dict[str, Any]) -> None:
        """
        Add a tool observation to the context.
        
        Args:
            observation: The observation data from tool execution
        """
        observation["timestamp"] = datetime.now().isoformat()
        self.observations.append(observation)
    
    def add_error(self, error: str) -> None:
        """
        Add an error observation to the context.
        
        Args:
            error: The error message
        """
        self.add_observation({
            "type": "error",
            "message": error
        })
    
    def create_task_plan(self, goal: str) -> TaskPlan:
        """
        Create a new task plan.
        
        Args:
            goal: The main goal of the task
            
        Returns:
            The created task plan
        """
        self.task_plan = TaskPlan(goal)
        return self.task_plan
    
    def get_user_intent(self) -> str:
        """
        Extract the user's intent from the conversation history.
        
        Returns:
            The user's most recent request or intent
        """
        for message in reversed(self.conversation_history):
            if message.role == "user":
                return message.content
        return ""
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get the current state of the system.
        
        Returns:
            Dictionary containing current state information
        """
        return {
            "message_count": len(self.conversation_history),
            "observation_count": len(self.observations),
            "has_task_plan": self.task_plan is not None,
            "last_observation": self.observations[-1] if self.observations else None
        }
    
    def get_task_progress(self) -> Dict[str, Any]:
        """
        Get the current task progress.
        
        Returns:
            Task progress information
        """
        if not self.task_plan:
            return {"has_plan": False}
        
        return {
            "has_plan": True,
            "goal": self.task_plan.goal,
            "current_phase": self.task_plan.current_phase,
            "total_phases": len(self.task_plan.phases),
            "status": self.task_plan.status
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the entire context.
        
        Returns:
            Context summary
        """
        return {
            "system_prompt": self.system_prompt[:100] + "...",
            "conversation_length": len(self.conversation_history),
            "observations_count": len(self.observations),
            "task_plan": self.task_plan.to_dict() if self.task_plan else None
        }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the full conversation history.
        
        Returns:
            List of message dictionaries
        """
        return [msg.to_dict() for msg in self.conversation_history]
    
    def clear(self) -> None:
        """Clear all context except the system prompt."""
        system_msg = self.conversation_history[0]
        self.conversation_history = [system_msg]
        self.observations = []
        self.task_plan = None
