"""
Enhanced Context Manager with Infinite Memory Integration

This module extends the base context manager to integrate the infinite memory system,
providing seamless context preservation across unlimited conversation lengths while
maintaining fast access to relevant information.
"""

import sys
import os
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.context.context_manager import ContextManager, Message, TaskPlan
from src.core.infinite_memory import InfiniteMemoryManager


class EnhancedContextManager(ContextManager):
    """
    Enhanced context manager with infinite memory capabilities.
    
    This class extends the base ContextManager to integrate sophisticated memory
    management, allowing the system to maintain context across conversations of
    any length without losing important information.
    
    Features:
    - Automatic memory compression
    - Intelligent summarization
    - Fast retrieval of relevant historical context
    - Complete persistence across sessions
    - Never loses context regardless of conversation length
    """
    
    def __init__(
        self,
        system_prompt: str,
        enable_infinite_memory: bool = True,
        memory_storage_path: str = "./memory_store"
    ):
        """
        Initialize enhanced context manager.
        
        Args:
            system_prompt: System prompt defining agent identity
            enable_infinite_memory: Whether to enable infinite memory
            memory_storage_path: Path for memory persistence
        """
        super().__init__(system_prompt)
        
        self.enable_infinite_memory = enable_infinite_memory
        
        if enable_infinite_memory:
            self.memory_manager = InfiniteMemoryManager(
                working_memory_size=20,
                short_term_segments=10,
                compression_threshold=50000,
                storage_path=memory_storage_path
            )
            print(f"[Context] Infinite memory enabled. Storage: {memory_storage_path}")
        else:
            self.memory_manager = None
    
    def add_user_message(self, content: str) -> None:
        """Add user message to both base context and infinite memory."""
        super().add_user_message(content)
        
        if self.memory_manager:
            self.memory_manager.add_message({
                "role": "user",
                "content": content
            })
    
    def add_assistant_message(self, content: str) -> None:
        """Add assistant message to both base context and infinite memory."""
        super().add_assistant_message(content)
        
        if self.memory_manager:
            self.memory_manager.add_message({
                "role": "assistant",
                "content": content
            })
    
    def add_observation(self, observation: Dict[str, Any]) -> None:
        """Add observation with memory tracking."""
        super().add_observation(observation)
        
        if self.memory_manager:
            # Add observation to memory
            obs_content = f"[Observation] {observation.get('type', 'unknown')}: {str(observation)[:200]}"
            self.memory_manager.add_message({
                "role": "system",
                "content": obs_content
            })
    
    def get_context_for_llm(
        self,
        max_tokens: int = 8000,
        include_system_prompt: bool = True
    ) -> List[Dict[str, str]]:
        """
        Get optimized context for LLM with automatic compression.
        
        This method intelligently manages context to stay within token limits
        while preserving all critical information through summarization.
        
        Args:
            max_tokens: Maximum token count for context
            include_system_prompt: Whether to include system prompt
            
        Returns:
            List of messages optimized for LLM
        """
        if not self.memory_manager:
            # Fall back to base implementation
            messages = []
            if include_system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            # Add recent conversation
            for msg in self.conversation_history[-20:]:
                messages.append(msg.to_dict())
            
            return messages
        
        # Use infinite memory manager to get optimized context
        messages = self.memory_manager.get_context_for_llm(max_tokens)
        
        # Ensure system prompt is included
        if include_system_prompt:
            # Check if system message already exists
            has_system = any(m.get("role") == "system" for m in messages)
            
            if not has_system:
                messages.insert(0, {
                    "role": "system",
                    "content": self.system_prompt
                })
            else:
                # Enhance existing system message with original prompt
                for msg in messages:
                    if msg.get("role") == "system":
                        msg["content"] = f"{self.system_prompt}\n\n{msg['content']}"
                        break
        
        return messages
    
    def search_context(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search historical context for relevant information.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of relevant context segments
        """
        if not self.memory_manager:
            # Simple search in conversation history
            results = []
            for msg in self.conversation_history:
                if query.lower() in msg.content.lower():
                    results.append({
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat()
                    })
                    
                    if len(results) >= max_results:
                        break
            
            return results
        
        # Use memory manager's search
        return self.memory_manager.search_memory(query, max_results)
    
    def get_full_context_summary(self) -> str:
        """
        Get comprehensive context summary including all memory tiers.
        
        Returns:
            Full context summary
        """
        if not self.memory_manager:
            summary_dict = super().get_summary()
            return str(summary_dict)
        
        return self.memory_manager.get_full_context()
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """
        Get detailed memory usage statistics.
        
        Returns:
            Memory statistics dictionary
        """
        base_stats = {
            "conversation_length": len(self.conversation_history),
            "observations_count": len(self.observations),
            "has_task_plan": self.task_plan is not None
        }
        
        if self.memory_manager:
            memory_stats = self.memory_manager.get_statistics()
            base_stats.update(memory_stats)
        
        return base_stats
    
    def inject_context(self, context: str, role: str = "system"):
        """
        Inject additional context in real-time.
        
        Args:
            context: Context to inject
            role: Message role (system, user, assistant)
        """
        message = Message(role, context)
        self.conversation_history.append(message)
        
        if self.memory_manager:
            self.memory_manager.add_message({
                "role": role,
                "content": context
            })
        
        print(f"[Context] Injected {role} context: {context[:50]}...")
    
    def compress_memory_now(self):
        """Force immediate memory compression."""
        if self.memory_manager:
            print("[Context] Forcing memory compression...")
            self.memory_manager._compress_working_memory()
            print("[Context] Compression complete.")
        else:
            print("[Context] Infinite memory not enabled.")
    
    def save_checkpoint(self, checkpoint_name: str = "auto"):
        """
        Save current context state as checkpoint.
        
        Args:
            checkpoint_name: Name for the checkpoint
        """
        if self.memory_manager:
            self.memory_manager._save_memory()
            print(f"[Context] Checkpoint saved: {checkpoint_name}")
    
    def clear_working_memory_only(self):
        """Clear only working memory, preserve historical context."""
        if self.memory_manager:
            # Compress current working memory first
            self.memory_manager._compress_working_memory()
            
            # Clear conversation history but keep system message
            system_msg = self.conversation_history[0]
            self.conversation_history = [system_msg]
            
            print("[Context] Working memory cleared, historical context preserved.")
        else:
            self.clear()
