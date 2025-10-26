"""
Database Setup and Usage Example

This example demonstrates how to set up and use the Graive AI database system,
including PostgreSQL with vector support and ChromaDB integration.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.database_manager import DatabaseManager
from src.database.schema import Base
from sqlalchemy import create_engine


def setup_database_demo():
    """Demonstrate database setup and basic operations."""
    print("\n" + "="*70)
    print("DATABASE SETUP DEMO")
    print("="*70)
    
    # Initialize database manager
    # For production: use PostgreSQL
    # db_url = "postgresql://user:password@localhost/graive"
    
    # For demo: use SQLite
    db_url = "sqlite:///./graive_demo.db"
    
    print(f"\n[Setup] Initializing database: {db_url}")
    
    db_manager = DatabaseManager(
        db_url=db_url,
        vector_db_path="./demo_chroma_db"
    )
    
    print("[Setup] Database initialized successfully!")
    
    return db_manager


def demo_user_creation(db_manager):
    """Demonstrate user creation."""
    print("\n[Demo] Creating user...")
    
    user = db_manager.create_user(
        username="demo_user",
        email="demo@example.com",
        preferences={
            "interaction_mode": "interruptible",
            "default_llm": "openai"
        }
    )
    
    print(f"[Demo] User created: {user.username} (ID: {user.id})")
    return user


def demo_conversation_flow(db_manager, user_id):
    """Demonstrate complete conversation flow."""
    print("\n[Demo] Creating conversation...")
    
    # Create conversation
    conversation = db_manager.create_conversation(
        user_id=user_id,
        title="AI Research Discussion",
        llm_provider="openai",
        system_prompt="You are a helpful AI research assistant."
    )
    
    print(f"[Demo] Conversation created: {conversation.id}")
    
    # Add messages
    print("\n[Demo] Adding messages...")
    
    msg1 = db_manager.add_message(
        conversation_id=conversation.id,
        role="user",
        content="What are the latest developments in large language models?",
        add_embedding=True
    )
    print(f"  Added message 1 (embedding: {msg1.embedding_id is not None})")
    
    msg2 = db_manager.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content="Recent developments in large language models include improved reasoning "
               "capabilities, better instruction following, and enhanced context windows. "
               "Models like GPT-4 and Claude 3 demonstrate significant advances in complex "
               "task completion and multi-step reasoning.",
        add_embedding=True
    )
    print(f"  Added message 2 (embedding: {msg2.embedding_id is not None})")
    
    msg3 = db_manager.add_message(
        conversation_id=conversation.id,
        role="user",
        content="Tell me more about context window improvements",
        add_embedding=True
    )
    print(f"  Added message 3 (embedding: {msg3.embedding_id is not None})")
    
    # Add more messages to demonstrate memory compression
    for i in range(10):
        db_manager.add_message(
            conversation_id=conversation.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Sample message {i} about AI and machine learning topics",
            add_embedding=True
        )
    
    print(f"[Demo] Added 13 total messages")
    
    return conversation


def demo_memory_segments(db_manager, conversation_id):
    """Demonstrate memory segment creation."""
    print("\n[Demo] Creating memory segment...")
    
    # Get some messages to compress
    messages = db_manager.get_messages(conversation_id, limit=5)
    message_ids = [msg.id for msg in messages]
    
    segment = db_manager.add_memory_segment(
        conversation_id=conversation_id,
        summary="Discussion about large language models and recent improvements in "
               "context windows, reasoning capabilities, and instruction following.",
        message_ids=message_ids,
        tier="short_term",
        importance_score=0.8
    )
    
    print(f"[Demo] Memory segment created: {segment.id}")
    print(f"  Tier: {segment.tier}")
    print(f"  Messages compressed: {len(message_ids)}")
    print(f"  Importance score: {segment.importance_score}")
    
    return segment


def demo_tool_execution_logging(db_manager, conversation_id, user_id):
    """Demonstrate tool execution logging."""
    print("\n[Demo] Logging tool execution...")
    
    execution = db_manager.log_tool_execution(
        conversation_id=conversation_id,
        user_id=user_id,
        tool_name="document",
        action="create",
        parameters={
            "format": "markdown",
            "filename": "research_notes.md",
            "content": {"title": "LLM Research Notes"}
        },
        result={
            "success": True,
            "file_path": "/path/to/research_notes.md"
        },
        success=True,
        execution_time_ms=150
    )
    
    print(f"[Demo] Tool execution logged: {execution.id}")
    print(f"  Tool: {execution.tool_name}")
    print(f"  Action: {execution.action}")
    print(f"  Success: {execution.success}")
    print(f"  Execution time: {execution.execution_time_ms}ms")


def demo_semantic_search(db_manager, conversation_id):
    """Demonstrate semantic search capabilities."""
    print("\n[Demo] Performing semantic search...")
    
    # Search for content related to context windows
    results = db_manager.semantic_search(
        query="How have context windows improved in recent models?",
        conversation_id=conversation_id,
        n_results=3
    )
    
    print(f"[Demo] Found {len(results)} relevant results:")
    for i, result in enumerate(results):
        print(f"\n  Result {i+1}:")
        print(f"    Content: {result['content'][:100]}...")
        print(f"    Source: {result['metadata'].get('source_type')}")
        print(f"    Role: {result['metadata'].get('role')}")


def demo_checkpoint_creation(db_manager, conversation_id):
    """Demonstrate checkpoint creation."""
    print("\n[Demo] Creating checkpoint...")
    
    checkpoint = db_manager.create_checkpoint(
        conversation_id=conversation_id,
        iteration_number=10,
        agent_state="thinking",
        state_snapshot={
            "current_task": "research",
            "progress": "50%",
            "next_action": "analyze"
        },
        name="Research Midpoint",
        is_auto=False
    )
    
    print(f"[Demo] Checkpoint created: {checkpoint.id}")
    print(f"  Name: {checkpoint.name}")
    print(f"  Iteration: {checkpoint.iteration_number}")


def demo_conversation_statistics(db_manager, conversation_id):
    """Demonstrate conversation statistics retrieval."""
    print("\n[Demo] Getting conversation statistics...")
    
    stats = db_manager.get_conversation_statistics(conversation_id)
    
    print(f"[Demo] Conversation Statistics:")
    print(f"  Total messages: {stats['total_messages']}")
    print(f"  Memory segments: {stats['memory_segments']}")
    print(f"  Tool executions: {stats['tool_executions']}")
    print(f"  Status: {stats['status']}")
    print(f"  Created: {stats['created_at']}")


def main():
    """Run complete database demonstration."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*17 + "GRAIVE AI - DATABASE DEMO" + " "*27 + "║")
    print("║" + " "*10 + "PostgreSQL + ChromaDB Integration" + " "*23 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Setup database
    db_manager = setup_database_demo()
    
    # Create user
    user = demo_user_creation(db_manager)
    
    # Demonstrate conversation flow
    conversation = demo_conversation_flow(db_manager, user.id)
    
    # Demonstrate memory segments
    demo_memory_segments(db_manager, conversation.id)
    
    # Demonstrate tool execution logging
    demo_tool_execution_logging(db_manager, conversation.id, user.id)
    
    # Demonstrate semantic search
    demo_semantic_search(db_manager, conversation.id)
    
    # Demonstrate checkpoint creation
    demo_checkpoint_creation(db_manager, conversation.id)
    
    # Show statistics
    demo_conversation_statistics(db_manager, conversation.id)
    
    print("\n" + "="*70)
    print("DATABASE DEMO COMPLETE")
    print("="*70)
    
    print("\nKey Features Demonstrated:")
    print("  ✓ User management")
    print("  ✓ Conversation tracking")
    print("  ✓ Message storage with embeddings")
    print("  ✓ Memory segment compression")
    print("  ✓ Tool execution logging")
    print("  ✓ Semantic search (ChromaDB)")
    print("  ✓ Checkpoint creation")
    print("  ✓ Statistics and analytics")
    
    print("\nDatabase Files Created:")
    print("  • graive_demo.db (SQLite)")
    print("  • demo_chroma_db/ (ChromaDB vector store)")
    
    print("\nFor Production:")
    print("  Use PostgreSQL: postgresql://user:password@localhost/graive")
    print("  Install: pip install psycopg2-binary sqlalchemy chromadb")
    print()


if __name__ == "__main__":
    main()
