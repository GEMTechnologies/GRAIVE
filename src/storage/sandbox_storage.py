"""
Sandbox Storage Manager - Multi-layered Persistence System

This module implements a comprehensive data storage and retrieval system for Graive AI
sandboxes, providing persistent file system access, structured database management,
context/knowledge base storage, and media caching capabilities.

Each sandbox functions as a stateful environment where all data persists for the
entire lifecycle, supporting long-running projects like document generation,
data analysis, and application development.
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import os
import json
import sqlite3
import shutil
from datetime import datetime
from enum import Enum
import pickle
import hashlib


class StorageLayer(Enum):
    """Storage layers available in sandbox."""
    FILE_SYSTEM = "file_system"
    CONTEXT_KNOWLEDGE = "context_knowledge"
    DATABASE = "database"
    MEDIA_CACHE = "media_cache"
    VECTOR_STORE = "vector_store"


class SandboxStorageManager:
    """
    Multi-layered storage manager for sandbox environments.
    
    Provides unified interface for:
    - File system operations (persistent UNIX-like storage)
    - Context/knowledge base (in-memory JSON with persistence)
    - Database scaffolds (SQLite, PostgreSQL, MySQL)
    - Media cache (images, charts, audio, presentations)
    - Vector embeddings for semantic search
    """
    
    def __init__(
        self,
        sandbox_id: str,
        base_path: str,
        enable_database: bool = True,
        enable_vector_store: bool = True
    ):
        """
        Initialize sandbox storage manager.
        
        Args:
            sandbox_id: Unique identifier for this sandbox
            base_path: Base directory for sandbox storage
            enable_database: Whether to initialize database support
            enable_vector_store: Whether to enable vector embeddings
        """
        self.sandbox_id = sandbox_id
        self.base_path = Path(base_path)
        
        # Create sandbox directory structure
        self.sandbox_root = self.base_path / f"sandbox_{sandbox_id}"
        self.file_system_root = self.sandbox_root / "filesystem"
        self.context_store_path = self.sandbox_root / "context"
        self.database_path = self.sandbox_root / "databases"
        self.media_cache_path = self.sandbox_root / "media"
        self.vector_store_path = self.sandbox_root / "vectors"
        
        # Initialize directory structure
        self._initialize_directories()
        
        # Initialize context/knowledge base
        self.context_db = ContextKnowledgeBase(self.context_store_path)
        
        # Initialize database scaffold
        self.database_manager = None
        if enable_database:
            self.database_manager = DatabaseScaffold(self.database_path)
        
        # Initialize media cache
        self.media_cache = MediaCache(self.media_cache_path)
        
        # Initialize vector store
        self.vector_store = None
        if enable_vector_store:
            from src.database.vector_db import VectorDatabase
            self.vector_store = VectorDatabase(
                persist_directory=str(self.vector_store_path)
            )
        
        # Storage metadata
        self.metadata = {
            "sandbox_id": sandbox_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            "storage_layers": [layer.value for layer in StorageLayer]
        }
        
        self._save_metadata()
    
    def _initialize_directories(self):
        """Create sandbox directory structure."""
        for directory in [
            self.sandbox_root,
            self.file_system_root,
            self.context_store_path,
            self.database_path,
            self.media_cache_path,
            self.vector_store_path
        ]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _save_metadata(self):
        """Save sandbox metadata."""
        metadata_path = self.sandbox_root / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _update_access_time(self):
        """Update last access timestamp."""
        self.metadata["last_accessed"] = datetime.utcnow().isoformat()
        self._save_metadata()
    
    # ==================== FILE SYSTEM LAYER ====================
    
    def write_file(
        self,
        file_path: str,
        content: Union[str, bytes],
        encoding: str = 'utf-8'
    ) -> Dict[str, Any]:
        """
        Write file to sandbox file system.
        
        Args:
            file_path: Relative path within sandbox
            content: File content (string or bytes)
            encoding: Encoding for text files
        
        Returns:
            Operation result with file metadata
        """
        full_path = self.file_system_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        mode = 'wb' if isinstance(content, bytes) else 'w'
        
        try:
            if isinstance(content, bytes):
                with open(full_path, mode) as f:
                    f.write(content)
            else:
                with open(full_path, mode, encoding=encoding) as f:
                    f.write(content)
            
            self._update_access_time()
            
            return {
                "success": True,
                "file_path": str(file_path),
                "absolute_path": str(full_path),
                "size_bytes": full_path.stat().st_size,
                "created_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": str(file_path)
            }
    
    def read_file(
        self,
        file_path: str,
        encoding: str = 'utf-8',
        binary: bool = False
    ) -> Dict[str, Any]:
        """
        Read file from sandbox file system.
        
        Args:
            file_path: Relative path within sandbox
            encoding: Encoding for text files
            binary: Whether to read as binary
        
        Returns:
            File content and metadata
        """
        full_path = self.file_system_root / file_path
        
        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        try:
            mode = 'rb' if binary else 'r'
            
            if binary:
                with open(full_path, mode) as f:
                    content = f.read()
            else:
                with open(full_path, mode, encoding=encoding) as f:
                    content = f.read()
            
            self._update_access_time()
            
            return {
                "success": True,
                "file_path": str(file_path),
                "content": content,
                "size_bytes": full_path.stat().st_size,
                "modified_at": datetime.fromtimestamp(
                    full_path.stat().st_mtime
                ).isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": str(file_path)
            }
    
    def append_file(
        self,
        file_path: str,
        content: str,
        encoding: str = 'utf-8'
    ) -> Dict[str, Any]:
        """Append content to existing file or create new."""
        full_path = self.file_system_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, 'a', encoding=encoding) as f:
                f.write(content)
            
            self._update_access_time()
            
            return {
                "success": True,
                "file_path": str(file_path),
                "size_bytes": full_path.stat().st_size
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_files(
        self,
        directory: str = "",
        pattern: str = "*",
        recursive: bool = False
    ) -> Dict[str, Any]:
        """
        List files in sandbox directory.
        
        Args:
            directory: Directory to list (relative to sandbox root)
            pattern: Glob pattern for filtering
            recursive: Whether to list recursively
        
        Returns:
            List of files with metadata
        """
        search_path = self.file_system_root / directory
        
        if not search_path.exists():
            return {
                "success": False,
                "error": f"Directory not found: {directory}"
            }
        
        try:
            if recursive:
                files = list(search_path.rglob(pattern))
            else:
                files = list(search_path.glob(pattern))
            
            file_list = []
            for file_path in files:
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.file_system_root)
                    file_list.append({
                        "path": str(rel_path),
                        "name": file_path.name,
                        "size_bytes": file_path.stat().st_size,
                        "modified_at": datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat()
                    })
            
            self._update_access_time()
            
            return {
                "success": True,
                "files": file_list,
                "count": len(file_list)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete file from sandbox."""
        full_path = self.file_system_root / file_path
        
        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        try:
            full_path.unlink()
            self._update_access_time()
            
            return {
                "success": True,
                "file_path": str(file_path)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # ==================== CONTEXT/KNOWLEDGE BASE LAYER ====================
    
    def store_context(
        self,
        key: str,
        value: Any,
        context_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Store context/knowledge in knowledge base.
        
        Args:
            key: Context key
            value: Context value (any JSON-serializable type)
            context_type: Type of context (general, task, conversation, etc.)
        
        Returns:
            Storage result
        """
        return self.context_db.store(key, value, context_type)
    
    def retrieve_context(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """Retrieve context from knowledge base."""
        return self.context_db.retrieve(key, default)
    
    def search_context(
        self,
        query: str,
        context_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search context by text query."""
        return self.context_db.search(query, context_type, limit)
    
    def list_context_keys(
        self,
        context_type: Optional[str] = None
    ) -> List[str]:
        """List all context keys."""
        return self.context_db.list_keys(context_type)
    
    # ==================== DATABASE LAYER ====================
    
    def create_database(
        self,
        db_name: str,
        db_type: str = "sqlite"
    ) -> Dict[str, Any]:
        """
        Create new database in sandbox.
        
        Args:
            db_name: Database name
            db_type: Database type (sqlite, postgresql, mysql)
        
        Returns:
            Database connection info
        """
        if not self.database_manager:
            return {
                "success": False,
                "error": "Database support not enabled"
            }
        
        return self.database_manager.create_database(db_name, db_type)
    
    def execute_query(
        self,
        db_name: str,
        query: str,
        params: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """Execute SQL query on database."""
        if not self.database_manager:
            return {
                "success": False,
                "error": "Database support not enabled"
            }
        
        return self.database_manager.execute_query(db_name, query, params)
    
    def get_database_connection(self, db_name: str) -> Optional[Any]:
        """Get database connection object."""
        if not self.database_manager:
            return None
        
        return self.database_manager.get_connection(db_name)
    
    # ==================== MEDIA CACHE LAYER ====================
    
    def cache_media(
        self,
        media_data: bytes,
        media_type: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cache media file (image, audio, video, presentation).
        
        Args:
            media_data: Binary media data
            media_type: Media type (image, audio, video, presentation, chart)
            filename: Optional filename (auto-generated if not provided)
        
        Returns:
            Cache result with file path
        """
        return self.media_cache.cache(media_data, media_type, filename)
    
    def retrieve_media(
        self,
        media_id: str
    ) -> Optional[bytes]:
        """Retrieve cached media by ID."""
        return self.media_cache.retrieve(media_id)
    
    def list_cached_media(
        self,
        media_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all cached media files."""
        return self.media_cache.list_files(media_type)
    
    # ==================== VECTOR STORE LAYER ====================
    
    def add_embedding(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add text embedding to vector store."""
        if not self.vector_store:
            return {
                "success": False,
                "error": "Vector store not enabled"
            }
        
        if not embedding_id:
            embedding_id = hashlib.md5(text.encode()).hexdigest()
        
        self.vector_store.add_text_embedding(
            text_id=embedding_id,
            text=text,
            metadata=metadata or {}
        )
        
        return {
            "success": True,
            "embedding_id": embedding_id
        }
    
    def semantic_search(
        self,
        query: str,
        n_results: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Perform semantic search in vector store."""
        if not self.vector_store:
            return []
        
        return self.vector_store.semantic_search(
            query=query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
    
    # ==================== UTILITY METHODS ====================
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics for sandbox."""
        stats = {
            "sandbox_id": self.sandbox_id,
            "total_size_bytes": 0,
            "layers": {}
        }
        
        # File system stats
        fs_size = sum(
            f.stat().st_size
            for f in self.file_system_root.rglob('*')
            if f.is_file()
        )
        stats["layers"]["file_system"] = {
            "size_bytes": fs_size,
            "file_count": len(list(self.file_system_root.rglob('*')))
        }
        stats["total_size_bytes"] += fs_size
        
        # Context store stats
        ctx_size = sum(
            f.stat().st_size
            for f in self.context_store_path.rglob('*')
            if f.is_file()
        )
        stats["layers"]["context"] = {
            "size_bytes": ctx_size,
            "entry_count": len(self.context_db.list_keys())
        }
        stats["total_size_bytes"] += ctx_size
        
        # Media cache stats
        media_size = sum(
            f.stat().st_size
            for f in self.media_cache_path.rglob('*')
            if f.is_file()
        )
        stats["layers"]["media_cache"] = {
            "size_bytes": media_size,
            "file_count": len(self.media_cache.list_files())
        }
        stats["total_size_bytes"] += media_size
        
        # Format sizes
        stats["total_size_mb"] = stats["total_size_bytes"] / (1024 * 1024)
        
        return stats
    
    def clear_layer(self, layer: StorageLayer) -> Dict[str, Any]:
        """Clear specific storage layer."""
        try:
            if layer == StorageLayer.FILE_SYSTEM:
                shutil.rmtree(self.file_system_root)
                self.file_system_root.mkdir(parents=True, exist_ok=True)
            
            elif layer == StorageLayer.CONTEXT_KNOWLEDGE:
                self.context_db.clear()
            
            elif layer == StorageLayer.MEDIA_CACHE:
                self.media_cache.clear()
            
            elif layer == StorageLayer.DATABASE:
                if self.database_manager:
                    shutil.rmtree(self.database_path)
                    self.database_path.mkdir(parents=True, exist_ok=True)
            
            return {
                "success": True,
                "layer": layer.value,
                "message": f"Cleared {layer.value} layer"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def export_sandbox(self, export_path: str) -> Dict[str, Any]:
        """Export entire sandbox to archive."""
        try:
            archive_path = shutil.make_archive(
                export_path,
                'zip',
                self.sandbox_root
            )
            
            return {
                "success": True,
                "archive_path": archive_path,
                "size_bytes": Path(archive_path).stat().st_size
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup(self):
        """Clean up sandbox resources."""
        if self.database_manager:
            self.database_manager.close_all()


class ContextKnowledgeBase:
    """
    In-memory JSON-based context/knowledge base with persistence.
    
    Stores task plans, user messages, tool observations, conversation history,
    and other contextual information needed for reasoning and execution flow.
    """
    
    def __init__(self, storage_path: Path):
        """Initialize context knowledge base."""
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.db_file = self.storage_path / "knowledge_base.json"
        self.contexts: Dict[str, Dict[str, Any]] = {}
        
        # Load existing data
        self._load()
    
    def _load(self):
        """Load contexts from disk."""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.contexts = json.load(f)
            except json.JSONDecodeError:
                self.contexts = {}
    
    def _save(self):
        """Save contexts to disk."""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.contexts, f, indent=2)
    
    def store(
        self,
        key: str,
        value: Any,
        context_type: str = "general"
    ) -> Dict[str, Any]:
        """Store context entry."""
        entry = {
            "value": value,
            "type": context_type,
            "stored_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        self.contexts[key] = entry
        self._save()
        
        return {
            "success": True,
            "key": key
        }
    
    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve context value."""
        entry = self.contexts.get(key)
        if entry:
            return entry.get("value", default)
        return default
    
    def search(
        self,
        query: str,
        context_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search contexts by text query."""
        results = []
        query_lower = query.lower()
        
        for key, entry in self.contexts.items():
            # Type filter
            if context_type and entry.get("type") != context_type:
                continue
            
            # Text search in key and value
            value_str = json.dumps(entry["value"]).lower()
            if query_lower in key.lower() or query_lower in value_str:
                results.append({
                    "key": key,
                    "value": entry["value"],
                    "type": entry["type"],
                    "stored_at": entry["stored_at"]
                })
        
        return results[:limit]
    
    def list_keys(self, context_type: Optional[str] = None) -> List[str]:
        """List all context keys."""
        if context_type:
            return [
                k for k, v in self.contexts.items()
                if v.get("type") == context_type
            ]
        return list(self.contexts.keys())
    
    def clear(self):
        """Clear all contexts."""
        self.contexts = {}
        self._save()


class DatabaseScaffold:
    """
    Database scaffold manager for creating and managing structured data storage.
    
    Supports SQLite (default), PostgreSQL, and MySQL databases within sandbox.
    """
    
    def __init__(self, database_path: Path):
        """Initialize database scaffold."""
        self.database_path = database_path
        self.database_path.mkdir(parents=True, exist_ok=True)
        
        self.connections: Dict[str, Any] = {}
        self.metadata = {}
    
    def create_database(
        self,
        db_name: str,
        db_type: str = "sqlite"
    ) -> Dict[str, Any]:
        """Create new database."""
        if db_type != "sqlite":
            return {
                "success": False,
                "error": f"Database type {db_type} not yet supported. Use 'sqlite'"
            }
        
        db_file = self.database_path / f"{db_name}.db"
        
        try:
            conn = sqlite3.connect(str(db_file))
            self.connections[db_name] = conn
            
            self.metadata[db_name] = {
                "type": db_type,
                "path": str(db_file),
                "created_at": datetime.utcnow().isoformat()
            }
            
            return {
                "success": True,
                "db_name": db_name,
                "db_path": str(db_file),
                "db_type": db_type
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_query(
        self,
        db_name: str,
        query: str,
        params: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """Execute SQL query."""
        if db_name not in self.connections:
            return {
                "success": False,
                "error": f"Database {db_name} not found"
            }
        
        try:
            conn = self.connections[db_name]
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            
            # Get results for SELECT queries
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                return {
                    "success": True,
                    "rows": rows,
                    "columns": columns,
                    "row_count": len(rows)
                }
            else:
                return {
                    "success": True,
                    "rows_affected": cursor.rowcount
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_connection(self, db_name: str) -> Optional[Any]:
        """Get database connection."""
        return self.connections.get(db_name)
    
    def close_all(self):
        """Close all database connections."""
        for conn in self.connections.values():
            conn.close()
        self.connections = {}


class MediaCache:
    """
    Media cache for storing generated images, charts, audio, presentations.
    
    Organizes media files by type and provides efficient retrieval.
    """
    
    def __init__(self, cache_path: Path):
        """Initialize media cache."""
        self.cache_path = cache_path
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Create type-specific directories
        self.media_types = ["image", "audio", "video", "presentation", "chart"]
        for media_type in self.media_types:
            (self.cache_path / media_type).mkdir(exist_ok=True)
        
        self.index_file = self.cache_path / "cache_index.json"
        self.index: Dict[str, Dict[str, Any]] = {}
        self._load_index()
    
    def _load_index(self):
        """Load cache index."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
            except json.JSONDecodeError:
                self.index = {}
    
    def _save_index(self):
        """Save cache index."""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
    
    def cache(
        self,
        media_data: bytes,
        media_type: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cache media file."""
        if media_type not in self.media_types:
            return {
                "success": False,
                "error": f"Invalid media type: {media_type}"
            }
        
        # Generate ID and filename
        media_id = hashlib.md5(media_data).hexdigest()
        
        if not filename:
            # Use hash as filename
            extension = self._guess_extension(media_type, media_data)
            filename = f"{media_id}{extension}"
        
        # Save file
        media_path = self.cache_path / media_type / filename
        
        try:
            with open(media_path, 'wb') as f:
                f.write(media_data)
            
            # Update index
            self.index[media_id] = {
                "type": media_type,
                "filename": filename,
                "path": str(media_path),
                "size_bytes": len(media_data),
                "cached_at": datetime.utcnow().isoformat()
            }
            self._save_index()
            
            return {
                "success": True,
                "media_id": media_id,
                "path": str(media_path),
                "size_bytes": len(media_data)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def retrieve(self, media_id: str) -> Optional[bytes]:
        """Retrieve cached media."""
        entry = self.index.get(media_id)
        if not entry:
            return None
        
        try:
            with open(entry["path"], 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def list_files(
        self,
        media_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List cached media files."""
        if media_type:
            return [
                {"media_id": k, **v}
                for k, v in self.index.items()
                if v.get("type") == media_type
            ]
        return [{"media_id": k, **v} for k, v in self.index.items()]
    
    def clear(self):
        """Clear all cached media."""
        for media_type in self.media_types:
            type_dir = self.cache_path / media_type
            if type_dir.exists():
                shutil.rmtree(type_dir)
                type_dir.mkdir()
        
        self.index = {}
        self._save_index()
    
    def _guess_extension(self, media_type: str, data: bytes) -> str:
        """Guess file extension from media type and data."""
        # Check magic bytes
        if data[:2] == b'\xff\xd8':
            return '.jpg'
        elif data[:8] == b'\x89PNG\r\n\x1a\n':
            return '.png'
        elif data[:4] == b'GIF8':
            return '.gif'
        
        # Default extensions by type
        defaults = {
            "image": ".png",
            "audio": ".mp3",
            "video": ".mp4",
            "presentation": ".pptx",
            "chart": ".png"
        }
        return defaults.get(media_type, ".bin")
