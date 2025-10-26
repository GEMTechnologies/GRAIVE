"""
Unit tests for the Context Manager component.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.context import ContextManager, Message, TaskPlan


class TestContextManager:
    """Test suite for the ContextManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system_prompt = "You are a test AI agent"
        self.context = ContextManager(self.system_prompt)
    
    def test_initialization(self):
        """Test that the context manager initializes correctly."""
        assert self.context.system_prompt == self.system_prompt
        assert len(self.context.conversation_history) == 1
        assert self.context.conversation_history[0].role == "system"
    
    def test_add_user_message(self):
        """Test adding a user message."""
        self.context.add_user_message("Hello")
        assert len(self.context.conversation_history) == 2
        assert self.context.conversation_history[-1].role == "user"
        assert self.context.conversation_history[-1].content == "Hello"
    
    def test_add_assistant_message(self):
        """Test adding an assistant message."""
        self.context.add_assistant_message("Hi there")
        assert len(self.context.conversation_history) == 2
        assert self.context.conversation_history[-1].role == "assistant"
    
    def test_add_observation(self):
        """Test adding an observation."""
        observation = {"tool": "test", "result": "success"}
        self.context.add_observation(observation)
        assert len(self.context.observations) == 1
        assert "timestamp" in self.context.observations[0]
    
    def test_create_task_plan(self):
        """Test creating a task plan."""
        task_plan = self.context.create_task_plan("Test goal")
        assert isinstance(task_plan, TaskPlan)
        assert task_plan.goal == "Test goal"
        assert self.context.task_plan is not None
    
    def test_get_user_intent(self):
        """Test getting user intent."""
        self.context.add_user_message("Do something")
        intent = self.context.get_user_intent()
        assert intent == "Do something"


if __name__ == "__main__":
    pytest.main([__file__])
