"""
Unit tests for the Agent Loop component.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import AgentLoop, LoopState
from src.orchestrator import ToolOrchestrator
from src.context import ContextManager


class TestAgentLoop:
    """Test suite for the AgentLoop class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        system_prompt = "Test system prompt"
        self.context = ContextManager(system_prompt)
        self.orchestrator = ToolOrchestrator()
        self.agent = AgentLoop(self.orchestrator, self.context)
    
    def test_initialization(self):
        """Test that the agent loop initializes correctly."""
        assert self.agent.state == LoopState.ANALYZING
        assert self.agent.iteration_count == 0
        assert self.agent.max_iterations == 100
    
    def test_context_manager_injection(self):
        """Test that the context manager is properly injected."""
        assert self.agent.context is not None
        assert isinstance(self.agent.context, ContextManager)
    
    def test_orchestrator_injection(self):
        """Test that the orchestrator is properly injected."""
        assert self.agent.orchestrator is not None
        assert isinstance(self.agent.orchestrator, ToolOrchestrator)


if __name__ == "__main__":
    pytest.main([__file__])
