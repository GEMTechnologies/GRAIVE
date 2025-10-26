# 🎯 Persistent Planning Architecture - The Original Graive Approach

## Executive Summary

You've revealed the critical missing component: the original Graive creates **visible, editable planning markdown files** throughout the generation process, enabling complete transparency, human interruption, and version tracking. The current implementation has sophisticated orchestration but lacks this persistent artifact layer.

## 🔍 What You Described (The Original Architecture)

### Complete Workflow for 12,000-Word Document

#### Stage 1: Strategic Planning (User Visible ✅)

**System Creates:**
```
workspace/session_20251026_145623/planning/
├── 1_initial_plan.md          ← USER CAN REVIEW AND EDIT
├── 2_plan_v2.md               ← AFTER USER MODIFICATIONS
└── 3_final_plan.md            ← APPROVED VERSION
```

**What `1_initial_plan.md` Contains:**
```markdown
# Document Generation Plan

## Document Metadata
- **Topic**: Impact of Climate Change on African Agriculture
- **Type**: Research Paper
- **Target Word Count**: 12,000 words
- **Created**: 2025-10-26 14:56:23
- **Plan Version**: 1

## Module Breakdown

The document will be generated in 6 modules:

### Module 1: Introduction
- **Target Words**: 1,800
- **Purpose**: Establish context and research questions
- **Key Points to Cover**:
  - Background on climate change
  - Significance for African agriculture
  - Research objectives
  - Thesis statement
- **Media Requirements**:
  - Images: No
  - Tables: No

### Module 2: Literature Review
- **Target Words**: 2,400
- **Purpose**: Synthesize existing research
- **Key Points**:
  - Historical climate patterns in Africa
  - Agricultural vulnerability studies
  - Adaptation strategies research
  - Gaps in current literature
- **Media Requirements**:
  - Images: Yes (1 climate trend chart)
  - Tables: Yes (1 summary of key studies)

[...continues for all 6 modules...]

## Instructions

### To Approve This Plan:
Type `approve` in the chat

### To Modify This Plan:
1. Edit this file directly
2. Save changes
3. Type `updated` to reload

### To Cancel:
Type `cancel`
```

**User Workflow:**
```
System: ⏸️  WAITING FOR USER APPROVAL
        Please review: planning/1_initial_plan.md
        
User: [Opens file, edits Module 2 to add specific requirements]
      
User: updated

System: ✅ Reloaded plan
        Changes detected in Module 2
        Ready to proceed?
        
User: approve

System: 🚀 Starting generation...
```

#### Stage 2: Module Planning Files (Progress Tracking ✅)

**System Creates:**
```
workspace/session_20251026_145623/modules/
├── module_1_introduction.md
├── module_2_literature_review.md
├── module_3_methodology.md
├── module_4_results.md
├── module_5_discussion.md
└── module_6_conclusion.md
```

**What `module_2_literature_review.md` Contains During Generation:**
```markdown
# Module 2: Literature Review

## Status
- [✓] Planning
- [✓] Generating
- [  ] Quality Review
- [  ] Complete

## Specifications
- **Target Words**: 2,400
- **Current Words**: 1,847
- **Quality Score**: Assessing...

## Content

[Content being generated appears here in real-time...]

## Quality Report

[Will appear after generation]

## Version History
- v1: Initial planning (2025-10-26 14:56:30)
- v2: Generation started (2025-10-26 14:58:15)
- v3: Generating (2025-10-26 14:59:02) - 45% complete
```

**User Can See Progress:**
```
workspace/session_20251026_145623/progress/
└── current_progress.md         ← UPDATES IN REAL-TIME
```

**What `current_progress.md` Contains:**
```markdown
# Document Generation Progress

**Last Updated**: 2025-10-26 14:59:02

## Overall Status
- **Current Module**: 2/6
- **Progress**: 33%
- **Status**: GENERATING

## Module Progress
- Module 1: ✅ COMPLETE (1,825 words, Quality: 8.4/10)
- Module 2: 🔄 GENERATING (1,847/2,400 words - 77%)
- Module 3: ⏸️  PENDING
- Module 4: ⏸️  PENDING
- Module 5: ⏸️  PENDING
- Module 6: ⏸️  PENDING

## Timeline
- **Started**: 2025-10-26 14:58:00
- **Elapsed**: 1 minute 2 seconds
- **Estimated Completion**: ~8 minutes remaining

---
*This file updates every 5 seconds*
```

#### Stage 3: Human Interruption (Critical Feature ✅)

**Scenario: User Sees Progress and Wants to Change Direction**

```
System: [Currently generating Module 2 - Literature Review]
        Progress: 1,847/2,400 words (77%)

User: stop

System: ⏸️  PAUSED at Module 2 (77% complete)
        
        Options:
        1. Continue - Resume generation
        2. Modify - Edit current module requirements
        3. Restart - Regenerate this module from scratch
        4. Cancel - Abort generation
        
User: modify

System: Please edit: modules/module_2_literature_review.md
        Type 'ready' when done

User: [Edits the file to add: "Focus more on sub-Saharan studies"]
      ready

System: ✅ Changes detected
        Recommendation: Restart Module 2 to incorporate changes
        Proceed with restart? (yes/no)
        
User: yes

System: 🔄 Regenerating Module 2 with updated requirements...
        [Generation resumes with new focus]
```

#### Stage 4: Assembly with Version Tracking (Transparency ✅)

**System Creates:**
```
workspace/session_20251026_145623/assembly/
├── draft_1_combined.md        ← All modules merged
├── draft_2_revised.md         ← After quality improvements
├── draft_3_final.md           ← Final approved version
└── verification_report.md     ← Quality assessment
```

**What `draft_1_combined.md` Header Looks Like:**
```markdown
# Impact of Climate Change on African Agriculture

**Draft Version**: 1 (Combined)
**Generated**: 2025-10-26 15:05:42
**Total Words**: 11,847
**Status**: Under Review

---

[Complete assembled document from all modules...]

---

## Generation Metadata
- Modules: 6
- Total Generation Time: 7 minutes 42 seconds
- Quality Scores: [8.4, 8.2, 8.7, 8.5, 8.3, 8.6]
- Revisions: 1 (Module 2 restarted)
```

**User Review Process:**
```
System: ✅ DRAFT 1 COMPLETE
        📄 File: assembly/draft_1_combined.md
        📊 Words: 11,847 / 12,000 (98.7%)
        
        Please review the draft.
        
        Options:
        1. Approve - Proceed to final export
        2. Request revisions - Specify changes
        3. Regenerate specific modules
        
User: [Reviews draft_1_combined.md]
      The conclusion needs to be stronger
      
System: Would you like to:
        1. Regenerate Module 6 (Conclusion)
        2. Provide specific revision guidance
        3. Edit the file directly
        
User: 1

System: 🔄 Regenerating Module 6...
        [Regenerates with prompt: "Create a stronger, more impactful conclusion"]
        
        ✅ Module 6 regenerated
        📄 New file: modules/module_6_conclusion_v2.md
        
        Reassembling document...
        ✅ Draft 2 created: assembly/draft_2_revised.md
```

## 📊 Current Implementation vs. Required Architecture

### ✅ What EXISTS in Current Codebase

**File**: [src/planning/document_orchestrator.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\document_orchestrator.py)

- **InteractiveDocumentOrchestrator** class with human-in-the-loop hooks
- Callback-based review points (plan review, section review, final review)
- Specialized agents for different section types
- Parallel execution capabilities
- Shared context management

**Capabilities:**
```python
orchestrator = InteractiveDocumentOrchestrator(llm, tools, workspace)

result = orchestrator.generate_document_interactive(
    document_type="research_paper",
    title="My Document",
    requirements={...},
    review_callback=my_review_function  # Called at review points
)
```

### ❌ What's MISSING (Critical Gap)

The current implementation uses **callback functions** but doesn't create **persistent visible markdown files** that users can:
1. Open in their text editor during generation
2. Watch update in real-time
3. Edit directly and reload
4. Track as version history

**Missing Components:**

#### 1. Persistent Plan Files
- Currently: Plan exists only in memory (JSON export optional)
- Needed: Markdown plan files at `planning/N_plan_description.md`
- User Impact: Can't review/edit plan in readable format

#### 2. Real-Time Module Progress Files
- Currently: Console output only
- Needed: `modules/module_N_title.md` files that update during generation
- User Impact: Can't see progress or partial content

#### 3. Live Progress Dashboard
- Currently: No persistent progress tracking
- Needed: `progress/current_progress.md` that updates every few seconds
- User Impact: Can't monitor overall progress without watching console

#### 4. Assembly Drafts with Versions
- Currently: Final output only
- Needed: `assembly/draft_N_type.md` files for each assembly stage
- User Impact: Can't review intermediate combinations or track revisions

#### 5. Interactive File-Based Control
- Currently: Requires programmatic callbacks
- Needed: User edits markdown files → system detects → reloads automatically
- User Impact: Must use API/code instead of natural file editing

## 🛠️ Integration Strategy

### Option 1: Enhance InteractiveDocumentOrchestrator (Recommended)

Add persistent file tracking to the existing interactive orchestrator:

```python
class InteractiveDocumentOrchestrator(DocumentOrchestrator):
    def __init__(self, llm_provider, tool_orchestrator, base_sandbox_path):
        super().__init__(llm_provider, tool_orchestrator, base_sandbox_path)
        
        # ADD: Persistent planner
        from src.planning.persistent_planner import create_persistent_planner
        self.persistent_planner = create_persistent_planner(
            Path(base_sandbox_path)
        )
    
    def generate_document_interactive(self, ...):
        # MODIFY: Create visible plan file
        plan_result = self.persistent_planner.create_initial_plan(
            topic=title,
            word_count=requirements['total_word_count'],
            document_type=document_type
        )
        
        # MODIFY: Wait for user approval via file or command
        user_action = self._wait_for_user_approval(plan_result['plan_file'])
        
        if user_action == 'updated':
            # Reload modified plan from file
            plan = self._reload_plan_from_file(plan_result['plan_file'])
        
        # MODIFY: Create module planning files
        module_files = self.persistent_planner.create_module_plans(plan.sections)
        
        # MODIFY: Update module files during generation
        for i, section in enumerate(plan.sections):
            self.persistent_planner.update_module_status(
                module_order=i+1,
                status='generating'
            )
            
            output = self._execute_section(section, plan)
            
            self.persistent_planner.update_module_status(
                module_order=i+1,
                status='complete',
                content=output['content'],
                quality_score=output['quality_score']
            )
        
        # MODIFY: Save assembly drafts
        draft_1 = self.assembler.assemble_document(section_outputs, ...)
        self.persistent_planner.save_assembly_draft(draft_1, "combined")
        
        # ... continue with review and revision
```

### Option 2: Use PersistentPlanner Directly

Replace the memory-only planning with persistent file-based planning:

```python
# In graive.py generate_document() method:

if self.document_planner and self.persistent_planner:
    # Stage 1: Create visible plan
    plan_result = self.persistent_planner.create_initial_plan(
        topic=topic,
        word_count=word_count,
        document_type=document_type,
        include_images=include_images,
        include_tables=include_tables
    )
    
    # Stage 2: Wait for approval
    print("\n⏸️  Waiting for user action...")
    print("Type 'approve' to start, 'updated' to reload modified plan, or 'cancel' to abort")
    
    # [Implementation would need interactive input handling]
```

## 🎯 Required Implementation Steps

### Step 1: Integrate PersistentPlanner into InteractiveDocumentOrchestrator

**File to Modify**: [src/planning/document_orchestrator.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\document_orchestrator.py)

Add persistent planner initialization and use it throughout the interactive workflow.

### Step 2: Create File-Watching Mechanism

Implement file watcher that detects when user edits planning/module files:

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PlanFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('_plan.md'):
            print(f"⚠️  Plan file modified: {event.src_path}")
            print("Type 'reload' to apply changes")
```

### Step 3: Add Real-Time Progress Updates

Create background thread that updates `progress/current_progress.md` every 5 seconds during generation.

### Step 4: Implement Interactive Input Handling

Add proper input handling in graive.py interactive mode to support:
- `approve` - Start generation
- `updated` - Reload modified plan
- `stop` - Pause generation
- `continue` - Resume
- `modify` - Edit current module
- `cancel` - Abort

### Step 5: Version Tracking

Implement automatic version tracking for:
- Plans (1_initial_plan.md, 2_plan_v2.md, ...)
- Modules (module_2_v1.md, module_2_v2.md, ...)
- Drafts (draft_1_combined.md, draft_2_revised.md, ...)

## 🚀 Expected User Experience After Implementation

```
User: write a 12000 word research paper about climate change in africa

Graive AI: I'll create a strategic plan for this research paper.

📋 CREATING STRATEGIC PLAN
Topic: climate change in africa
Type: research_paper
Target Words: 12,000
======================================================================

✅ PLAN CREATED
📄 File: 1_initial_plan.md
📍 Location: workspace/session_20251026_145623/planning/1_initial_plan.md
📊 Modules: 6

======================================================================
⏸️  WAITING FOR USER APPROVAL
======================================================================
Please review the plan at: planning/1_initial_plan.md

Options:
  1. Type 'approve' to proceed with generation
  2. Edit 1_initial_plan.md and type 'updated' to reload
  3. Type 'cancel' to abort
======================================================================

User: [Opens planning/1_initial_plan.md in VS Code, reviews structure]
      approve

Graive AI: 🚀 Starting generation with 6 modules...

📋 Creating module planning files...
   ✅ Created: module_1_introduction.md
   ✅ Created: module_2_literature_review.md
   ✅ Created: module_3_methodology.md
   ✅ Created: module_4_results.md
   ✅ Created: module_5_discussion.md
   ✅ Created: module_6_conclusion.md

✅ All 6 module plans created

💡 TIP: Open progress/current_progress.md to monitor generation in real-time

[Module 1/6] Generating: Introduction
                Target: 1,800 words
                Status: Generating...
                Progress: 25% (450 words)...
                Progress: 50% (900 words)...
                Progress: 75% (1,350 words)...
                ✅ Complete: 1,825 words
                Quality: 8.4/10

[Module 2/6] Generating: Literature Review
                Target: 2,400 words
                Status: Generating...
                Progress: 30% (720 words)...

User: stop

Graive AI: ⏸️  PAUSED at Module 2 (720/2,400 words - 30%)

Options:
  1. continue - Resume generation
  2. modify - Edit module requirements
  3. restart - Regenerate from start
  4. cancel - Abort

User: modify

Graive AI: Please edit: modules/module_2_literature_review.md
          Type 'ready' when done

User: [Adds requirement: "Include more studies from 2020-2024"]
      ready

Graive AI: ✅ Changes detected
          Restarting Module 2 with updated requirements...
          
[Module 2/6] Generating: Literature Review (v2)
                Target: 2,400 words
                New focus: Recent studies 2020-2024
                Status: Generating...
                ✅ Complete: 2,387 words
                Quality: 8.7/10

[... continues through all modules ...]

✅ ALL MODULES COMPLETE

📝 ASSEMBLING DOCUMENT
   Combining 6 modules...
   Total words: 11,942
   ✅ Draft 1 created: assembly/draft_1_combined.md

Please review draft_1_combined.md

Type 'approve' to finalize or provide revision feedback

User: approve

Graive AI: ✅ DOCUMENT GENERATION COMPLETE
          📄 Final: climate_change_in_africa_20251026_150842.md
          📍 Location: workspace/session_20251026_145623/documents/
          📊 Words: 11,942
          🎓 Quality: 8.5/10 average
          ⏱️  Time: 12 minutes 34 seconds
```

## 📁 Complete Workspace Structure After Generation

```
workspace/session_20251026_145623/
├── planning/
│   ├── 1_initial_plan.md
│   ├── 2_plan_v2.md (if user modified)
│   └── 3_final_plan.md (approved version)
├── modules/
│   ├── module_1_introduction.md (✅ Complete)
│   ├── module_2_literature_review.md (✅ Complete, v2 after modification)
│   ├── module_3_methodology.md (✅ Complete)
│   ├── module_4_results.md (✅ Complete)
│   ├── module_5_discussion.md (✅ Complete)
│   └── module_6_conclusion.md (✅ Complete)
├── assembly/
│   ├── draft_1_combined.md
│   ├── draft_2_revised.md (if revisions requested)
│   ├── draft_3_final.md (approved version)
│   └── verification_report.md
├── progress/
│   └── current_progress.md (final state: 100% complete)
├── documents/
│   └── climate_change_in_africa_20251026_150842.md (FINAL OUTPUT)
└── images/ (if generated)
    └── [generated images]
```

## Status Summary

### ✅ Implemented
- Persistent planning module ([persistent_planner.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\persistent_planner.py))
- Document orchestrator with callbacks
- Specialized agents
- Plan creation and export
- Section-by-section execution

### ⚠️ Needs Integration
- Connect PersistentPlanner to InteractiveDocumentOrchestrator
- Add file-based user approval workflow
- Implement real-time progress file updates
- Add file modification detection
- Create interactive input handling in graive.py

### 🎯 Next Step

Modify [InteractiveDocumentOrchestrator](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\document_orchestrator.py#L460-L592) to use [PersistentPlanner](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\persistent_planner.py) for all planning artifacts, enabling the complete visible file-based workflow you described.

This is the TRUE architecture of the original Graive - transparent, interruptible, version-controlled document generation with complete user visibility and control.
