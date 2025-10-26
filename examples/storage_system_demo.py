"""
Sandbox Storage System - Comprehensive Demonstration

This example demonstrates the complete multi-layered storage system for
Graive AI sandboxes, including file system operations, context management,
database usage, media caching, and vector search capabilities.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.storage import (
    SandboxStorageManager,
    StorageTool,
    create_storage_tool_for_sandbox,
    StorageLayer
)


def example_file_system_operations():
    """
    Example 1: File System Layer
    
    Demonstrates persistent file storage within sandbox with UNIX-like operations.
    All files persist for the entire sandbox lifecycle.
    """
    print("=" * 80)
    print("EXAMPLE 1: FILE SYSTEM OPERATIONS")
    print("=" * 80)
    
    # Create storage manager for sandbox
    storage = SandboxStorageManager(
        sandbox_id="demo_sandbox_001",
        base_path="./sandbox_storage"
    )
    
    # Write files
    print("\n1. Writing Files")
    result = storage.write_file(
        file_path="project/research_notes.txt",
        content="Initial research findings on AI in healthcare..."
    )
    print(f"   ✓ Created: {result['file_path']}")
    print(f"   Size: {result['size_bytes']} bytes")
    
    result = storage.write_file(
        file_path="project/data/results.json",
        content='{"accuracy": 0.923, "samples": 10000}'
    )
    print(f"   ✓ Created: {result['file_path']}")
    
    # Append to file
    print("\n2. Appending to File")
    storage.append_file(
        file_path="project/research_notes.txt",
        content="\n\nAdditional findings from literature review..."
    )
    print("   ✓ Appended content")
    
    # Read file
    print("\n3. Reading File")
    result = storage.read_file("project/research_notes.txt")
    if result["success"]:
        print(f"   Content preview: {result['content'][:100]}...")
        print(f"   Size: {result['size_bytes']} bytes")
    
    # List files
    print("\n4. Listing Files")
    result = storage.list_files(directory="project", recursive=True)
    print(f"   Found {result['count']} files:")
    for file_info in result['files']:
        print(f"   - {file_info['path']} ({file_info['size_bytes']} bytes)")
    
    # Storage statistics
    print("\n5. Storage Statistics")
    stats = storage.get_storage_stats()
    print(f"   Total size: {stats['total_size_mb']:.2f} MB")
    print(f"   File system: {stats['layers']['file_system']['file_count']} files")
    
    return storage


def example_context_knowledge_base(storage: SandboxStorageManager):
    """
    Example 2: Context/Knowledge Base Layer
    
    Demonstrates storing and retrieving contextual information for reasoning,
    task planning, conversation history, and execution state.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: CONTEXT/KNOWLEDGE BASE")
    print("=" * 80)
    
    # Store task context
    print("\n1. Storing Task Context")
    storage.store_context(
        key="current_task",
        value={
            "task_id": "generate_thesis",
            "status": "in_progress",
            "progress": 0.35,
            "sections_completed": ["introduction", "literature_review"]
        },
        context_type="task"
    )
    print("   ✓ Stored task context")
    
    # Store conversation history
    storage.store_context(
        key="conversation_summary",
        value="User requested generation of 200,000-word PhD thesis on AI in healthcare",
        context_type="conversation"
    )
    print("   ✓ Stored conversation context")
    
    # Store research findings
    storage.store_context(
        key="key_findings",
        value=[
            "AI improves diagnostic accuracy by 23%",
            "Reduces diagnosis time by 40%",
            "Implementation challenges include data quality"
        ],
        context_type="research"
    )
    print("   ✓ Stored research findings")
    
    # Retrieve context
    print("\n2. Retrieving Context")
    task_info = storage.retrieve_context("current_task")
    print(f"   Current task: {task_info['task_id']}")
    print(f"   Progress: {task_info['progress'] * 100}%")
    print(f"   Completed: {', '.join(task_info['sections_completed'])}")
    
    # Search context
    print("\n3. Searching Context")
    results = storage.search_context("thesis", limit=5)
    print(f"   Found {len(results)} matching contexts:")
    for result in results:
        print(f"   - {result['key']}: {result['type']}")
    
    # List all keys
    print("\n4. Listing Context Keys")
    task_keys = storage.list_context_keys(context_type="task")
    print(f"   Task contexts: {task_keys}")
    
    research_keys = storage.list_context_keys(context_type="research")
    print(f"   Research contexts: {research_keys}")


def example_database_operations(storage: SandboxStorageManager):
    """
    Example 3: Database Scaffold Layer
    
    Demonstrates creating and using structured databases within sandbox for
    data-driven applications and analytics.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: DATABASE OPERATIONS")
    print("=" * 80)
    
    # Create database
    print("\n1. Creating Database")
    result = storage.create_database(
        db_name="research_data",
        db_type="sqlite"
    )
    print(f"   ✓ Created: {result['db_name']}")
    print(f"   Path: {result['db_path']}")
    
    # Create table
    print("\n2. Creating Table")
    result = storage.execute_query(
        db_name="research_data",
        query="""
        CREATE TABLE IF NOT EXISTS patient_data (
            id INTEGER PRIMARY KEY,
            age INTEGER,
            diagnosis VARCHAR(100),
            ai_accuracy REAL,
            traditional_accuracy REAL
        )
        """
    )
    print("   ✓ Created patient_data table")
    
    # Insert data
    print("\n3. Inserting Data")
    sample_data = [
        (45, "Pneumonia", 0.95, 0.78),
        (62, "Heart Disease", 0.92, 0.85),
        (33, "Diabetes", 0.88, 0.82),
        (58, "Cancer", 0.90, 0.75)
    ]
    
    for patient_id, (age, diagnosis, ai_acc, trad_acc) in enumerate(sample_data, 1):
        storage.execute_query(
            db_name="research_data",
            query="""
            INSERT INTO patient_data (id, age, diagnosis, ai_accuracy, traditional_accuracy)
            VALUES (?, ?, ?, ?, ?)
            """,
            params=(patient_id, age, diagnosis, ai_acc, trad_acc)
        )
    print(f"   ✓ Inserted {len(sample_data)} records")
    
    # Query data
    print("\n4. Querying Data")
    result = storage.execute_query(
        db_name="research_data",
        query="""
        SELECT diagnosis, ai_accuracy, traditional_accuracy,
               (ai_accuracy - traditional_accuracy) as improvement
        FROM patient_data
        ORDER BY improvement DESC
        """
    )
    
    if result["success"]:
        print("   Results:")
        print(f"   {'Diagnosis':<20} {'AI Acc':<10} {'Trad Acc':<10} {'Improvement':<12}")
        print("   " + "-" * 60)
        for row in result['rows']:
            print(f"   {row[0]:<20} {row[1]:<10.2f} {row[2]:<10.2f} {row[3]:<12.2f}")
    
    # Aggregate analysis
    print("\n5. Aggregate Analysis")
    result = storage.execute_query(
        db_name="research_data",
        query="""
        SELECT 
            AVG(ai_accuracy) as avg_ai,
            AVG(traditional_accuracy) as avg_traditional,
            AVG(ai_accuracy - traditional_accuracy) as avg_improvement
        FROM patient_data
        """
    )
    
    if result["success"]:
        row = result['rows'][0]
        print(f"   Average AI Accuracy: {row[0]:.2%}")
        print(f"   Average Traditional Accuracy: {row[1]:.2%}")
        print(f"   Average Improvement: {row[2]:.2%}")


def example_media_cache(storage: SandboxStorageManager):
    """
    Example 4: Media Cache Layer
    
    Demonstrates caching generated media files (images, charts, audio, etc.)
    with organized retrieval.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: MEDIA CACHE")
    print("=" * 80)
    
    # Simulate chart generation
    print("\n1. Caching Generated Chart")
    
    # Create simple PNG data (1x1 red pixel as example)
    png_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0'
        b'\x00\x00\x00\x03\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    result = storage.cache_media(
        media_data=png_data,
        media_type="chart",
        filename="accuracy_comparison.png"
    )
    
    if result["success"]:
        print(f"   ✓ Cached chart: {result['media_id'][:16]}...")
        print(f"   Path: {result['path']}")
        print(f"   Size: {result['size_bytes']} bytes")
    
    # Cache multiple images
    print("\n2. Caching Multiple Images")
    for i in range(3):
        result = storage.cache_media(
            media_data=png_data,
            media_type="image",
            filename=f"figure_{i+1}.png"
        )
        print(f"   ✓ Cached: figure_{i+1}.png")
    
    # List cached media
    print("\n3. Listing Cached Media")
    charts = storage.list_cached_media(media_type="chart")
    print(f"   Charts: {len(charts)} files")
    for media in charts:
        print(f"   - {media['filename']} ({media['size_bytes']} bytes)")
    
    images = storage.list_cached_media(media_type="image")
    print(f"   Images: {len(images)} files")
    
    # Retrieve media
    print("\n4. Retrieving Media")
    if charts:
        media_id = charts[0]['media_id']
        retrieved_data = storage.retrieve_media(media_id)
        if retrieved_data:
            print(f"   ✓ Retrieved media: {len(retrieved_data)} bytes")


def example_vector_store(storage: SandboxStorageManager):
    """
    Example 5: Vector Store Layer
    
    Demonstrates semantic embeddings and intelligent retrieval for document
    sections, research findings, and contextual information.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: VECTOR STORE & SEMANTIC SEARCH")
    print("=" * 80)
    
    # Add document embeddings
    print("\n1. Adding Document Embeddings")
    
    document_sections = [
        {
            "id": "intro_001",
            "text": "Artificial intelligence has revolutionized healthcare diagnostics, improving accuracy and reducing time to diagnosis.",
            "metadata": {"section": "introduction", "type": "thesis"}
        },
        {
            "id": "lit_001",
            "text": "Machine learning algorithms demonstrate superior performance in medical image analysis compared to traditional methods.",
            "metadata": {"section": "literature_review", "type": "thesis"}
        },
        {
            "id": "method_001",
            "text": "We employed a retrospective cohort study analyzing electronic health records from 50,000 patients.",
            "metadata": {"section": "methodology", "type": "thesis"}
        },
        {
            "id": "result_001",
            "text": "AI-assisted diagnosis achieved 92.3% accuracy compared to 78.5% for traditional approaches, representing a 13.8% improvement.",
            "metadata": {"section": "results", "type": "thesis"}
        }
    ]
    
    for doc in document_sections:
        result = storage.add_embedding(
            text=doc["text"],
            metadata=doc["metadata"],
            embedding_id=doc["id"]
        )
        if result["success"]:
            print(f"   ✓ Added: {doc['metadata']['section']}")
    
    # Semantic search
    print("\n2. Semantic Search Queries")
    
    # Search for accuracy information
    print("\n   Query: 'diagnostic accuracy comparison'")
    results = storage.semantic_search(
        query="diagnostic accuracy comparison",
        n_results=2
    )
    for i, result in enumerate(results, 1):
        print(f"   Result {i}:")
        print(f"   - Text: {result['text'][:100]}...")
        print(f"   - Section: {result['metadata'].get('section', 'unknown')}")
        print(f"   - Similarity: {result['similarity']:.3f}")
    
    # Search for methodology
    print("\n   Query: 'research methodology patient data'")
    results = storage.semantic_search(
        query="research methodology patient data",
        n_results=2
    )
    for i, result in enumerate(results, 1):
        print(f"   Result {i}:")
        print(f"   - Text: {result['text'][:100]}...")
        print(f"   - Section: {result['metadata'].get('section', 'unknown')}")


def example_integrated_workflow():
    """
    Example 6: Integrated Workflow
    
    Demonstrates using multiple storage layers together in a realistic
    document generation workflow.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 6: INTEGRATED DOCUMENT GENERATION WORKFLOW")
    print("=" * 80)
    
    # Create storage for thesis project
    storage = SandboxStorageManager(
        sandbox_id="thesis_project_001",
        base_path="./sandbox_storage"
    )
    
    print("\n1. Initialize Project Context")
    storage.store_context(
        key="project_info",
        value={
            "title": "AI in Healthcare Diagnostics",
            "word_count_target": 200000,
            "sections": ["intro", "lit_review", "methods", "results", "discussion"]
        },
        context_type="project"
    )
    print("   ✓ Project context stored")
    
    print("\n2. Create Research Database")
    storage.create_database("research_citations")
    storage.execute_query(
        db_name="research_citations",
        query="""
        CREATE TABLE citations (
            id INTEGER PRIMARY KEY,
            author TEXT,
            year INTEGER,
            title TEXT,
            journal TEXT
        )
        """
    )
    
    # Add citations
    citations = [
        ("Smith et al.", 2023, "Deep Learning in Medical Imaging", "Nature Medicine"),
        ("Jones et al.", 2024, "AI-Assisted Diagnosis Systems", "JAMA"),
        ("Brown et al.", 2023, "Clinical AI Applications", "Lancet")
    ]
    
    for author, year, title, journal in citations:
        storage.execute_query(
            db_name="research_citations",
            query="INSERT INTO citations (author, year, title, journal) VALUES (?, ?, ?, ?)",
            params=(author, year, title, journal)
        )
    print(f"   ✓ Added {len(citations)} citations to database")
    
    print("\n3. Save Generated Sections as Files")
    sections = {
        "introduction.md": "# Introduction\n\nThis thesis explores...",
        "literature_review.md": "# Literature Review\n\nExisting research shows...",
        "results/data_analysis.py": "import pandas as pd\n# Analysis code..."
    }
    
    for path, content in sections.items():
        storage.write_file(path, content)
        print(f"   ✓ Saved: {path}")
    
    print("\n4. Cache Generated Visualizations")
    png_data = b'\x89PNG\r\n\x1a\n...'  # Simulated PNG
    storage.cache_media(png_data, "chart", "accuracy_chart.png")
    storage.cache_media(png_data, "chart", "timeline_figure.png")
    print("   ✓ Cached 2 visualizations")
    
    print("\n5. Add Sections to Vector Store for Search")
    storage.add_embedding(
        text="Introduction section discussing AI improvements",
        metadata={"section": "introduction", "status": "complete"}
    )
    storage.add_embedding(
        text="Literature review synthesizing 50 research papers",
        metadata={"section": "literature_review", "status": "complete"}
    )
    print("   ✓ Added sections to vector store")
    
    print("\n6. Get Project Statistics")
    stats = storage.get_storage_stats()
    print(f"   Total storage used: {stats['total_size_mb']:.2f} MB")
    print(f"   Files: {stats['layers']['file_system']['file_count']}")
    print(f"   Context entries: {stats['layers']['context']['entry_count']}")
    print(f"   Cached media: {stats['layers']['media_cache']['file_count']}")
    
    print("\n7. Export Complete Sandbox")
    result = storage.export_sandbox("./exports/thesis_project_001")
    if result["success"]:
        print(f"   ✓ Exported to: {result['archive_path']}")
        print(f"   Archive size: {result['size_bytes'] / (1024*1024):.2f} MB")
    
    storage.cleanup()


def example_storage_tool_usage():
    """
    Example 7: Using Storage Tool Interface
    
    Demonstrates high-level storage tool for easy integration with agent systems.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 7: STORAGE TOOL INTERFACE")
    print("=" * 80)
    
    # Create storage tool
    tool = create_storage_tool_for_sandbox(
        sandbox_id="tool_demo_001",
        base_path="./sandbox_storage"
    )
    
    print("\n1. Available Actions")
    actions = tool.get_available_actions()
    print(f"   Total actions: {len(actions)}")
    print(f"   File operations: {[a for a in actions if 'file' in a]}")
    print(f"   Context operations: {[a for a in actions if 'context' in a]}")
    
    print("\n2. Execute File Operations")
    result = tool.execute(
        "write_file",
        file_path="demo.txt",
        content="Hello from storage tool!"
    )
    print(f"   ✓ Write result: {result['success']}")
    
    result = tool.execute(
        "read_file",
        file_path="demo.txt"
    )
    print(f"   ✓ Read content: {result['content']}")
    
    print("\n3. Execute Context Operations")
    result = tool.execute(
        "store_context",
        key="demo_data",
        value={"status": "active", "count": 42}
    )
    print(f"   ✓ Stored context: {result['success']}")
    
    result = tool.execute(
        "retrieve_context",
        key="demo_data"
    )
    print(f"   ✓ Retrieved: {result['value']}")
    
    print("\n4. Get Storage Statistics")
    result = tool.execute("get_storage_stats")
    if result["success"]:
        stats = result["stats"]
        print(f"   Total size: {stats['total_size_mb']:.2f} MB")


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" GRAIVE AI - MULTI-LAYERED SANDBOX STORAGE SYSTEM")
    print("=" * 80)
    print("\nComprehensive demonstration of persistent data storage across all layers:")
    print("  1. File System (UNIX-like persistent storage)")
    print("  2. Context/Knowledge Base (reasoning state)")
    print("  3. Database Scaffold (structured data)")
    print("  4. Media Cache (images, charts, audio)")
    print("  5. Vector Store (semantic search)")
    print("\n" + "=" * 80)
    
    # Run examples
    storage = example_file_system_operations()
    example_context_knowledge_base(storage)
    example_database_operations(storage)
    example_media_cache(storage)
    example_vector_store(storage)
    
    # Clean up
    storage.cleanup()
    
    # Integrated workflow
    example_integrated_workflow()
    
    # Storage tool
    example_storage_tool_usage()
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nThe sandbox storage system provides:")
    print("  ✓ Persistent file storage for entire sandbox lifecycle")
    print("  ✓ Context/knowledge management for reasoning and state")
    print("  ✓ Structured databases for data-driven applications")
    print("  ✓ Organized media caching for generated content")
    print("  ✓ Vector embeddings for semantic search and retrieval")
    print("  ✓ Unified tool interface for easy agent integration")
    print("\nAll data persists across sessions, supporting long-running projects!")
    print("=" * 80)
