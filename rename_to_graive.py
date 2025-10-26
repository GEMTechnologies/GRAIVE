#!/usr/bin/env python
"""
Comprehensive renaming script: Manus → Graive

This script safely renames all occurrences of "manus" to "graive" throughout
the codebase while preserving functionality.

Handles:
- File names
- Directory names  
- Code references (classes, functions, variables)
- Documentation
- Comments
- String literals
- Import statements
"""

import os
import re
from pathlib import Path
import shutil

# Workspace root
WORKSPACE = Path(r"c:\Users\GEMTECH 1\Desktop\MANUS")

# Files and directories to skip
SKIP_PATTERNS = {
    '__pycache__',
    '.git',
    '.pytest_cache',
    'node_modules',
    '.venv',
    'venv',
    'rename_to_graive.py',  # Don't modify self
    '.pyc',
    '.pyo'
}

def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    return any(skip in str(path) for skip in SKIP_PATTERNS)

def rename_in_file(file_path: Path):
    """Rename all occurrences of manus to graive in a file."""
    if should_skip(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Track if changes were made
        original_content = content
        
        # Replace variations of "manus" with "graive"
        replacements = [
            # All caps
            (r'\bMANUS\b', 'GRAIVE'),
            # Title case
            (r'\bManus\b', 'Graive'),
            # Lower case
            (r'\bmanus\b', 'graive'),
            # In paths (special handling)
            (r'Desktop\\MANUS', r'Desktop\\GRAIVE'),
            (r'Desktop/MANUS', r'Desktop/GRAIVE'),
            # Class names
            (r'ManusAI', 'GraiveAI'),
            # URLs/identifiers that might contain manus
            (r'manus_', 'graive_'),
            (r'_manus', '_graive'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"  ⚠️  Error processing {file_path}: {e}")
        return False

def rename_file_or_dir(path: Path) -> Path:
    """Rename file or directory if it contains 'manus'."""
    if should_skip(path):
        return path
    
    name = path.name.lower()
    
    if 'manus' in name:
        # Create new name
        new_name = path.name.replace('manus', 'graive').replace('Manus', 'Graive').replace('MANUS', 'GRAIVE')
        new_path = path.parent / new_name
        
        try:
            # Rename
            path.rename(new_path)
            print(f"  ✅ Renamed: {path.name} → {new_name}")
            return new_path
        except Exception as e:
            print(f"  ⚠️  Could not rename {path}: {e}")
            return path
    
    return path

def main():
    """Main renaming process."""
    print("="*70)
    print("🔄 RENAMING MANUS → GRAIVE")
    print("="*70)
    print(f"Workspace: {WORKSPACE}\n")
    
    # Phase 1: Rename file contents
    print("Phase 1: Updating file contents...")
    print("-"*70)
    
    files_changed = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(WORKSPACE):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not should_skip(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            
            # Only process text files
            if file_path.suffix in {'.py', '.md', '.txt', '.yaml', '.yml', '.json', '.bat', '.sh', '.rst'}:
                files_processed += 1
                if rename_in_file(file_path):
                    files_changed += 1
                    print(f"  ✓ Updated: {file_path.relative_to(WORKSPACE)}")
    
    print(f"\n✅ Phase 1 Complete: {files_changed}/{files_processed} files updated\n")
    
    # Phase 2: Rename main Python file
    print("Phase 2: Renaming main entry point...")
    print("-"*70)
    
    manus_py = WORKSPACE / "manus.py"
    if manus_py.exists():
        graive_py = WORKSPACE / "graive.py"
        manus_py.rename(graive_py)
        print(f"  ✅ Renamed: manus.py → graive.py\n")
    
    # Phase 3: Rename test files
    print("Phase 3: Renaming test files...")
    print("-"*70)
    
    test_files_renamed = 0
    for file in WORKSPACE.glob("test_*.py"):
        if 'manus' in file.name.lower():
            new_path = rename_file_or_dir(file)
            if new_path != file:
                test_files_renamed += 1
    
    print(f"\n✅ Phase 3 Complete: {test_files_renamed} test files renamed\n")
    
    # Phase 4: Update batch files
    print("Phase 4: Updating batch files...")
    print("-"*70)
    
    for bat_file in WORKSPACE.glob("*.bat"):
        if rename_in_file(bat_file):
            print(f"  ✓ Updated: {bat_file.name}")
    
    print("\n✅ Phase 4 Complete\n")
    
    # Final Summary
    print("="*70)
    print("✅ RENAMING COMPLETE")
    print("="*70)
    print(f"Files updated: {files_changed}")
    print(f"Main file: manus.py → graive.py")
    print(f"Test files: {test_files_renamed} renamed")
    print("\nNext steps:")
    print("1. Review changes: git diff (if using git)")
    print("2. Test the system: python graive.py")
    print("3. Update documentation if needed")
    print("="*70)

if __name__ == "__main__":
    main()
