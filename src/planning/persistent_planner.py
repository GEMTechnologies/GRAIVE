"""
Persistent Planning System

Implements visible, version-controlled planning workflow with human-in-the-loop control.
All planning artifacts are saved as editable markdown files that users can review and modify.

This is the CORRECT architecture for autonomous document generation:
1. Create visible plan files
2. Allow human review/modification
3. Track versions of plans and modules
4. Maintain progress visibility
5. Enable interruption and redirection
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PersistentPlanner:
    """
    Persistent planning system with visible artifacts and version control.
    
    Creates markdown planning files that users can review, edit, and approve
    before generation begins. Tracks all versions and maintains progress state.
    """
    
    def __init__(self, session_workspace: Path):
        """
        Initialize persistent planner.
        
        Args:
            session_workspace: Session workspace root directory
        """
        self.session_workspace = Path(session_workspace)
        
        # Create planning structure
        self.planning_dir = self.session_workspace / "planning"
        self.modules_dir = self.session_workspace / "modules"
        self.assembly_dir = self.session_workspace / "assembly"
        self.progress_dir = self.session_workspace / "progress"
        
        for directory in [self.planning_dir, self.modules_dir, 
                         self.assembly_dir, self.progress_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Track versions
        self.plan_version = 0
        self.module_versions = {}
        self.draft_version = 0
        
        # Progress state
        self.current_module = 0
        self.total_modules = 0
        self.generation_status = "initialized"
    
    def create_initial_plan(
        self,
        topic: str,
        word_count: int,
        document_type: str = "essay",
        include_images: bool = False,
        include_tables: bool = False,
        user_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create initial planning document as visible markdown file.
        
        This creates a human-readable plan that the user can review and modify.
        
        Args:
            topic: Document topic
            word_count: Target word count
            document_type: Document type
            include_images: Include images
            include_tables: Include tables
            user_requirements: Additional user requirements
        
        Returns:
            Plan metadata with file paths
        """
        self.plan_version += 1
        plan_file = self.planning_dir / f"{self.plan_version}_initial_plan.md"
        
        print(f"\n{'='*70}")
        print(f"📋 CREATING STRATEGIC PLAN")
        print(f"{'='*70}\n")
        print(f"Topic: {topic}")
        print(f"Type: {document_type}")
        print(f"Target Words: {word_count:,}")
        print(f"{'='*70}\n")
        
        # Determine module breakdown
        modules = self._determine_modules(word_count, document_type, topic)
        self.total_modules = len(modules)
        
        # Create plan markdown
        plan_content = self._generate_plan_markdown(
            topic=topic,
            word_count=word_count,
            document_type=document_type,
            modules=modules,
            include_images=include_images,
            include_tables=include_tables,
            user_requirements=user_requirements
        )
        
        # Save plan
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        file_size = os.path.getsize(plan_file)
        
        print(f"✅ PLAN CREATED")
        print(f"📄 File: {plan_file.name}")
        print(f"📍 Location: {plan_file}")
        print(f"📊 Modules: {len(modules)}")
        print(f"💾 Size: {file_size:,} bytes\n")
        
        print(f"{'='*70}")
        print(f"⏸️  WAITING FOR USER APPROVAL")
        print(f"{'='*70}")
        print(f"Please review the plan at: {plan_file}")
        print(f"")
        print(f"Options:")
        print(f"  1. Type 'approve' to proceed with generation")
        print(f"  2. Edit {plan_file.name} and type 'updated' to reload")
        print(f"  3. Type 'cancel' to abort")
        print(f"{'='*70}\n")
        
        return {
            'plan_file': str(plan_file),
            'version': self.plan_version,
            'modules': modules,
            'total_modules': len(modules),
            'awaiting_approval': True
        }
    
    def _determine_modules(
        self,
        word_count: int,
        document_type: str,
        topic: str
    ) -> List[Dict[str, Any]]:
        """
        Break document into manageable modules.
        
        For long documents (>5000 words), creates multiple modules.
        Each module is a complete section that can be generated independently.
        """
        modules = []
        
        # Document type templates
        if document_type == "thesis" or word_count > 10000:
            # Large document - many modules
            modules = [
                {"title": "Abstract", "words": int(word_count * 0.05), "order": 1},
                {"title": "Introduction", "words": int(word_count * 0.15), "order": 2},
                {"title": "Literature Review", "words": int(word_count * 0.20), "order": 3},
                {"title": "Methodology", "words": int(word_count * 0.15), "order": 4},
                {"title": "Results", "words": int(word_count * 0.20), "order": 5},
                {"title": "Discussion", "words": int(word_count * 0.15), "order": 6},
                {"title": "Conclusion", "words": int(word_count * 0.10), "order": 7},
            ]
        elif document_type == "paper" or word_count > 5000:
            # Medium document - moderate modules
            modules = [
                {"title": "Introduction", "words": int(word_count * 0.20), "order": 1},
                {"title": f"Background and Context of {topic}", "words": int(word_count * 0.25), "order": 2},
                {"title": f"Main Analysis of {topic}", "words": int(word_count * 0.30), "order": 3},
                {"title": f"Implications and Future Directions", "words": int(word_count * 0.15), "order": 4},
                {"title": "Conclusion", "words": int(word_count * 0.10), "order": 5},
            ]
        else:
            # Standard document - simple modules
            module_count = max(3, min(6, word_count // 1000))
            intro_words = int(word_count * 0.15)
            conclusion_words = int(word_count * 0.15)
            body_words = word_count - intro_words - conclusion_words
            body_per_module = body_words // (module_count - 2)
            
            modules.append({"title": "Introduction", "words": intro_words, "order": 1})
            
            for i in range(module_count - 2):
                modules.append({
                    "title": f"Section {i+1}: Aspect {i+1} of {topic}",
                    "words": body_per_module,
                    "order": i + 2
                })
            
            modules.append({"title": "Conclusion", "words": conclusion_words, "order": module_count})
        
        return modules
    
    def _generate_plan_markdown(
        self,
        topic: str,
        word_count: int,
        document_type: str,
        modules: List[Dict],
        include_images: bool,
        include_tables: bool,
        user_requirements: Optional[str]
    ) -> str:
        """Generate markdown content for the plan file."""
        
        plan_md = f"""# Document Generation Plan

## Document Metadata
- **Topic**: {topic}
- **Type**: {document_type}
- **Target Word Count**: {word_count:,} words
- **Include Images**: {'Yes' if include_images else 'No'}
- **Include Tables**: {'Yes' if include_tables else 'No'}
- **Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Plan Version**: {self.plan_version}

## User Requirements
{user_requirements if user_requirements else "None specified"}

---

## Module Breakdown

The document will be generated in {len(modules)} modules for better control and quality:

"""
        
        for module in modules:
            plan_md += f"""### Module {module['order']}: {module['title']}
- **Target Words**: {module['words']:,}
- **Purpose**: [Auto-generated - you can edit this]
- **Key Points to Cover**:
  - [Edit to add specific points you want covered]
  - [Add more points as needed]
- **Media Requirements**:
  - Images: {"Yes" if include_images and module['order'] not in [1, len(modules)] else "No"}
  - Tables: {"Yes" if include_tables and module['order'] not in [1, len(modules)] else "No"}

"""
        
        plan_md += f"""
---

## Generation Strategy

1. **Module-by-Module Generation**: Each module will be generated independently with full context from previous modules
2. **Progress Tracking**: You will see real-time progress for each module
3. **Quality Checkpoints**: Each module undergoes quality review before proceeding
4. **Human-in-the-Loop**: You can interrupt and provide feedback at any point
5. **Version Control**: All drafts and revisions are saved with version numbers

## Estimated Timeline

- Planning Phase: Complete ✅
- Module Generation: ~{len(modules) * 2} minutes ({len(modules)} modules × ~2 min each)
- Assembly & Review: ~3 minutes
- **Total Estimated Time**: ~{len(modules) * 2 + 3} minutes

---

## Instructions

### To Approve This Plan:
Type `approve` in the chat

### To Modify This Plan:
1. Edit this file directly (change module titles, word counts, key points, etc.)
2. Save your changes
3. Type `updated` in the chat to reload the modified plan

### To Cancel:
Type `cancel` in the chat

---

## Notes

- This plan is a living document - it will be updated as generation progresses
- Each completed module will be marked with ✅
- Any issues or revisions will be noted in version history
- You can request changes to any module before or after generation

"""
        
        return plan_md
    
    def create_module_plans(self, modules: List[Dict]) -> List[str]:
        """
        Create individual planning files for each module.
        
        These serve as targets for generation and track progress.
        """
        module_files = []
        
        print(f"\n📋 Creating module planning files...\n")
        
        for module in modules:
            module_file = self.modules_dir / f"module_{module['order']}_{self._sanitize_filename(module['title'])}.md"
            
            module_content = f"""# Module {module['order']}: {module['title']}

## Status
- [  ] Planning
- [  ] Generating
- [  ] Quality Review
- [  ] Complete

## Specifications
- **Target Words**: {module['words']:,}
- **Current Words**: 0
- **Quality Score**: Not yet assessed

## Content

[Content will be generated here]

## Quality Report

[Quality assessment will appear here after generation]

## Version History
- v1: Initial planning ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

"""
            
            with open(module_file, 'w', encoding='utf-8') as f:
                f.write(module_content)
            
            module_files.append(str(module_file))
            self.module_versions[module['title']] = 1
            
            print(f"   ✅ Created: {module_file.name}")
        
        print(f"\n✅ All {len(modules)} module plans created\n")
        
        return module_files
    
    def update_module_status(
        self,
        module_order: int,
        status: str,
        content: Optional[str] = None,
        quality_score: Optional[float] = None
    ):
        """
        Update module status with progress tracking.
        
        Args:
            module_order: Module number (1-indexed)
            status: Status (planning/generating/review/complete)
            content: Generated content (if available)
            quality_score: Quality assessment score
        """
        # Find module file
        module_files = list(self.modules_dir.glob(f"module_{module_order}_*.md"))
        if not module_files:
            print(f"⚠️  Module {module_order} file not found")
            return
        
        module_file = module_files[0]
        
        # Read current content
        with open(module_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Update status checkboxes
        status_map = {
            'planning': 0,
            'generating': 1,
            'review': 2,
            'complete': 3
        }
        
        lines = current_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('- ['):
                status_index = (i - lines.index('## Status') - 1)
                if status_index <= status_map.get(status, 0):
                    lines[i] = line.replace('[ ]', '[✓]')
        
        # Update content if provided
        if content:
            content_index = lines.index('## Content')
            lines[content_index + 2] = content
            
            # Update word count
            word_count = len(content.split())
            for i, line in enumerate(lines):
                if line.startswith('- **Current Words**:'):
                    lines[i] = f"- **Current Words**: {word_count:,}"
        
        # Update quality score if provided
        if quality_score is not None:
            for i, line in enumerate(lines):
                if line.startswith('- **Quality Score**:'):
                    lines[i] = f"- **Quality Score**: {quality_score:.2f}/10"
        
        # Add version entry
        version_index = lines.index('## Version History')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines.insert(version_index + 1, f"- v{self.module_versions.get(module_file.stem, 1) + 1}: {status.capitalize()} ({timestamp})")
        
        # Write back
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        # Update progress tracking
        self._update_progress_file(module_order, status)
    
    def _update_progress_file(self, module_order: int, status: str):
        """Update the progress tracking file for real-time visibility."""
        progress_file = self.progress_dir / "current_progress.md"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        progress_content = f"""# Document Generation Progress

**Last Updated**: {timestamp}

## Overall Status
- **Current Module**: {module_order}/{self.total_modules}
- **Progress**: {int((module_order / self.total_modules) * 100)}%
- **Status**: {status.upper()}

## Module Progress
"""
        
        # Add module progress bars
        for i in range(1, self.total_modules + 1):
            if i < module_order:
                progress_content += f"- Module {i}: ✅ COMPLETE\n"
            elif i == module_order:
                progress_content += f"- Module {i}: 🔄 {status.upper()}\n"
            else:
                progress_content += f"- Module {i}: ⏸️  PENDING\n"
        
        progress_content += f"""
## Timeline
- **Started**: [Track start time]
- **Current Duration**: [Calculate elapsed]
- **Estimated Completion**: [Estimate based on progress]

---
*This file updates in real-time as generation progresses*
"""
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            f.write(progress_content)
    
    def save_assembly_draft(
        self,
        content: str,
        draft_type: str = "combined"
    ) -> str:
        """
        Save assembly draft with version tracking.
        
        Args:
            content: Assembled document content
            draft_type: Type of draft (combined/revised/final)
        
        Returns:
            Path to saved draft file
        """
        self.draft_version += 1
        draft_file = self.assembly_dir / f"draft_{self.draft_version}_{draft_type}.md"
        
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        file_size = os.path.getsize(draft_file)
        word_count = len(content.split())
        
        print(f"\n✅ DRAFT SAVED")
        print(f"📄 File: {draft_file.name}")
        print(f"📊 Words: {word_count:,}")
        print(f"💾 Size: {file_size:,} bytes\n")
        
        return str(draft_file)
    
    def _sanitize_filename(self, title: str) -> str:
        """Convert title to safe filename."""
        safe = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        return safe.lower()[:50]  # Limit length


def create_persistent_planner(session_workspace: Path) -> PersistentPlanner:
    """Factory function to create persistent planner."""
    return PersistentPlanner(session_workspace)
