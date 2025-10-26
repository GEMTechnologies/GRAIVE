"""
CLI File Operations Module

Provides command-line style file operations for Graive AI:
- Create files and directories
- Delete files and directories  
- Rename/move files
- Edit file contents
- List directory contents
- Copy files
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional


class FileOperations:
    """
    CLI-style file operations with safety checks and progress tracking.
    """
    
    def __init__(self, workspace_path: str):
        """
        Initialize file operations.
        
        Args:
            workspace_path: Root workspace directory
        """
        self.workspace = Path(workspace_path)
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    def create_file(self, file_path: str, content: str = "") -> Dict[str, Any]:
        """
        Create a new file with optional content.
        
        Args:
            file_path: Path to file (relative to workspace or absolute)
            content: File content (default: empty)
        
        Returns:
            Result dict with success status
        """
        try:
            path = self._resolve_path(file_path)
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(path)
            
            print(f"✅ Created file: {path.name}")
            print(f"   📍 Path: {path}")
            print(f"   💾 Size: {file_size:,} bytes")
            
            return {
                "success": True,
                "action": "create_file",
                "path": str(path),
                "size": file_size
            }
        
        except Exception as e:
            print(f"❌ Failed to create file: {e}")
            return {
                "success": False,
                "action": "create_file",
                "error": str(e)
            }
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file.
        
        Args:
            file_path: Path to file to delete
        
        Returns:
            Result dict with success status
        """
        try:
            path = self._resolve_path(file_path)
            
            if not path.exists():
                return {
                    "success": False,
                    "action": "delete_file",
                    "error": f"File not found: {path}"
                }
            
            if path.is_dir():
                return {
                    "success": False,
                    "action": "delete_file",
                    "error": f"Path is a directory. Use delete_directory instead."
                }
            
            # Delete file
            path.unlink()
            
            print(f"✅ Deleted file: {path.name}")
            print(f"   📍 Was at: {path}")
            
            return {
                "success": True,
                "action": "delete_file",
                "path": str(path)
            }
        
        except Exception as e:
            print(f"❌ Failed to delete file: {e}")
            return {
                "success": False,
                "action": "delete_file",
                "error": str(e)
            }
    
    def rename_file(self, old_path: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a file or move it to a new location.
        
        Args:
            old_path: Current file path
            new_name: New filename or full path
        
        Returns:
            Result dict with success status
        """
        try:
            old = self._resolve_path(old_path)
            
            if not old.exists():
                return {
                    "success": False,
                    "action": "rename_file",
                    "error": f"File not found: {old}"
                }
            
            # Check if new_name is full path or just filename
            if '/' in new_name or '\\' in new_name:
                new = self._resolve_path(new_name)
            else:
                new = old.parent / new_name
            
            # Rename/move file
            old.rename(new)
            
            print(f"✅ Renamed file:")
            print(f"   📝 From: {old.name}")
            print(f"   📝 To: {new.name}")
            print(f"   📍 Location: {new}")
            
            return {
                "success": True,
                "action": "rename_file",
                "old_path": str(old),
                "new_path": str(new)
            }
        
        except Exception as e:
            print(f"❌ Failed to rename file: {e}")
            return {
                "success": False,
                "action": "rename_file",
                "error": str(e)
            }
    
    def edit_file(self, file_path: str, new_content: str, mode: str = 'overwrite') -> Dict[str, Any]:
        """
        Edit file contents.
        
        Args:
            file_path: Path to file
            new_content: New content to write
            mode: 'overwrite', 'append', or 'prepend'
        
        Returns:
            Result dict with success status
        """
        try:
            path = self._resolve_path(file_path)
            
            if not path.exists() and mode != 'overwrite':
                return {
                    "success": False,
                    "action": "edit_file",
                    "error": f"File not found: {path}"
                }
            
            if mode == 'overwrite':
                content = new_content
            elif mode == 'append':
                existing = path.read_text(encoding='utf-8')
                content = existing + new_content
            elif mode == 'prepend':
                existing = path.read_text(encoding='utf-8')
                content = new_content + existing
            else:
                return {
                    "success": False,
                    "action": "edit_file",
                    "error": f"Invalid mode: {mode}"
                }
            
            # Write new content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(path)
            
            print(f"✅ Edited file: {path.name}")
            print(f"   📍 Path: {path}")
            print(f"   📝 Mode: {mode}")
            print(f"   💾 Size: {file_size:,} bytes")
            
            return {
                "success": True,
                "action": "edit_file",
                "path": str(path),
                "mode": mode,
                "size": file_size
            }
        
        except Exception as e:
            print(f"❌ Failed to edit file: {e}")
            return {
                "success": False,
                "action": "edit_file",
                "error": str(e)
            }
    
    def create_directory(self, dir_path: str) -> Dict[str, Any]:
        """
        Create a directory.
        
        Args:
            dir_path: Path to directory to create
        
        Returns:
            Result dict with success status
        """
        try:
            path = self._resolve_path(dir_path)
            path.mkdir(parents=True, exist_ok=True)
            
            print(f"✅ Created directory: {path.name}")
            print(f"   📍 Path: {path}")
            
            return {
                "success": True,
                "action": "create_directory",
                "path": str(path)
            }
        
        except Exception as e:
            print(f"❌ Failed to create directory: {e}")
            return {
                "success": False,
                "action": "create_directory",
                "error": str(e)
            }
    
    def delete_directory(self, dir_path: str, recursive: bool = False) -> Dict[str, Any]:
        """
        Delete a directory.
        
        Args:
            dir_path: Path to directory
            recursive: Delete recursively (including contents)
        
        Returns:
            Result dict with success status
        """
        try:
            path = self._resolve_path(dir_path)
            
            if not path.exists():
                return {
                    "success": False,
                    "action": "delete_directory",
                    "error": f"Directory not found: {path}"
                }
            
            if not path.is_dir():
                return {
                    "success": False,
                    "action": "delete_directory",
                    "error": f"Path is not a directory: {path}"
                }
            
            if recursive:
                shutil.rmtree(path)
                print(f"✅ Deleted directory (recursive): {path.name}")
            else:
                path.rmdir()  # Only works if empty
                print(f"✅ Deleted empty directory: {path.name}")
            
            print(f"   📍 Was at: {path}")
            
            return {
                "success": True,
                "action": "delete_directory",
                "path": str(path),
                "recursive": recursive
            }
        
        except Exception as e:
            print(f"❌ Failed to delete directory: {e}")
            return {
                "success": False,
                "action": "delete_directory",
                "error": str(e)
            }
    
    def list_directory(self, dir_path: str = ".", pattern: str = "*") -> Dict[str, Any]:
        """
        List directory contents.
        
        Args:
            dir_path: Directory to list (default: current)
            pattern: Glob pattern to filter (default: all files)
        
        Returns:
            Result dict with file list
        """
        try:
            path = self._resolve_path(dir_path)
            
            if not path.exists():
                return {
                    "success": False,
                    "action": "list_directory",
                    "error": f"Directory not found: {path}"
                }
            
            if not path.is_dir():
                return {
                    "success": False,
                    "action": "list_directory",
                    "error": f"Path is not a directory: {path}"
                }
            
            # List files matching pattern
            files = []
            dirs = []
            
            for item in sorted(path.glob(pattern)):
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "size": item.stat().st_size,
                        "path": str(item)
                    })
                elif item.is_dir():
                    dirs.append({
                        "name": item.name,
                        "path": str(item)
                    })
            
            print(f"📁 Contents of: {path}")
            print(f"\n   Directories ({len(dirs)}):")
            for d in dirs[:10]:
                print(f"     📂 {d['name']}/")
            if len(dirs) > 10:
                print(f"     ... and {len(dirs) - 10} more")
            
            print(f"\n   Files ({len(files)}):")
            for f in files[:10]:
                print(f"     📄 {f['name']} ({f['size']:,} bytes)")
            if len(files) > 10:
                print(f"     ... and {len(files) - 10} more")
            
            return {
                "success": True,
                "action": "list_directory",
                "path": str(path),
                "files": files,
                "directories": dirs,
                "total_files": len(files),
                "total_directories": len(dirs)
            }
        
        except Exception as e:
            print(f"❌ Failed to list directory: {e}")
            return {
                "success": False,
                "action": "list_directory",
                "error": str(e)
            }
    
    def copy_file(self, source_path: str, dest_path: str) -> Dict[str, Any]:
        """
        Copy a file.
        
        Args:
            source_path: Source file path
            dest_path: Destination file path
        
        Returns:
            Result dict with success status
        """
        try:
            source = self._resolve_path(source_path)
            dest = self._resolve_path(dest_path)
            
            if not source.exists():
                return {
                    "success": False,
                    "action": "copy_file",
                    "error": f"Source file not found: {source}"
                }
            
            # Create destination directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source, dest)
            
            file_size = os.path.getsize(dest)
            
            print(f"✅ Copied file:")
            print(f"   📝 From: {source.name}")
            print(f"   📝 To: {dest.name}")
            print(f"   💾 Size: {file_size:,} bytes")
            
            return {
                "success": True,
                "action": "copy_file",
                "source": str(source),
                "destination": str(dest),
                "size": file_size
            }
        
        except Exception as e:
            print(f"❌ Failed to copy file: {e}")
            return {
                "success": False,
                "action": "copy_file",
                "error": str(e)
            }
    
    def _resolve_path(self, file_path: str) -> Path:
        """
        Resolve file path (relative to workspace or absolute).
        
        Args:
            file_path: File path to resolve
        
        Returns:
            Resolved Path object
        """
        path = Path(file_path)
        
        if path.is_absolute():
            return path
        else:
            return self.workspace / path


def create_file_operations(workspace_path: str) -> FileOperations:
    """
    Factory function to create file operations instance.
    
    Args:
        workspace_path: Path to workspace
    
    Returns:
        Configured FileOperations instance
    """
    return FileOperations(workspace_path)
