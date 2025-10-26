"""
Storage Tool - Unified Interface for Multi-layered Data Storage

This tool provides a unified interface for accessing all storage layers within
a Graive sandbox: file system, context/knowledge base, databases, media cache,
and vector embeddings.
"""

from typing import Dict, List, Any, Optional, Union
from src.storage.sandbox_storage import SandboxStorageManager, StorageLayer


class StorageTool:
    """
    Unified storage tool for Graive AI sandboxes.
    
    Provides high-level interface for all storage operations across
    multiple persistence layers.
    """
    
    def __init__(self, sandbox_manager: SandboxStorageManager):
        """
        Initialize storage tool.
        
        Args:
            sandbox_manager: SandboxStorageManager instance
        """
        self.storage = sandbox_manager
        self.name = "storage_tool"
        self.description = "Multi-layered persistent storage for files, data, context, and media"
    
    def get_available_actions(self) -> List[str]:
        """Get list of available storage actions."""
        return [
            # File system
            "write_file",
            "read_file",
            "append_file",
            "list_files",
            "delete_file",
            
            # Context/Knowledge
            "store_context",
            "retrieve_context",
            "search_context",
            "list_context_keys",
            
            # Database
            "create_database",
            "execute_query",
            "get_tables",
            
            # Media cache
            "cache_media",
            "retrieve_media",
            "list_media",
            
            # Vector store
            "add_embedding",
            "semantic_search",
            
            # Utilities
            "get_storage_stats",
            "export_sandbox",
            "clear_layer"
        ]
    
    def execute(self, action: str, **params) -> Dict[str, Any]:
        """
        Execute storage action.
        
        Args:
            action: Action name
            **params: Action-specific parameters
        
        Returns:
            Action result dictionary
        """
        # File system actions
        if action == "write_file":
            return self.storage.write_file(
                file_path=params["file_path"],
                content=params["content"],
                encoding=params.get("encoding", "utf-8")
            )
        
        elif action == "read_file":
            return self.storage.read_file(
                file_path=params["file_path"],
                encoding=params.get("encoding", "utf-8"),
                binary=params.get("binary", False)
            )
        
        elif action == "append_file":
            return self.storage.append_file(
                file_path=params["file_path"],
                content=params["content"],
                encoding=params.get("encoding", "utf-8")
            )
        
        elif action == "list_files":
            return self.storage.list_files(
                directory=params.get("directory", ""),
                pattern=params.get("pattern", "*"),
                recursive=params.get("recursive", False)
            )
        
        elif action == "delete_file":
            return self.storage.delete_file(
                file_path=params["file_path"]
            )
        
        # Context/Knowledge actions
        elif action == "store_context":
            return self.storage.store_context(
                key=params["key"],
                value=params["value"],
                context_type=params.get("context_type", "general")
            )
        
        elif action == "retrieve_context":
            result = self.storage.retrieve_context(
                key=params["key"],
                default=params.get("default")
            )
            return {"success": True, "value": result}
        
        elif action == "search_context":
            results = self.storage.search_context(
                query=params["query"],
                context_type=params.get("context_type"),
                limit=params.get("limit", 10)
            )
            return {"success": True, "results": results}
        
        elif action == "list_context_keys":
            keys = self.storage.list_context_keys(
                context_type=params.get("context_type")
            )
            return {"success": True, "keys": keys}
        
        # Database actions
        elif action == "create_database":
            return self.storage.create_database(
                db_name=params["db_name"],
                db_type=params.get("db_type", "sqlite")
            )
        
        elif action == "execute_query":
            return self.storage.execute_query(
                db_name=params["db_name"],
                query=params["query"],
                params=params.get("query_params")
            )
        
        elif action == "get_tables":
            return self.storage.execute_query(
                db_name=params["db_name"],
                query="SELECT name FROM sqlite_master WHERE type='table'"
            )
        
        # Media cache actions
        elif action == "cache_media":
            return self.storage.cache_media(
                media_data=params["media_data"],
                media_type=params["media_type"],
                filename=params.get("filename")
            )
        
        elif action == "retrieve_media":
            media_data = self.storage.retrieve_media(
                media_id=params["media_id"]
            )
            return {
                "success": media_data is not None,
                "media_data": media_data
            }
        
        elif action == "list_media":
            files = self.storage.list_cached_media(
                media_type=params.get("media_type")
            )
            return {"success": True, "files": files}
        
        # Vector store actions
        elif action == "add_embedding":
            return self.storage.add_embedding(
                text=params["text"],
                metadata=params.get("metadata"),
                embedding_id=params.get("embedding_id")
            )
        
        elif action == "semantic_search":
            results = self.storage.semantic_search(
                query=params["query"],
                n_results=params.get("n_results", 10),
                filter_metadata=params.get("filter_metadata")
            )
            return {"success": True, "results": results}
        
        # Utility actions
        elif action == "get_storage_stats":
            stats = self.storage.get_storage_stats()
            return {"success": True, "stats": stats}
        
        elif action == "export_sandbox":
            return self.storage.export_sandbox(
                export_path=params["export_path"]
            )
        
        elif action == "clear_layer":
            layer = StorageLayer(params["layer"])
            return self.storage.clear_layer(layer)
        
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }


def create_storage_tool_for_sandbox(
    sandbox_id: str,
    base_path: str = "./sandboxes"
) -> StorageTool:
    """
    Create storage tool for a specific sandbox.
    
    Args:
        sandbox_id: Unique sandbox identifier
        base_path: Base path for sandbox storage
    
    Returns:
        Configured StorageTool instance
    """
    storage_manager = SandboxStorageManager(
        sandbox_id=sandbox_id,
        base_path=base_path,
        enable_database=True,
        enable_vector_store=True
    )
    
    return StorageTool(storage_manager)
