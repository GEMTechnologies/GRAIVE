"""
Database Schema for Graive AI Platform

This module defines the complete database schema for the Graive AI system, including
tables for conversations, memory segments, tool executions, user preferences, and
vector embeddings for semantic search. The schema supports infinite memory management,
conversation tracking, and efficient retrieval of historical context.

Recommended Database: PostgreSQL 15+ with pgvector extension
Alternative: SQLite for development, PostgreSQL for production
Vector Store: ChromaDB for semantic embeddings and similarity search
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, 
    Float, Boolean, JSON, ForeignKey, Index, BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    """
    User account information and preferences.
    
    Stores user credentials, preferences, API keys, and configuration settings.
    Each user can have multiple conversations and custom tool configurations.
    """
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User preferences and settings
    preferences = Column(JSONB, default={})
    api_keys = Column(JSONB, default={})  # Encrypted in production
    interaction_mode = Column(String(50), default='interruptible')
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    tool_executions = relationship("ToolExecution", back_populates="user")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
    )


class Conversation(Base):
    """
    Conversation sessions between user and agent.
    
    Each conversation represents a complete interaction session with the agent,
    containing multiple messages, tool executions, and memory segments. Conversations
    support pause/resume and can span multiple sessions with complete state restoration.
    """
    __tablename__ = 'conversations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    session_id = Column(String(36), unique=True, nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # State tracking
    status = Column(String(50), default='active')  # active, paused, completed, archived
    total_messages = Column(Integer, default=0)
    total_tokens = Column(BigInteger, default=0)
    compression_count = Column(Integer, default=0)
    
    # Configuration
    llm_provider = Column(String(50))
    llm_model = Column(String(100))
    system_prompt = Column(Text)
    
    # Metadata
    meta_data = Column(JSONB, default={})
    tags = Column(ARRAY(String), default=[])
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    memory_segments = relationship("MemorySegment", back_populates="conversation", cascade="all, delete-orphan")
    tool_executions = relationship("ToolExecution", back_populates="conversation")
    checkpoints = relationship("Checkpoint", back_populates="conversation", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_conv_user_id', 'user_id'),
        Index('idx_conv_session_id', 'session_id'),
        Index('idx_conv_status', 'status'),
        Index('idx_conv_last_active', 'last_active'),
    )


class Message(Base):
    """
    Individual messages within conversations.
    
    Stores all messages exchanged between user and agent, including system messages,
    observations, and tool results. Messages support full-text search and are linked
    to vector embeddings for semantic retrieval.
    """
    __tablename__ = 'messages'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Message content
    role = Column(String(50), nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Message metadata
    token_count = Column(Integer, default=0)
    importance_score = Column(Float, default=0.5)
    message_type = Column(String(50), default='interaction')  # interaction, observation, error, feedback
    
    # Vector embedding reference
    embedding_id = Column(String(36), index=True)
    
    # Tool execution reference
    tool_execution_id = Column(String(36), ForeignKey('tool_executions.id'), nullable=True)
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    tool_execution = relationship("ToolExecution", back_populates="messages")
    
    # Indexes
    __table_args__ = (
        Index('idx_msg_conversation', 'conversation_id'),
        Index('idx_msg_timestamp', 'timestamp'),
        Index('idx_msg_role', 'role'),
        Index('idx_msg_embedding', 'embedding_id'),
    )


class MemorySegment(Base):
    """
    Compressed memory segments for infinite context management.
    
    Represents compressed groups of messages with intelligent summaries. Memory segments
    form the backbone of the infinite memory system, allowing conversations to scale
    beyond token limits while preserving all critical information.
    """
    __tablename__ = 'memory_segments'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Segment content
    summary = Column(Text, nullable=False)
    message_ids = Column(ARRAY(String), default=[])
    start_timestamp = Column(DateTime, nullable=False)
    end_timestamp = Column(DateTime, nullable=False)
    
    # Segment metadata
    tier = Column(String(50), nullable=False)  # working, short_term, long_term
    importance_score = Column(Float, default=0.5)
    access_count = Column(Integer, default=0)
    compression_level = Column(Integer, default=1)  # 1 = first compression, 2+ = hierarchical
    
    # Vector embedding reference
    embedding_id = Column(String(36), index=True)
    
    # Statistics
    original_message_count = Column(Integer, default=0)
    original_token_count = Column(Integer, default=0)
    compressed_token_count = Column(Integer, default=0)
    compression_ratio = Column(Float, default=1.0)
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", back_populates="memory_segments")
    
    # Indexes
    __table_args__ = (
        Index('idx_memseg_conversation', 'conversation_id'),
        Index('idx_memseg_tier', 'tier'),
        Index('idx_memseg_importance', 'importance_score'),
        Index('idx_memseg_timestamp', 'start_timestamp', 'end_timestamp'),
    )


class ToolExecution(Base):
    """
    Record of all tool executions within the system.
    
    Tracks every tool invocation including parameters, results, execution time,
    and success status. This provides complete audit trail and enables learning
    from historical tool usage patterns.
    """
    __tablename__ = 'tool_executions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    
    # Tool information
    tool_name = Column(String(100), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    parameters = Column(JSONB, default={})
    
    # Execution details
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    execution_time_ms = Column(Integer)
    
    # Results
    success = Column(Boolean, default=False)
    result = Column(JSONB, default={})
    error_message = Column(Text)
    
    # Context
    iteration_number = Column(Integer)
    agent_state = Column(String(50))
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", back_populates="tool_executions")
    user = relationship("User", back_populates="tool_executions")
    messages = relationship("Message", back_populates="tool_execution")
    
    # Indexes
    __table_args__ = (
        Index('idx_tool_conversation', 'conversation_id'),
        Index('idx_tool_name', 'tool_name'),
        Index('idx_tool_timestamp', 'started_at'),
        Index('idx_tool_success', 'success'),
    )


class Checkpoint(Base):
    """
    Conversation state checkpoints for rollback and recovery.
    
    Stores complete conversation state at specific points, enabling rollback to
    previous states and recovery from errors or unwanted execution paths.
    """
    __tablename__ = 'checkpoints'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Checkpoint metadata
    name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # State snapshot
    iteration_number = Column(Integer, nullable=False)
    agent_state = Column(String(50))
    message_count = Column(Integer, default=0)
    
    # Complete state (serialized)
    state_snapshot = Column(JSONB, default={})
    context_summary = Column(Text)
    
    # Metadata
    is_auto = Column(Boolean, default=True)  # Auto vs manual checkpoint
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", back_populates="checkpoints")
    
    # Indexes
    __table_args__ = (
        Index('idx_checkpoint_conversation', 'conversation_id'),
        Index('idx_checkpoint_created', 'created_at'),
    )


class VectorEmbedding(Base):
    """
    Vector embeddings for semantic search and retrieval.
    
    Stores vector representations of messages and memory segments, enabling
    semantic search across conversation history. Embeddings are generated using
    sentence transformers or OpenAI's embedding API.
    """
    __tablename__ = 'vector_embeddings'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Source reference
    source_type = Column(String(50), nullable=False)  # message, memory_segment, document
    source_id = Column(String(36), nullable=False, index=True)
    
    # Embedding data
    model_name = Column(String(100), nullable=False)
    embedding_dimension = Column(Integer, nullable=False)
    # Vector stored in separate vector database (ChromaDB/pgvector)
    
    # Text content (for reference)
    text_content = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    meta_data = Column(JSONB, default={})
    
    # Indexes
    __table_args__ = (
        Index('idx_embedding_source', 'source_type', 'source_id'),
    )


class Document(Base):
    """
    Documents created or processed by the system.
    
    Tracks all documents generated or analyzed by Graive, including their location,
    format, and associated metadata. Supports full document lifecycle management.
    """
    __tablename__ = 'documents'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=True, index=True)
    
    # Document information
    filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    format = Column(String(50), nullable=False)  # md, docx, pptx, pdf, etc.
    
    # Content metadata
    file_size = Column(BigInteger)
    page_count = Column(Integer)
    word_count = Column(Integer)
    
    # Operations
    operation = Column(String(50))  # created, read, converted, analyzed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Vector embedding reference
    embedding_id = Column(String(36), index=True)
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", foreign_keys=[conversation_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_doc_conversation', 'conversation_id'),
        Index('idx_doc_format', 'format'),
        Index('idx_doc_created', 'created_at'),
    )


class InteractionEvent(Base):
    """
    User interaction events for human-in-the-loop tracking.
    
    Records all user interruptions, modifications, and feedback during agent execution.
    Enables analysis of interaction patterns and improvement of collaborative features.
    """
    __tablename__ = 'interaction_events'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # pause, continue, modify, feedback, stop
    event_data = Column(JSONB, default={})
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Context
    iteration_number = Column(Integer)
    agent_state = Column(String(50))
    
    # Impact
    goal_modified = Column(Boolean, default=False)
    execution_paused = Column(Boolean, default=False)
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", foreign_keys=[conversation_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_event_conversation', 'conversation_id'),
        Index('idx_event_type', 'event_type'),
        Index('idx_event_timestamp', 'timestamp'),
    )


class AgentMetrics(Base):
    """
    Performance metrics and analytics for agent operations.
    
    Tracks execution performance, resource usage, success rates, and other metrics
    to enable monitoring, optimization, and performance analysis.
    """
    __tablename__ = 'agent_metrics'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=True, index=True)
    
    # Metric information
    metric_type = Column(String(100), nullable=False, index=True)
    metric_name = Column(String(200), nullable=False)
    metric_value = Column(Float, nullable=False)
    
    # Context
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Aggregation
    aggregation_period = Column(String(50))  # hourly, daily, weekly
    
    # Metadata
    meta_data = Column(JSONB, default={})
    
    # Relationships
    conversation = relationship("Conversation", foreign_keys=[conversation_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_type', 'metric_type'),
        Index('idx_metrics_timestamp', 'timestamp'),
    )


# Additional indexes for performance optimization
Index('idx_messages_fulltext', Message.content, postgresql_using='gin')
Index('idx_memory_fulltext', MemorySegment.summary, postgresql_using='gin')
