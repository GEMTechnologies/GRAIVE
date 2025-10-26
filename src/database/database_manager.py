"""
Database Manager for Graive AI

This module provides high-level database operations for the Graive AI system,
including conversation management, message storage, memory compression tracking,
and vector search integration.
"""

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os

from .schema import (
    Base, User, Conversation, Message, MemorySegment,
    ToolExecution, Checkpoint, Document, InteractionEvent, AgentMetrics
)
from .vector_db import VectorDatabase


class DatabaseManager:
    """
    High-level database manager for Graive AI.
    
    Provides convenient methods for all database operations including conversation
    management, message storage, memory segment tracking, tool execution logging,
    and semantic search through vector database integration.
    """
    
    def __init__(
        self,
        db_url: str = "postgresql://localhost/graive",
        vector_db_path: str = "./chroma_db",
        echo: bool = False
    ):
        """
        Initialize database manager.
        
        Args:
            db_url: Database connection URL (PostgreSQL recommended)
            vector_db_path: Path for vector database storage
            echo: Whether to echo SQL statements
        """
        # Initialize SQL database
        self.engine = create_engine(db_url, echo=echo)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Initialize vector database
        self.vector_db = VectorDatabase(persist_directory=vector_db_path)
        
        print(f"[Database] Initialized: {db_url}")
        print(f"[Database] Vector DB: {vector_db_path}")
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    # User Management
    
    def create_user(
        self,
        username: str,
        email: str,
        preferences: Dict[str, Any] = None
    ) -> User:
        """Create new user."""
        session = self.get_session()
        try:
            user = User(
                username=username,
                email=email,
                preferences=preferences or {}
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def get_user(self, user_id: str = None, username: str = None) -> Optional[User]:
        """Get user by ID or username."""
        session = self.get_session()
        try:
            if user_id:
                return session.query(User).filter(User.id == user_id).first()
            elif username:
                return session.query(User).filter(User.username == username).first()
            return None
        finally:
            session.close()
    
    # Conversation Management
    
    def create_conversation(
        self,
        user_id: str,
        title: str = None,
        llm_provider: str = None,
        system_prompt: str = None
    ) -> Conversation:
        """Create new conversation."""
        session = self.get_session()
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title,
                llm_provider=llm_provider,
                system_prompt=system_prompt
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation
        finally:
            session.close()
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        session = self.get_session()
        try:
            return session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
        finally:
            session.close()
    
    def list_conversations(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """List user's conversations."""
        session = self.get_session()
        try:
            return session.query(Conversation).filter(
                Conversation.user_id == user_id
            ).order_by(
                Conversation.last_active.desc()
            ).limit(limit).offset(offset).all()
        finally:
            session.close()
    
    def update_conversation_status(
        self,
        conversation_id: str,
        status: str
    ) -> bool:
        """Update conversation status."""
        session = self.get_session()
        try:
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if conversation:
                conversation.status = status
                conversation.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    # Message Management
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        message_type: str = 'interaction',
        metadata: Dict[str, Any] = None,
        add_embedding: bool = True
    ) -> Message:
        """Add message to conversation."""
        session = self.get_session()
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                message_type=message_type,
                metadata=metadata or {}
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            
            # Add to vector database for semantic search
            if add_embedding and len(content) > 10:
                self.vector_db.add_message_embedding(
                    message_id=message.id,
                    content=content,
                    metadata={
                        "conversation_id": conversation_id,
                        "role": role,
                        "message_type": message_type,
                        "timestamp": message.timestamp.isoformat()
                    }
                )
                message.embedding_id = message.id
                session.commit()
            
            # Update conversation stats
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                conversation.total_messages += 1
                conversation.last_active = datetime.utcnow()
                session.commit()
            
            return message
        finally:
            session.close()
    
    def get_messages(
        self,
        conversation_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Message]:
        """Get messages for conversation."""
        session = self.get_session()
        try:
            return session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(
                Message.timestamp.asc()
            ).limit(limit).offset(offset).all()
        finally:
            session.close()
    
    # Memory Segment Management
    
    def add_memory_segment(
        self,
        conversation_id: str,
        summary: str,
        message_ids: List[str],
        tier: str,
        importance_score: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> MemorySegment:
        """Add memory segment."""
        session = self.get_session()
        try:
            # Get timestamps from messages
            messages = session.query(Message).filter(
                Message.id.in_(message_ids)
            ).all()
            
            if not messages:
                raise ValueError("No messages found for segment")
            
            start_timestamp = min(msg.timestamp for msg in messages)
            end_timestamp = max(msg.timestamp for msg in messages)
            
            segment = MemorySegment(
                conversation_id=conversation_id,
                summary=summary,
                message_ids=message_ids,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                tier=tier,
                importance_score=importance_score,
                original_message_count=len(message_ids),
                metadata=metadata or {}
            )
            
            session.add(segment)
            session.commit()
            session.refresh(segment)
            
            # Add to vector database
            self.vector_db.add_memory_segment_embedding(
                segment_id=segment.id,
                summary=summary,
                metadata={
                    "conversation_id": conversation_id,
                    "tier": tier,
                    "importance_score": importance_score,
                    "message_count": len(message_ids)
                }
            )
            
            segment.embedding_id = segment.id
            session.commit()
            
            return segment
        finally:
            session.close()
    
    def get_memory_segments(
        self,
        conversation_id: str,
        tier: str = None
    ) -> List[MemorySegment]:
        """Get memory segments for conversation."""
        session = self.get_session()
        try:
            query = session.query(MemorySegment).filter(
                MemorySegment.conversation_id == conversation_id
            )
            
            if tier:
                query = query.filter(MemorySegment.tier == tier)
            
            return query.order_by(MemorySegment.start_timestamp.desc()).all()
        finally:
            session.close()
    
    # Tool Execution Tracking
    
    def log_tool_execution(
        self,
        conversation_id: str,
        user_id: str,
        tool_name: str,
        action: str,
        parameters: Dict[str, Any],
        result: Dict[str, Any] = None,
        success: bool = False,
        error_message: str = None,
        execution_time_ms: int = None
    ) -> ToolExecution:
        """Log tool execution."""
        session = self.get_session()
        try:
            execution = ToolExecution(
                conversation_id=conversation_id,
                user_id=user_id,
                tool_name=tool_name,
                action=action,
                parameters=parameters,
                result=result or {},
                success=success,
                error_message=error_message,
                execution_time_ms=execution_time_ms,
                completed_at=datetime.utcnow()
            )
            session.add(execution)
            session.commit()
            session.refresh(execution)
            return execution
        finally:
            session.close()
    
    # Checkpoint Management
    
    def create_checkpoint(
        self,
        conversation_id: str,
        iteration_number: int,
        agent_state: str,
        state_snapshot: Dict[str, Any],
        name: str = None,
        is_auto: bool = True
    ) -> Checkpoint:
        """Create conversation checkpoint."""
        session = self.get_session()
        try:
            checkpoint = Checkpoint(
                conversation_id=conversation_id,
                iteration_number=iteration_number,
                agent_state=agent_state,
                state_snapshot=state_snapshot,
                name=name,
                is_auto=is_auto
            )
            session.add(checkpoint)
            session.commit()
            session.refresh(checkpoint)
            return checkpoint
        finally:
            session.close()
    
    # Semantic Search
    
    def semantic_search(
        self,
        query: str,
        conversation_id: str = None,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search across conversations.
        
        Args:
            query: Search query
            conversation_id: Optional conversation filter
            n_results: Number of results
            
        Returns:
            List of search results
        """
        if conversation_id:
            return self.vector_db.search_by_conversation(
                query=query,
                conversation_id=conversation_id,
                n_results=n_results
            )
        else:
            return self.vector_db.semantic_search(
                query=query,
                n_results=n_results
            )
    
    # Analytics and Metrics
    
    def get_conversation_statistics(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """Get detailed conversation statistics."""
        session = self.get_session()
        try:
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                return {}
            
            message_count = session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).count()
            
            segment_count = session.query(MemorySegment).filter(
                MemorySegment.conversation_id == conversation_id
            ).count()
            
            tool_exec_count = session.query(ToolExecution).filter(
                ToolExecution.conversation_id == conversation_id
            ).count()
            
            return {
                "conversation_id": conversation_id,
                "total_messages": message_count,
                "memory_segments": segment_count,
                "tool_executions": tool_exec_count,
                "compression_count": conversation.compression_count,
                "status": conversation.status,
                "created_at": conversation.created_at.isoformat(),
                "last_active": conversation.last_active.isoformat()
            }
        finally:
            session.close()
    
    def cleanup_old_data(self, days: int = 90):
        """Clean up old archived conversations."""
        session = self.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            old_conversations = session.query(Conversation).filter(
                and_(
                    Conversation.status == 'archived',
                    Conversation.last_active < cutoff_date
                )
            ).all()
            
            for conv in old_conversations:
                # Delete associated vector embeddings
                self.vector_db.delete_by_conversation(conv.id)
                
                # Delete conversation (cascade will handle related records)
                session.delete(conv)
            
            session.commit()
            
            return len(old_conversations)
        finally:
            session.close()
