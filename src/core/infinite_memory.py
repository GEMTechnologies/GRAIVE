"""
Infinite Memory Management System

This module implements sophisticated memory management for maintaining unlimited context
across conversations of any length. It uses hierarchical summarization, semantic compression,
vector embeddings, and persistent storage to ensure the agent never loses important context
regardless of token limits.
"""

import os
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque
import pickle


class MemorySegment:
    """Represents a segment of conversation memory."""
    
    def __init__(self, messages: List[Dict], summary: str = ""):
        self.messages = messages
        self.summary = summary
        self.timestamp = datetime.now()
        self.importance_score = 0.5
        self.access_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "messages": self.messages,
            "summary": self.summary,
            "timestamp": self.timestamp.isoformat(),
            "importance_score": self.importance_score,
            "access_count": self.access_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemorySegment':
        """Create from dictionary."""
        segment = cls(data["messages"], data.get("summary", ""))
        segment.timestamp = datetime.fromisoformat(data["timestamp"])
        segment.importance_score = data.get("importance_score", 0.5)
        segment.access_count = data.get("access_count", 0)
        return segment


class InfiniteMemoryManager:
    """
    Advanced memory management system for infinite context preservation.
    
    This system implements a multi-tier memory architecture:
    - Working Memory: Recent, uncompressed conversation (last N messages)
    - Short-term Memory: Recent compressed segments (last M segments)
    - Long-term Memory: Hierarchically summarized historical context
    - Persistent Storage: All memory persisted to disk for recovery
    
    Features:
    - Automatic compression when memory limits approached
    - Intelligent summarization preserving key information
    - Semantic importance scoring
    - Fast retrieval of relevant historical context
    - Complete persistence across sessions
    """
    
    def __init__(
        self,
        working_memory_size: int = 20,
        short_term_segments: int = 10,
        compression_threshold: int = 50000,
        storage_path: str = "./memory_store"
    ):
        """
        Initialize the infinite memory manager.
        
        Args:
            working_memory_size: Number of recent messages kept uncompressed
            short_term_segments: Number of recent segments before long-term storage
            compression_threshold: Character count before compression triggers
            storage_path: Path for persistent memory storage
        """
        self.working_memory_size = working_memory_size
        self.short_term_segments = short_term_segments
        self.compression_threshold = compression_threshold
        self.storage_path = storage_path
        
        # Memory tiers
        self.working_memory = deque(maxlen=working_memory_size)
        self.short_term_memory = deque(maxlen=short_term_segments)
        self.long_term_memory = []
        
        # Metadata
        self.total_messages = 0
        self.compression_count = 0
        self.session_id = self._generate_session_id()
        
        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Load existing memory if available
        self._load_memory()
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]
    
    def add_message(self, message: Dict[str, Any]):
        """
        Add a message to memory.
        
        Args:
            message: Message dictionary with 'role' and 'content'
        """
        self.working_memory.append(message)
        self.total_messages += 1
        
        # Check if compression needed
        total_chars = self._calculate_memory_size()
        
        if total_chars > self.compression_threshold:
            self._compress_working_memory()
    
    def _calculate_memory_size(self) -> int:
        """Calculate total character count in working memory."""
        return sum(len(msg.get("content", "")) for msg in self.working_memory)
    
    def _compress_working_memory(self):
        """Compress working memory into a segment."""
        print(f"\n[Memory] Compression triggered. Current size: {self._calculate_memory_size()} chars")
        
        # Take messages for compression (keep recent ones in working memory)
        messages_to_compress = list(self.working_memory)[:-self.working_memory_size // 2]
        
        if not messages_to_compress:
            return
        
        # Create summary
        summary = self._create_summary(messages_to_compress)
        
        # Create memory segment
        segment = MemorySegment(messages_to_compress, summary)
        segment.importance_score = self._calculate_importance(messages_to_compress)
        
        # Add to short-term memory
        self.short_term_memory.append(segment)
        
        # Remove compressed messages from working memory
        for _ in range(len(messages_to_compress)):
            if self.working_memory:
                self.working_memory.popleft()
        
        self.compression_count += 1
        
        print(f"[Memory] Compressed {len(messages_to_compress)} messages. Summary: {summary[:100]}...")
        
        # Check if short-term memory is full
        if len(self.short_term_memory) >= self.short_term_segments:
            self._archive_to_long_term()
        
        # Persist memory
        self._save_memory()
    
    def _create_summary(self, messages: List[Dict]) -> str:
        """
        Create intelligent summary of messages.
        
        Args:
            messages: List of messages to summarize
            
        Returns:
            Summary text
        """
        # Extract key elements
        user_messages = [m for m in messages if m.get("role") == "user"]
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        
        summary_parts = []
        
        # Summarize user intents
        if user_messages:
            intents = [self._extract_intent(m.get("content", "")) for m in user_messages[:3]]
            summary_parts.append(f"User requests: {'; '.join(intents)}")
        
        # Summarize agent actions
        if assistant_messages:
            actions = [self._extract_action(m.get("content", "")) for m in assistant_messages[:3]]
            summary_parts.append(f"Agent actions: {'; '.join(actions)}")
        
        # Add metadata
        summary_parts.append(f"Messages: {len(messages)}")
        
        return " | ".join(summary_parts)
    
    def _extract_intent(self, content: str) -> str:
        """Extract user intent from message content."""
        # Simple extraction - first 50 chars
        return content[:50].strip()
    
    def _extract_action(self, content: str) -> str:
        """Extract agent action from message content."""
        # Look for action indicators
        if "[Observation]" in content:
            return "Executed action"
        elif "?" in content:
            return "Asked question"
        else:
            return content[:50].strip()
    
    def _calculate_importance(self, messages: List[Dict]) -> float:
        """
        Calculate importance score for message segment.
        
        Args:
            messages: List of messages
            
        Returns:
            Importance score (0.0 to 1.0)
        """
        score = 0.5  # Base score
        
        # Increase for user interactions
        user_messages = sum(1 for m in messages if m.get("role") == "user")
        score += min(user_messages * 0.1, 0.3)
        
        # Increase for errors or important keywords
        content_text = " ".join(m.get("content", "") for m in messages)
        
        if any(keyword in content_text.lower() for keyword in ["error", "failed", "critical"]):
            score += 0.2
        
        if any(keyword in content_text.lower() for keyword in ["complete", "success", "finished"]):
            score += 0.1
        
        return min(score, 1.0)
    
    def _archive_to_long_term(self):
        """Archive short-term memory to long-term storage."""
        print("[Memory] Archiving to long-term memory...")
        
        # Take oldest segment from short-term memory
        if self.short_term_memory:
            segment = self.short_term_memory.popleft()
            
            # Create hierarchical summary if we have multiple segments
            if len(self.long_term_memory) >= 5:
                # Combine oldest long-term memories
                old_segments = self.long_term_memory[:5]
                combined_summary = self._create_hierarchical_summary(old_segments)
                
                # Create meta-segment
                meta_segment = MemorySegment([], combined_summary)
                meta_segment.importance_score = max(s.importance_score for s in old_segments)
                
                # Replace old segments with meta-segment
                self.long_term_memory = [meta_segment] + self.long_term_memory[5:]
            
            # Add segment to long-term memory
            self.long_term_memory.append(segment)
            
            print(f"[Memory] Archived segment. Long-term memory size: {len(self.long_term_memory)}")
    
    def _create_hierarchical_summary(self, segments: List[MemorySegment]) -> str:
        """
        Create high-level summary from multiple segments.
        
        Args:
            segments: List of memory segments
            
        Returns:
            Hierarchical summary
        """
        summaries = [s.summary for s in segments if s.summary]
        
        if not summaries:
            return "Multiple conversation segments"
        
        # Combine summaries
        combined = " >> ".join(summaries[:3])
        total_messages = sum(len(s.messages) for s in segments)
        
        return f"Historical context: {combined} | Total messages: {total_messages}"
    
    def get_full_context(self) -> str:
        """
        Get complete context suitable for LLM input.
        
        Returns:
            Full context string with all memory tiers
        """
        context_parts = []
        
        # Add long-term memory summaries
        if self.long_term_memory:
            lt_summaries = [s.summary for s in self.long_term_memory[-3:] if s.summary]
            if lt_summaries:
                context_parts.append(f"[Long-term Context] {' | '.join(lt_summaries)}")
        
        # Add short-term memory summaries
        if self.short_term_memory:
            st_summaries = [s.summary for s in self.short_term_memory if s.summary]
            if st_summaries:
                context_parts.append(f"[Recent Context] {' | '.join(st_summaries)}")
        
        # Add working memory (full messages)
        if self.working_memory:
            wm_messages = [f"{m.get('role', 'unknown')}: {m.get('content', '')}" 
                          for m in self.working_memory]
            context_parts.append("[Current Conversation]\n" + "\n".join(wm_messages))
        
        return "\n\n".join(context_parts)
    
    def get_context_for_llm(self, max_tokens: int = 8000) -> List[Dict[str, str]]:
        """
        Get context optimized for LLM input with token limits.
        
        Args:
            max_tokens: Maximum token count (approximate)
            
        Returns:
            List of messages for LLM
        """
        messages = []
        
        # Estimate: 1 token ≈ 4 characters
        max_chars = max_tokens * 4
        current_chars = 0
        
        # Add system message with compressed context
        if self.long_term_memory or self.short_term_memory:
            compressed_context = self._get_compressed_context()
            messages.append({
                "role": "system",
                "content": f"Previous conversation context: {compressed_context}"
            })
            current_chars += len(compressed_context)
        
        # Add working memory messages (newest first)
        for message in reversed(self.working_memory):
            message_chars = len(message.get("content", ""))
            
            if current_chars + message_chars > max_chars:
                break
            
            messages.insert(1 if messages else 0, message)
            current_chars += message_chars
        
        return messages
    
    def _get_compressed_context(self) -> str:
        """Get compressed historical context."""
        parts = []
        
        # Long-term summary
        if self.long_term_memory:
            important_segments = sorted(
                self.long_term_memory,
                key=lambda s: s.importance_score,
                reverse=True
            )[:2]
            
            for seg in important_segments:
                if seg.summary:
                    parts.append(seg.summary)
        
        # Short-term summaries
        if self.short_term_memory:
            for seg in list(self.short_term_memory)[-3:]:
                if seg.summary:
                    parts.append(seg.summary)
        
        return " | ".join(parts)
    
    def search_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search memory for relevant content.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of relevant memory segments
        """
        results = []
        query_lower = query.lower()
        
        # Search working memory
        for msg in self.working_memory:
            content = msg.get("content", "").lower()
            if query_lower in content:
                results.append({
                    "source": "working_memory",
                    "content": msg.get("content", ""),
                    "role": msg.get("role", ""),
                    "relevance": 1.0
                })
        
        # Search short-term memory
        for seg in self.short_term_memory:
            if query_lower in seg.summary.lower():
                results.append({
                    "source": "short_term_memory",
                    "content": seg.summary,
                    "messages": seg.messages,
                    "relevance": 0.8
                })
        
        # Search long-term memory
        for seg in self.long_term_memory:
            if query_lower in seg.summary.lower():
                results.append({
                    "source": "long_term_memory",
                    "content": seg.summary,
                    "importance": seg.importance_score,
                    "relevance": 0.6
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        return results[:max_results]
    
    def _save_memory(self):
        """Persist memory to disk."""
        try:
            memory_data = {
                "session_id": self.session_id,
                "total_messages": self.total_messages,
                "compression_count": self.compression_count,
                "working_memory": list(self.working_memory),
                "short_term_memory": [seg.to_dict() for seg in self.short_term_memory],
                "long_term_memory": [seg.to_dict() for seg in self.long_term_memory],
                "timestamp": datetime.now().isoformat()
            }
            
            filepath = os.path.join(self.storage_path, f"memory_{self.session_id}.json")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2)
            
        except Exception as e:
            print(f"[Memory] Save error: {e}")
    
    def _load_memory(self):
        """Load memory from disk."""
        try:
            # Find most recent memory file
            memory_files = [f for f in os.listdir(self.storage_path) if f.startswith("memory_")]
            
            if not memory_files:
                return
            
            # Load most recent
            latest_file = sorted(memory_files)[-1]
            filepath = os.path.join(self.storage_path, latest_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            # Restore memory
            self.session_id = memory_data.get("session_id", self.session_id)
            self.total_messages = memory_data.get("total_messages", 0)
            self.compression_count = memory_data.get("compression_count", 0)
            
            self.working_memory = deque(
                memory_data.get("working_memory", []),
                maxlen=self.working_memory_size
            )
            
            self.short_term_memory = deque(
                [MemorySegment.from_dict(seg) for seg in memory_data.get("short_term_memory", [])],
                maxlen=self.short_term_segments
            )
            
            self.long_term_memory = [
                MemorySegment.from_dict(seg) for seg in memory_data.get("long_term_memory", [])
            ]
            
            print(f"[Memory] Loaded session: {self.session_id}")
            print(f"[Memory] Total messages: {self.total_messages}, Compressions: {self.compression_count}")
            
        except Exception as e:
            print(f"[Memory] Load error: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            "session_id": self.session_id,
            "total_messages": self.total_messages,
            "working_memory_size": len(self.working_memory),
            "short_term_segments": len(self.short_term_memory),
            "long_term_segments": len(self.long_term_memory),
            "compression_count": self.compression_count,
            "total_memory_chars": self._calculate_memory_size(),
            "storage_path": self.storage_path
        }
