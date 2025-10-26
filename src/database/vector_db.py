"""
Vector Database Integration for Semantic Search

This module provides integration with ChromaDB for vector embeddings and semantic search.
ChromaDB is specifically designed for AI applications and provides excellent performance
for similarity search, making it ideal for the infinite memory system.

Why ChromaDB:
- Purpose-built for AI applications
- Excellent performance for similarity search
- Simple API and easy integration
- Supports metadata filtering
- Persistent storage
- Open source and production-ready

Alternative: PostgreSQL with pgvector extension for unified storage
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import numpy as np
from typing import List, Dict, Any, Optional
import os


class VectorDatabase:
    """
    Vector database manager for semantic search and embeddings.
    
    This class provides high-level interface to ChromaDB for storing and retrieving
    vector embeddings of messages, memory segments, and documents. It enables semantic
    search across unlimited conversation history, finding relevant context based on
    meaning rather than exact text matching.
    """
    
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "graive_embeddings",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize vector database.
        
        Args:
            persist_directory: Directory for persistent storage
            collection_name: Name of the collection
            embedding_model: Model for generating embeddings
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client with new API
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "Graive AI conversation embeddings"}
        )
        
        print(f"[VectorDB] Initialized with {self.collection.count()} embeddings")
    
    def add_message_embedding(
        self,
        message_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Add message embedding to vector database.
        
        Args:
            message_id: Unique message identifier
            content: Message text content
            metadata: Additional metadata
            
        Returns:
            Embedding ID
        """
        self.collection.add(
            documents=[content],
            ids=[message_id],
            metadatas=[{
                **metadata,
                "source_type": "message",
                "source_id": message_id
            }]
        )
        
        return message_id
    
    def add_memory_segment_embedding(
        self,
        segment_id: str,
        summary: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Add memory segment embedding to vector database.
        
        Args:
            segment_id: Unique segment identifier
            summary: Segment summary text
            metadata: Additional metadata
            
        Returns:
            Embedding ID
        """
        self.collection.add(
            documents=[summary],
            ids=[segment_id],
            metadatas=[{
                **metadata,
                "source_type": "memory_segment",
                "source_id": segment_id
            }]
        )
        
        return segment_id
    
    def add_document_embedding(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Add document embedding to vector database.
        
        Args:
            document_id: Unique document identifier
            content: Document text content
            metadata: Additional metadata
            
        Returns:
            Embedding ID
        """
        self.collection.add(
            documents=[content],
            ids=[document_id],
            metadatas=[{
                **metadata,
                "source_type": "document",
                "source_id": document_id
            }]
        )
        
        return document_id
    
    def semantic_search(
        self,
        query: str,
        n_results: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search across all embeddings.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of search results with content and metadata
        """
        where_filter = filter_metadata if filter_metadata else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        # Format results
        formatted_results = []
        
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def search_by_conversation(
        self,
        query: str,
        conversation_id: str,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search within specific conversation.
        
        Args:
            query: Search query text
            conversation_id: Conversation to search within
            n_results: Number of results
            
        Returns:
            List of search results
        """
        return self.semantic_search(
            query=query,
            n_results=n_results,
            filter_metadata={"conversation_id": conversation_id}
        )
    
    def search_by_source_type(
        self,
        query: str,
        source_type: str,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search specific source type (messages, memory_segments, documents).
        
        Args:
            query: Search query text
            source_type: Type of source to search
            n_results: Number of results
            
        Returns:
            List of search results
        """
        return self.semantic_search(
            query=query,
            n_results=n_results,
            filter_metadata={"source_type": source_type}
        )
    
    def get_by_id(self, embedding_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific embedding by ID.
        
        Args:
            embedding_id: Embedding identifier
            
        Returns:
            Embedding data or None
        """
        result = self.collection.get(ids=[embedding_id])
        
        if result['ids']:
            return {
                "id": result['ids'][0],
                "content": result['documents'][0],
                "metadata": result['metadatas'][0]
            }
        
        return None
    
    def delete_embedding(self, embedding_id: str) -> bool:
        """
        Delete embedding by ID.
        
        Args:
            embedding_id: Embedding identifier
            
        Returns:
            Success status
        """
        try:
            self.collection.delete(ids=[embedding_id])
            return True
        except Exception as e:
            print(f"[VectorDB] Delete error: {e}")
            return False
    
    def delete_by_conversation(self, conversation_id: str) -> int:
        """
        Delete all embeddings for a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Number of embeddings deleted
        """
        try:
            # Get all embeddings for conversation
            results = self.collection.get(
                where={"conversation_id": conversation_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                return len(results['ids'])
            
            return 0
        except Exception as e:
            print(f"[VectorDB] Delete conversation error: {e}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get vector database statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_embeddings": self.collection.count(),
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory
        }
    
    def persist(self):
        """Persist current state to disk."""
        self.client.persist()
        print(f"[VectorDB] Persisted {self.collection.count()} embeddings")


class PgVectorDatabase:
    """
    Alternative PostgreSQL pgvector implementation.
    
    This provides vector search capabilities within PostgreSQL using the pgvector
    extension. Useful when you want unified storage in a single database system.
    
    Note: Requires PostgreSQL 15+ with pgvector extension installed
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize pgvector database.
        
        Args:
            connection_string: PostgreSQL connection string
        """
        from sqlalchemy import create_engine, text
        
        self.engine = create_engine(connection_string)
        
        # Enable pgvector extension
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        
        print("[PgVector] Initialized PostgreSQL vector database")
    
    def add_embedding(
        self,
        embedding_id: str,
        vector: List[float],
        source_type: str,
        source_id: str,
        content: str,
        metadata: Dict[str, Any]
    ):
        """
        Add vector embedding to PostgreSQL.
        
        Args:
            embedding_id: Unique identifier
            vector: Embedding vector
            source_type: Type of source
            source_id: Source identifier
            content: Text content
            metadata: Additional metadata
        """
        from sqlalchemy import text
        import json
        
        vector_str = '[' + ','.join(map(str, vector)) + ']'
        
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO vector_embeddings_pgvector 
                    (id, vector, source_type, source_id, content, metadata)
                    VALUES (:id, :vector::vector, :source_type, :source_id, :content, :metadata)
                    ON CONFLICT (id) DO UPDATE 
                    SET vector = EXCLUDED.vector,
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata
                """),
                {
                    "id": embedding_id,
                    "vector": vector_str,
                    "source_type": source_type,
                    "source_id": source_id,
                    "content": content,
                    "metadata": json.dumps(metadata)
                }
            )
            conn.commit()
    
    def semantic_search(
        self,
        query_vector: List[float],
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using cosine similarity.
        
        Args:
            query_vector: Query embedding vector
            n_results: Number of results
            
        Returns:
            List of search results
        """
        from sqlalchemy import text
        
        vector_str = '[' + ','.join(map(str, query_vector)) + ']'
        
        with self.engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT id, source_type, source_id, content, metadata,
                           1 - (vector <=> :query_vector::vector) as similarity
                    FROM vector_embeddings_pgvector
                    ORDER BY vector <=> :query_vector::vector
                    LIMIT :limit
                """),
                {"query_vector": vector_str, "limit": n_results}
            )
            
            return [
                {
                    "id": row[0],
                    "source_type": row[1],
                    "source_id": row[2],
                    "content": row[3],
                    "metadata": row[4],
                    "similarity": row[5]
                }
                for row in result
            ]
