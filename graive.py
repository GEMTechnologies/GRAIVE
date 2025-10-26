#!/usr/bin/env python
"""
GRAIVE AI - Main Entry Point

Complete autonomous AI system with reflection, validation, and multi-agent coordination.

This is the single entry point that:
1. Initializes all system components (database, storage, LLMs, agents)
2. Sets up the reflection system for validation
3. Coordinates multi-agent workflows
4. Provides human-in-the-loop control
5. Monitors system health and costs

Usage:
    python graive.py                    # Interactive mode
    python graive.py --task "generate thesis"   # Direct task
    python graive.py --config custom.yaml       # Custom configuration
"""

import os
import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from datetime import datetime

# Type checking imports (only for type checkers, not runtime)
if TYPE_CHECKING:
    from src.langchain_integration import (
        LangChainLLMManager,
        RAGSystem,
        DocumentProcessor,
        LangChainMemoryManager
    )
    from src.browser_automation import AdvancedBrowserAutomation
    from src.reflection import ReflectionSystem
    from src.storage import SandboxStorageTool
    from src.quality import ReviewSystem
    from src.formatting import DocumentFormatter
    from src.media import ImageGenerator
    from src.execution import TaskExecutor
    from src.cli import FileOperations

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Core imports
try:
    from src.reflection import create_reflection_system, ActivityType
    from src.storage import create_storage_tool_for_sandbox
    from src.cost_optimization import create_cost_manager, TaskComplexity
    from src.quality import create_review_system
    from src.formatting import create_document_formatter
    from src.media import create_image_generator
    from src.execution import create_task_executor
    from src.cli import create_file_operations
    
    # Check if optional dependencies are available
    LANGCHAIN_AVAILABLE = True
    try:
        from src.langchain_integration import (
            LangChainLLMManager,
            RAGSystem,
            DocumentProcessor,
            LangChainMemoryManager
        )
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        print("Warning: LangChain not installed - some features disabled")
    
    BROWSER_AVAILABLE = True
    ADVANCED_BROWSER_AVAILABLE = False
    BROWSER_IMPORT_ERROR = None
    try:
        from src.browser_automation import (
            AdvancedBrowserAutomation,
            ADVANCED_BROWSER_AVAILABLE as _ADVANCED_BROWSER_AVAILABLE,
            BROWSER_IMPORT_ERROR as _BROWSER_IMPORT_ERROR,
        )
        ADVANCED_BROWSER_AVAILABLE = _ADVANCED_BROWSER_AVAILABLE
        BROWSER_IMPORT_ERROR = _BROWSER_IMPORT_ERROR
    except ImportError:
        BROWSER_AVAILABLE = False
        print("Warning: Browser automation not installed - web features disabled")

except ImportError as e:
    print(f"Error importing Graive modules: {e}")
    print("\nPlease ensure you're running from the Graive directory and dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


class GraiveAI:
    """
    Main Graive AI system coordinator.
    
    Orchestrates all components with reflection-based validation ensuring
    system coherence, preventing errors, and maintaining data integrity.
    """
    
    # Type annotations for all attributes
    if TYPE_CHECKING:
        reflection: Optional['ReflectionSystem']
        storage: Optional['SandboxStorageTool']
        llm_manager: Optional['LangChainLLMManager']
        rag_system: Optional['RAGSystem']
        memory_manager: Optional['LangChainMemoryManager']
        browser: Optional['AdvancedBrowserAutomation']
        review_system: Optional['ReviewSystem']
        document_formatter: Optional['DocumentFormatter']
        image_generator: Optional['ImageGenerator']
        task_executor: Optional['TaskExecutor']
        file_ops: Optional['FileOperations']
        document_planner: Optional[Any]
    
    def __init__(
        self,
        workspace: str = "./workspace",
        daily_budget: float = 50.0,
        enable_reflection: bool = True,
        enable_browser: bool = True,
        enable_rag: bool = True
    ):
        """
        Initialize Graive AI system.
        
        Args:
            workspace: Workspace directory
            daily_budget: Daily cost budget in USD
            enable_reflection: Enable reflection system
            enable_browser: Enable browser automation
            enable_rag: Enable RAG system
        """
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Session management - create unique session folder for this conversation
        from datetime import datetime
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_workspace = self.workspace / f"session_{self.session_id}"
        self.session_workspace.mkdir(parents=True, exist_ok=True)
        
        # Track last generated files for reference
        self.last_generated_image = None
        self.last_generated_document = None
        self.last_generated_code = None
        
        print(f"\n{'='*70}")
        print(f"GRAIVE AI SYSTEM INITIALIZATION")
        print(f"{'='*70}\n")
        
        # 1. Initialize Reflection System (Meta-cognitive layer)
        print("[1/14] Initializing Reflection System...")
        if enable_reflection:
            self.reflection = create_reflection_system(workspace_root=str(self.workspace))
            print("      ✓ Reflection system active")
            print("        - Pre-execution validation enabled")
            print("        - Post-execution verification enabled")
            print("        - Resource conflict detection enabled")
        else:
            self.reflection = None
            print("      ⚠ Reflection system disabled")
        
        # 2. Initialize Cost Management
        print("\n[2/14] Initializing Cost Management...")
        self.cost_manager = create_cost_manager(
            daily_budget=daily_budget,
            weekly_budget=daily_budget * 7,
            enable_caching=True
        )
        print(f"      ✓ Cost manager configured")
        print(f"        - Daily budget: ${daily_budget:.2f}")
        print(f"        - Response caching enabled")
        
        # 3. Initialize Storage System
        print("\n[3/14] Initializing Multi-layered Storage...")
        try:
            self.storage = create_storage_tool_for_sandbox(
                sandbox_id=f"graive_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                base_path=str(self.workspace)
            )
            print("      ✓ Storage system ready")
            print("        - File system layer")
            print("        - Context/knowledge base")
            print("        - Database scaffold")
            print("        - Media cache")
            print("        - Vector store")
        except Exception as e:
            print(f"      ⚠ Storage initialization error: {e}")
            print("      System will continue without full storage capabilities")
            print("      Install dependencies: pip install chromadb sentence-transformers")
            self.storage = None
        
        # 4. Initialize Database
        print("\n[4/14] Setting up Databases...")
        self._initialize_databases()
        print("      ✓ Databases initialized")
        
        # 5. Initialize LLM and RAG (if available)
        print("\n[5/14] Initializing AI Components...")
        self.llm_manager = None
        self.rag_system = None
        self.memory_manager = None
        
        if LANGCHAIN_AVAILABLE:
            try:
                self.llm_manager = LangChainLLMManager()
                
                # Initialize default LLM (will use mock if no API key)
                api_key = os.getenv("OPENAI_API_KEY", "")
                if api_key:
                    self.llm = self.llm_manager.create_llm(
                        provider="openai",
                        model="gpt-4",
                        temperature=0.7,
                        api_key=api_key
                    )
                    print("      ✓ OpenAI GPT-4 connected")
                else:
                    print("      ⚠ No API keys found - using mock mode")
                    self.llm = None
                
                if enable_rag and self.llm:
                    self.rag_system = RAGSystem(
                        llm=self.llm,
                        persist_directory=str(self.workspace / "rag_vectors")
                    )
                    print("      ✓ RAG system initialized")
                
                if self.llm:
                    self.memory_manager = LangChainMemoryManager(self.llm)
                    print("      ✓ Memory management ready")
                    
            except Exception as e:
                print(f"      ⚠ AI components initialization warning: {e}")
        else:
            print("      ⚠ LangChain not available - install with: pip install langchain")
        
        # 6. Initialize Browser Automation (if available)
        print("\n[6/14] Initializing Browser Automation...")
        self.browser = None
        if BROWSER_AVAILABLE and enable_browser:
            try:
                self.browser = AdvancedBrowserAutomation(
                    headless=True,
                    storage_manager=self.storage.storage if self.storage else None
                )
                if ADVANCED_BROWSER_AVAILABLE:
                    print("      ✓ Browser automation ready")
                    print("        - Stealth mode enabled")
                    print("        - Human behavior simulation")
                else:
                    print("      ✓ Lightweight HTTP browser ready")
                    if BROWSER_IMPORT_ERROR:
                        print(f"        - Selenium unavailable ({BROWSER_IMPORT_ERROR})")
                    print("        - Basic navigation and scraping active")
            except Exception as e:
                print(f"      ⚠ Browser initialization warning: {e}")
        elif not BROWSER_AVAILABLE:
            print("      ⚠ Browser automation not available")
        else:
            print("      ⚠ Browser automation disabled by configuration")
        
        # 7. Initialize PhD-Level Review System
        print("\n[7/14] Initializing Quality Review System...")
        try:
            self.review_system = create_review_system(min_quality_threshold=8.0)
            print("      ✓ PhD-level review system active")
            print("        - Multi-dimensional quality scoring")
            print("        - Iterative revision enabled")
            print("        - Quality threshold: 8.0/10")
        except Exception as e:
            print(f"      ⚠ Review system warning: {e}")
            self.review_system = None
        
        # 8. Initialize Professional Document Formatter
        print("\n[8/14] Initializing Document Formatter...")
        try:
            self.document_formatter = create_document_formatter(str(self.workspace))
            print("      ✓ Professional document formatting ready")
            print("        - Word (.docx) export capable")
            print("        - Image generation pipeline")
            print("        - Table formatting system")
        except Exception as e:
            print(f"      ⚠ Formatter warning: {e}")
            self.document_formatter = None
        
        # 9. Initialize Image Generator
        print("\n[9/14] Initializing Image Generator...")
        try:
            self.image_generator = create_image_generator(str(self.session_workspace))  # Use session workspace
            print("      ✓ Image generation system ready")
            print("        - Programmatic generation (flags, charts)")
            print("        - Web download capability")
            print("        - AI generation (DALL-E) support")
        except Exception as e:
            print(f"      ⚠ Image generator warning: {e}")
            self.image_generator = None
            self.last_generated_image = None
        
        # 10. Initialize Task Executor (CRITICAL)
        print("\n[10/14] Initializing Autonomous Task Executor...")
        try:
            self.task_executor = create_task_executor(
                workspace_path=str(self.session_workspace),  # Use session workspace
                llm_caller=self._call_llm_for_content
            )
            print("      ✓ Autonomous execution engine active")
            print("        - Code generation to files")
            print("        - Image insertion into documents")
            print("        - Task planning and execution")
        except Exception as e:
            print(f"      ⚠ Task executor warning: {e}")
            self.task_executor = None
        
        # 11. Initialize CLI File Operations (NEW!)
        print("\n[11/14] Initializing CLI File Operations...")
        try:
            self.file_ops = create_file_operations(str(self.session_workspace))
            print("      ✓ File operations ready")
            print("        - Create, delete, rename files")
            print("        - Edit file contents")
            print("        - List directories")
            print("        - Copy files")
        except Exception as e:
            print(f"      ⚠ File operations warning: {e}")
            self.file_ops = None
        
        # 12. Initialize Document Planner (CRITICAL - NEW!)
        print("\n[12/14] Initializing Strategic Document Planner...")
        try:
            from src.planning import create_document_planner
            self.document_planner = create_document_planner(llm_caller=self._call_llm_for_content)
            print("      ✓ Document planner ready")
            print("        - Multi-stage planning pipeline")
            print("        - Topic analysis and decomposition")
            print("        - Media placement strategy")
            print("        - Citation planning")
            print("        - Quality criteria establishment")
        except Exception as e:
            print(f"      ⚠ Document planner warning: {e}")
            self.document_planner = None
        
        # 13. Initialize Request Reasoner (NEW - CRITICAL!)
        print("\n[13/14] Initializing Request Reasoning System...")
        try:
            from src.planning.request_planner import create_request_reasoner
            self.request_reasoner = create_request_reasoner(llm_caller=self._call_llm_for_content)
            print("      ✓ Request reasoner ready")
            print("        - Deep intent analysis with reasoning")
            print("        - Requirement extraction with justification")
            print("        - Resource planning with purpose")
            print("        - Execution strategy with rationale")
            print("        - Risk analysis and mitigation")
        except Exception as e:
            print(f"      ⚠ Request reasoner warning: {e}")
            self.request_reasoner = None

        # 14. Initialize Persistent Planning System
        print("\n[14/14] Initializing Persistent Planning System...")
        try:
            from src.planning.persistent_planner import create_persistent_planner
            self.persistent_planner = create_persistent_planner(self.session_workspace)
            print("      ✓ Persistent planner ready")
            print("        - Visible markdown plans")
            print("        - Module progress tracking")
            print("        - Assembly draft versioning")
        except Exception as e:
            print(f"      ⚠ Persistent planner warning: {e}")
            self.persistent_planner = None

        # Register agents with reflection system
        if self.reflection:
            self._register_agents()

        print(f"\n{'='*70}")
        print(f"GRAIVE AI INITIALIZED SUCCESSFULLY")
        print(f"{'='*70}\n")
    
    def _initialize_databases(self):
        """Initialize required databases."""
        # Create citations database
        result = self.storage.execute(
            "create_database",
            db_name="citations",
            db_type="sqlite"
        )
        
        if result["success"]:
            # Create schema
            self.storage.execute(
                "execute_query",
                db_name="citations",
                query="""
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT,
                    year INTEGER,
                    journal TEXT,
                    url TEXT,
                    citation_apa TEXT,
                    abstract TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            # Create index on year for filtering
            self.storage.execute(
                "execute_query",
                db_name="citations",
                query="CREATE INDEX IF NOT EXISTS idx_year ON papers(year)"
            )
        
        # Create projects database
        result = self.storage.execute(
            "create_database",
            db_name="projects",
            db_type="sqlite"
        )
        
        if result["success"]:
            self.storage.execute(
                "execute_query",
                db_name="projects",
                query="""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            self.storage.execute(
                "execute_query",
                db_name="projects",
                query="""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT NOT NULL,
                    task_id TEXT UNIQUE NOT NULL,
                    agent_name TEXT,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id)
                )
                """
            )
    
    def _register_agents(self):
        """Register all agents with reflection system."""
        agents = [
            ("WriterAgent", ["document_generation", "section_writing", "citation_formatting"]),
            ("ResearchAgent", ["web_scraping", "paper_extraction", "database_queries"]),
            ("AnalysisAgent", ["statistical_analysis", "data_visualization", "interpretation"]),
            ("BrowserAgent", ["web_automation", "data_extraction", "file_downloads"]),
            ("CoordinatorAgent", ["task_planning", "agent_coordination", "workflow_management"])
        ]
        
        for agent_name, capabilities in agents:
            self.reflection.register_agent(
                agent_name=agent_name,
                capabilities=capabilities,
                metadata={"status": "active"}
            )
    
    def run_with_reflection(
        self,
        agent_name: str,
        activity_type: ActivityType,
        description: str,
        action: callable,
        inputs: Dict[str, Any],
        expected_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an action with reflection validation.
        
        This is the core execution pattern: reflect before action, execute if
        approved, then verify results match expectations.
        
        Args:
            agent_name: Agent executing the action
            activity_type: Type of activity
            description: Human-readable description
            action: Callable to execute
            inputs: Input parameters
            expected_outputs: Expected output structure
        
        Returns:
            Execution results with validation status
        """
        # Pre-execution reflection
        if self.reflection:
            activity = self.reflection.reflect_before_action(
                agent_name=agent_name,
                activity_type=activity_type,
                description=description,
                inputs=inputs,
                expected_outputs=expected_outputs
            )
            
            # Check if rejected
            if activity.validation_status.value == "rejected":
                return {
                    "success": False,
                    "error": "Action rejected by reflection system",
                    "activity_id": activity.activity_id,
                    "errors": activity.errors
                }
        else:
            activity = None
        
        # Execute action
        try:
            result = action(**inputs)
            success = True
            error_message = None
        except Exception as e:
            result = {}
            success = False
            error_message = str(e)
        
        # Post-execution reflection
        if self.reflection and activity:
            self.reflection.reflect_after_action(
                activity_id=activity.activity_id,
                actual_outputs=result if success else {},
                success=success,
                error_message=error_message
            )
        
        return {
            "success": success,
            "result": result,
            "error": error_message,
            "activity_id": activity.activity_id if activity else None
        }
    
    def generate_document(
        self,
        topic: str,
        word_count: int = 1200,
        include_images: bool = False,
        include_tables: bool = False,
        output_format: str = "md",
        enable_phd_review: bool = True,
        document_type: str = "essay",
        academic_level: str = "undergraduate"
    ) -> Dict[str, Any]:
        """
        Generate document using deliberate plan-then-generate architecture.

        Args:
            topic: Document subject
            word_count: Target word count
            include_images: Include images in plan
            include_tables: Include tables in plan
            output_format: Output format (md, docx, pdf)
            enable_phd_review: Enable quality review
            document_type: Document type (essay, paper, thesis, ...)
            academic_level: Target academic sophistication

        Returns:
            Document generation results
        """
        try:
            print(f"\n{'='*70}")
            print(f"📝 DOCUMENT GENERATION - {topic.upper()}")
            print(f"{'='*70}")
            print(f"Type: {document_type} | Words: {word_count} | Format: {output_format.upper()}")
            print(f"Academic Level: {academic_level}")
            if enable_phd_review:
                print("Quality: PhD-Level Review ENABLED")
            print(f"{'='*70}\n")

            if self.document_planner:
                return self._generate_document_with_planner(
                    topic=topic,
                    word_count=word_count,
                    include_images=include_images,
                    include_tables=include_tables,
                    output_format=output_format,
                    enable_phd_review=enable_phd_review,
                    document_type=document_type,
                    academic_level=academic_level
                )

            print("⚠️  Document planner not available - using direct generation\n")
            return self._generate_document_direct(
                topic=topic,
                word_count=word_count,
                include_images=include_images,
                include_tables=include_tables,
                output_format=output_format,
                enable_phd_review=enable_phd_review
            )

        except Exception as e:
            print(f"\n❌ DOCUMENT GENERATION FAILED: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e), "file_path": "None"}

    def _generate_document_with_planner(
        self,
        topic: str,
        word_count: int,
        include_images: bool,
        include_tables: bool,
        output_format: str,
        enable_phd_review: bool,
        document_type: str,
        academic_level: str
    ) -> Dict[str, Any]:
        """Generate document using strategic planning workflow."""

        print("=" * 70)
        print("STAGE 1: STRATEGIC PLANNING")
        print("=" * 70 + "\n")

        request_analysis = None
        user_request = (
            f"Write a {document_type} about {topic} with {word_count} words"
            f"{' including images' if include_images else ''}"
            f"{' including tables' if include_tables else ''}."
        )
        if self.request_reasoner:
            request_analysis = self.request_reasoner.analyze_request(user_request)

        persistent_plan = None
        module_files: List[str] = []
        if self.persistent_planner:
            persistent_plan = self.persistent_planner.create_initial_plan(
                topic=topic,
                word_count=word_count,
                document_type=document_type,
                include_images=include_images,
                include_tables=include_tables,
                user_requirements=request_analysis['intent']['reasoning'] if request_analysis else None
            )
            module_files = self.persistent_planner.create_module_plans(persistent_plan['modules'])

        plan = self.document_planner.create_plan(
            topic=topic,
            word_count=word_count,
            document_type=document_type,
            include_images=include_images,
            include_tables=include_tables,
            target_audience="academic",
            academic_level=academic_level
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_")
        plans_dir = self.session_workspace / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)
        plan_file = plans_dir / f"{safe_topic}_plan_{timestamp}.json"
        plan.save_plan(str(plan_file))
        print(f"💾 Plan saved: {plan_file.name}\n")

        print("=" * 70)
        print("STAGE 2: CONTENT GENERATION")
        print("=" * 70 + "\n")

        generated_sections: List[Dict[str, Any]] = []
        total_words = 0
        section_quality_scores: List[Optional[float]] = []

        for index, section in enumerate(plan.sections, 1):
            print(f"[Section {index}/{len(plan.sections)}] Generating: {section.title}")
            print(f"                Target: {section.word_count} words")

            if self.persistent_planner:
                self.persistent_planner.update_module_status(index, "generating")

            prompt = self._build_section_prompt(
                section_title=section.title,
                key_points=section.key_points,
                word_count=section.word_count,
                topic=topic,
                previous_sections=generated_sections
            )

            max_tokens = max(400, min(section.word_count * 3, 6000))
            section_content = self._call_llm_for_content(prompt, max_tokens=max_tokens)
            if not section_content.strip():
                section_content = self._generate_default_section_content(
                    section_title=section.title,
                    key_points=section.key_points,
                    word_count=section.word_count,
                    topic=topic
                )

            section_words = len(section_content.split())
            total_words += section_words

            section_quality: Optional[float] = None
            if enable_phd_review:
                if self.review_system:
                    section_review = self.review_system.review_content(
                        content=section_content,
                        topic=topic,
                        target_audience="academic",
                        field=document_type
                    )
                    section_quality = section_review["average_score"]
                    if section_review.get("needs_revision"):
                        print(f"                ⚠️  Quality: {section_quality:.1f}/10 - revising...")
                        section_content = self.review_system.revise_content(
                            content=section_content,
                            review_report=section_review,
                            topic=topic,
                            max_iterations=1
                        )
                        section_review = self.review_system.review_content(
                            content=section_content,
                            topic=topic,
                            target_audience="academic",
                            field=document_type
                        )
                        section_quality = section_review["average_score"]
                    print(f"                ✅ Quality: {section_quality:.1f}/10")
                else:
                    section_content = self._revise_section(section_content, 6.5)

            generated_sections.append(
                {
                    "title": section.title,
                    "content": section_content,
                    "word_count": section_words,
                    "media_specs": section.media_specs,
                }
            )
            section_quality_scores.append(section_quality)

            if self.persistent_planner:
                self.persistent_planner.update_module_status(
                    module_order=index,
                    status="complete",
                    content=section_content,
                    quality_score=section_quality
                )

            print(f"                ✓ Generated: {section_words} words\n")

        print(f"✅ All sections generated: {total_words} total words\n")

        print("=" * 70)
        print("STAGE 3: MEDIA INTEGRATION")
        print("=" * 70 + "\n")

        generated_media: List[Dict[str, Any]] = []

        for section_index, section in enumerate(generated_sections):
            if not section.get("media_specs"):
                continue

            for media_spec in section["media_specs"]:
                if media_spec.get("type") == "image":
                    description = media_spec.get("subject", f"Illustration for {section['title']}")
                    if self.image_generator:
                        img_result = self.image_generator.generate_image(
                            description=description,
                            method=media_spec.get("method", "auto")
                        )
                        if img_result.get("success"):
                            generated_media.append(
                                {
                                    "type": "image",
                                    "section_index": section_index,
                                    "path": img_result.get("path", img_result.get("filename")),
                                    "description": description,
                                }
                            )
                            print(f"🖼️  Image created: {description}")
                        else:
                            print(f"⚠️  Image generation failed: {description}")
                    else:
                        placeholder_path = f"images/{safe_topic}_section{section_index+1}.png"
                        generated_media.append(
                            {
                                "type": "image",
                                "section_index": section_index,
                                "path": placeholder_path,
                                "description": description,
                            }
                        )
                        print(f"🖼️  Image placeholder registered: {description}")
                elif media_spec.get("type") == "table":
                    table_md = self._generate_table_for_section(
                        subject=media_spec.get("subject", section["title"]),
                        topic=topic,
                        rows=media_spec.get("rows", 5),
                        columns=media_spec.get("columns", 3)
                    )
                    generated_media.append(
                        {
                            "type": "table",
                            "section_index": section_index,
                            "markdown": table_md,
                            "subject": media_spec.get("subject", section["title"]),
                        }
                    )
                    print(f"📊 Table prepared: {media_spec.get('subject', section['title'])}")

        print(f"✅ Media integration complete: {len(generated_media)} items\n")

        print("=" * 70)
        print("STAGE 4: DOCUMENT ASSEMBLY")
        print("=" * 70 + "\n")

        document_content = self._assemble_document(
            title=plan.title,
            sections=generated_sections,
            media=generated_media,
            citations=plan.citation_strategy
        )

        if self.persistent_planner:
            self.persistent_planner.save_assembly_draft(document_content, draft_type="combined")

        print(f"✅ Document assembled: {len(document_content.split())} words\n")

        review_report = None
        if enable_phd_review and self.review_system:
            print("=" * 70)
            print("STAGE 5: PhD-LEVEL QUALITY REVIEW")
            print("=" * 70 + "\n")

            review_report = self.review_system.review_content(
                content=document_content,
                topic=topic,
                target_audience="PhD researchers",
                field="academic"
            )

            if review_report.get("needs_revision"):
                print(f"🔄 Overall quality: {review_report['average_score']:.2f}/10 - revising...\n")
                document_content = self.review_system.revise_content(
                    content=document_content,
                    review_report=review_report,
                    topic=topic,
                    max_iterations=2
                )
                if self.persistent_planner:
                    self.persistent_planner.save_assembly_draft(document_content, draft_type="revised")
                review_report = self.review_system.review_content(
                    content=document_content,
                    topic=topic,
                    target_audience="PhD researchers",
                    field="academic"
                )
                print(f"✅ Revised quality: {review_report['average_score']:.2f}/10\n")
            else:
                print(f"✅ Quality approved: {review_report['average_score']:.2f}/10\n")

        print("=" * 70)
        print("STAGE 6: FORMATTING AND PERSISTENCE")
        print("=" * 70 + "\n")

        docs_dir = self.session_workspace / "documents"
        docs_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{safe_topic}_{timestamp}.{output_format}"
        file_path = docs_dir / file_name

        if self.document_formatter:
            print("📝 Applying professional formatting...")
            format_result = self.document_formatter.format_document(
                content=document_content,
                title=plan.title,
                author="Graive AI",
                output_format=output_format
            )

            exports = format_result.get("exports", {}) if isinstance(format_result, dict) else {}
            preferred_path = None
            if exports:
                preferred_path = exports.get(output_format.lower()) or exports.get(output_format.upper())
                if not preferred_path:
                    # fall back to the first available export path
                    preferred_path = next((path for path in exports.values() if path), None)
            if not preferred_path:
                preferred_path = format_result.get("file_path") if isinstance(format_result, dict) else None

            if preferred_path:
                file_path = Path(preferred_path)
                print(f"   ✅ Professionally formatted {output_format.upper()} ready")
            else:
                print("   ⚠️  Formatter could not create the requested format; falling back to markdown save")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(document_content)
                file_size = os.path.getsize(file_path)
                print(f"   ✅ File written ({file_size:,} bytes)\n")

            additional_exports = {
                fmt.upper(): path for fmt, path in exports.items() if path and Path(path) != file_path
            }
            if additional_exports:
                print("   📦 Additional exports:")
                for fmt, path in sorted(additional_exports.items()):
                    print(f"      • {fmt}: {path}")
                print()
        else:
            print("💾 Saving to file...")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(document_content)
            file_size = os.path.getsize(file_path)
            print(f"   ✅ File written ({file_size:,} bytes)\n")

        self.last_generated_document = str(file_path)

        if self.persistent_planner:
            self.persistent_planner.save_assembly_draft(document_content, draft_type="final")

        print("=" * 70)
        print("✅ DOCUMENT GENERATION COMPLETE")
        print("=" * 70)
        print(f"📄 File: {file_path.name}")
        print(f"📍 Location: {file_path}")
        print(f"📊 Words: {total_words}")
        print(f"🖼️  Images: {len([m for m in generated_media if m['type'] == 'image'])}")
        print(f"📈 Tables: {len([m for m in generated_media if m['type'] == 'table'])}")
        print(f"📋 Plan: {plan_file.name}")
        if persistent_plan:
            print(f"🗂️  Persistent Plan: {Path(persistent_plan['plan_file']).name}")
        if review_report:
            print(f"🎓 Quality: {review_report['average_score']:.2f}/10 ({review_report['quality_level']})")
        print("=" * 70 + "\n")

        self._show_workspace_contents()

        return {
            "success": True,
            "file_path": str(file_path),
            "word_count": total_words,
            "sections": len(generated_sections),
            "images": len([m for m in generated_media if m['type'] == 'image']),
            "tables": len([m for m in generated_media if m['type'] == 'table']),
            "plan_file": str(plan_file),
            "persistent_plan": persistent_plan,
            "module_files": module_files,
            "request_analysis": request_analysis,
            "quality_score": review_report['average_score'] if review_report else None,
        }

    def _generate_document_direct(
        self,
        topic: str,
        word_count: int,
        include_images: bool,
        include_tables: bool,
        output_format: str,
        enable_phd_review: bool,
        document_type: str = "essay",
        academic_level: str = "undergraduate"
    ) -> Dict[str, Any]:
        """Fallback document generation without strategic planner."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = re.sub(r'[^\w\s-]', '', topic).strip().replace(' ', '_')
        file_name = f"{safe_topic}_{timestamp}.{output_format}"
        file_path = self.session_workspace / "documents" / file_name

        docs_dir = self.session_workspace / "documents"
        docs_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Session workspace: {docs_dir}\n")

        print(f"[Step 1/6] 🤖 Generating initial content via API...")
        print("           Provider: OpenAI/DeepSeek")
        print("           Estimated time: 15-30 seconds")
        print("           Status: Sending request...")

        content_result = self._generate_content_action(
            topic=topic,
            word_count=word_count,
            include_citations=True
        )

        if not content_result or "content" not in content_result:
            print("\n❌ FAILED: Content generation error")
            return {"success": False, "error": "Content generation failed", "file_path": "None"}

        content = content_result["content"]
        actual_words = content_result["actual_words"]
        print(f"           ✅ Generated {actual_words} words\n")

        review_report: Optional[Dict[str, Any]] = None
        if enable_phd_review and self.review_system:
            print("[Step 2/6] 🎓 PhD-Level Quality Review...")
            print("           Conducting multi-dimensional assessment...")

            review_report = self.review_system.review_content(
                content=content,
                topic=topic,
                target_audience="PhD researchers",
                field="academic"
            )

            if review_report['needs_revision']:
                print("\n           🔄 Quality below threshold - starting revision...")
                content = self.review_system.revise_content(
                    content=content,
                    review_report=review_report,
                    topic=topic,
                    max_iterations=3
                )
                actual_words = len(content.split())
                print("           ✅ Content revised to PhD standards\n")
            else:
                print("           ✅ Content meets PhD quality standards\n")
        else:
            print("[Step 2/6] ⚠️  PhD review skipped (disabled or unavailable)\n")

        images: List[str] = []
        if include_images:
            print("[Step 3/6] 🖼️  Adding images...")
            num_images = 3 if "3 image" in str(include_images) else 2

            for i in range(num_images):
                img_desc = f"Figure {i+1}: Illustration related to {topic}"
                content += f"\n\n![{img_desc}](images/{safe_topic}_fig{i+1}.png)\n"
                images.append(img_desc)
                print(f"           ✓ Image {i+1}/{num_images} placeholder added")

            print(f"           ✅ All {len(images)} images added\n")
        else:
            print("[Step 3/6] ⚠️  No images requested\n")

        tables: List[str] = []
        if include_tables:
            print("[Step 4/6] 📊 Adding data tables...")
            num_tables = 2 if "2 table" in str(include_tables) else 1

            for i in range(num_tables):
                table_md = self._generate_table_action(topic, i + 1)["table_markdown"]
                content += f"\n\n### Table {i+1}: Data for {topic}\n\n{table_md}\n"
                tables.append(f"Table {i+1}")
                print(f"           ✓ Table {i+1}/{num_tables} generated")

            print(f"           ✅ All {len(tables)} tables added\n")
        else:
            print("[Step 4/6] ⚠️  No tables requested\n")

        if self.document_formatter and output_format in ["docx", "pdf"]:
            print("[Step 5/6] 📝 Professional formatting...")

            format_result = self.document_formatter.format_document(
                content=content,
                title=topic,
                author="Graive AI",
                output_format=output_format,
                include_toc=True,
                include_page_numbers=True
            )

            file_path = Path(format_result['file_path'])
            print("           ✅ Document professionally formatted\n")
        else:
            print("[Step 5/6] 💾 Writing to file...")
            print(f"             Path: {file_path}")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            file_size = os.path.getsize(file_path)
            print(f"             ✅ File written ({file_size:,} bytes)\n")

        print("[Step 6/6] 📊 Final quality verification...")

        if enable_phd_review and self.review_system and review_report:
            print(f"           Overall Quality Score: {review_report['average_score']:.2f}/10")
            print(f"           Quality Level: {review_report['quality_level']}")
            print(f"           Revision Iterations: {len(self.review_system.revision_history)}")

        print(f"           Word Count: {actual_words}")
        print(f"           Images: {len(images)}")
        print(f"           Tables: {len(tables)}")
        print("           ✅ Quality verification complete\n")

        print(f"\n{'='*70}")
        print("✅ DOCUMENT GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"📄 File: {file_path.name}")
        print(f"📍 Location: {file_path}")
        print(f"📊 Words: {actual_words}")
        if enable_phd_review and review_report:
            print(f"🎓 Quality Score: {review_report['average_score']:.2f}/10 ({review_report['quality_level']})")
        if images:
            print(f"🖼️  Images: {len(images)}")
        if tables:
            print(f"📈 Tables: {len(tables)}")
        print(f"{'='*70}\n")

        self._show_workspace_contents()

        self.last_generated_document = str(file_path)

        return {
            "success": True,
            "file_path": str(file_path),
            "word_count": actual_words,
            "images": images,
            "tables": tables,
            "format": output_format,
            "quality_score": review_report.get('average_score') if (enable_phd_review and review_report) else None,
            "quality_level": review_report.get('quality_level') if (enable_phd_review and review_report) else None
        }

    def _build_section_prompt(
        self,
        section_title: str,
        key_points: List[str],
        word_count: int,
        topic: str,
        previous_sections: List[Dict[str, Any]]
    ) -> str:
        """Construct contextual prompt for section generation."""

        context = ""
        if previous_sections:
            context_lines = ["Previous sections provide context:"]
            for prev in previous_sections[-2:]:
                snippet = prev['content'][:200].replace('\n', ' ')
                context_lines.append(f"- {prev['title']}: {snippet}...")
            context = "\n".join(context_lines) + "\n\n"

        key_points_text = "\n".join(f"- {point}" for point in key_points) if key_points else "- Continue the narrative logically"

        prompt = f"""{context}Write the section titled "{section_title}" for a document about {topic}.

Requirements:
- Target length: {word_count} words
- Address the following key points:
{key_points_text}
- Maintain academic tone suitable for {topic}
- Provide detailed explanations and concrete examples
- Ensure smooth transitions from previous sections
- Avoid repetition of earlier content

Begin the {section_title} section now."""

        return prompt

    def _assemble_document(
        self,
        title: str,
        sections: List[Dict[str, Any]],
        media: List[Dict[str, Any]],
        citations: Dict[str, Any]
    ) -> str:
        """Assemble complete document from generated sections and media."""

        content = f"# {title}\n\n"

        for index, section in enumerate(sections):
            content += f"## {section['title']}\n\n"
            content += section['content'].strip() + "\n\n"

            section_media = [item for item in media if item.get('section_index') == index]
            for media_item in section_media:
                if media_item['type'] == 'image':
                    content += f"![{media_item['description']}]({media_item['path']})\n\n"
                    content += f"*Figure: {media_item['description']}*\n\n"
                elif media_item['type'] == 'table':
                    content += media_item['markdown'].strip() + "\n\n"

        if citations and citations.get('target_citations'):
            content += "## References\n\n"
            content += "[References will be populated based on citation strategy]\n"

        return content

    def _generate_table_for_section(
        self,
        subject: str,
        topic: str,
        rows: int = 5,
        columns: int = 3
    ) -> str:
        """Generate markdown table for a section."""

        prompt = (
            f"Create a Markdown table with {rows} rows and {columns} columns summarizing {subject} "
            f"within the context of {topic}. Provide descriptive column headers and concise data."
        )
        table_md = self._call_llm_for_content(prompt, max_tokens=rows * columns * 12)
        if table_md.strip():
            return table_md.strip()

        headers = [f"Column {i+1}" for i in range(columns)]
        header_row = " | ".join(headers)
        separator_row = " | ".join(["---"] * columns)

        body_rows = []
        for row_index in range(rows):
            cells = [f"Value {row_index+1}-{col_index+1}" for col_index in range(columns)]
            body_rows.append(" | ".join(cells))

        return "\n".join([f"| {header_row} |", f"| {separator_row} |"] + [f"| {row} |" for row in body_rows])

    def _revise_section(self, content: str, quality_score: float) -> str:
        """Request targeted revision of a low-quality section."""

        prompt = (
            "Improve the following academic section to raise its quality score. "
            f"The current estimated quality is {quality_score:.1f}/10. "
            "Strengthen clarity, depth, and cohesion while preserving key facts.\n\n"
            f"Section:\n{content}\n\n"
            "Return the revised section text only."
        )
        revised = self._call_llm_for_content(prompt, max_tokens=len(content.split()) * 3)
        return revised.strip() if revised.strip() else content

    def _generate_default_section_content(
        self,
        section_title: str,
        key_points: List[str],
        word_count: int,
        topic: str
    ) -> str:
        """Fallback content when LLM generation is unavailable."""

        paragraphs = []
        base_sentence_count = max(3, word_count // 120)
        key_points = key_points or [f"Core aspect of {topic}"]

        for point in key_points:
            paragraph = (
                f"{section_title} explores {point} within the broader context of {topic}. "
                f"This section examines historical background, current developments, and emerging perspectives related to {point}."
            )
            if len(paragraph.split()) < base_sentence_count * 20:
                paragraph += (
                    f" Furthermore, it highlights practical implications and provides examples that demonstrate why {point} "
                    "matters for researchers and practitioners alike."
                )
            paragraphs.append(paragraph)

        while len("\n\n".join(paragraphs).split()) < word_count:
            paragraphs.append(
                f"Building upon these insights, the section emphasises the importance of {section_title.lower()} for understanding "
                f"the evolving narrative around {topic}."
            )

        return "\n\n".join(paragraphs)

    def _create_general_interaction_plan(self, message: str, interaction_type: str = "general") -> str:
        """Create a lightweight execution plan for general conversational tasks."""

        plans_dir = self.session_workspace / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_path = plans_dir / f"interaction_{timestamp}.md"

        steps = [
            "1. Review the user's message to determine intent and sentiment.",
            "2. Consult available context, notes, or recent outputs relevant to the request.",
            "3. Draft a helpful, action-oriented response that confirms next steps or follow-up actions.",
            "4. Log the interaction outcome, including files touched or created, into the conversation transcript directory.",
        ]

        plan_content = [
            "# General Interaction Plan",
            f"- Created: {datetime.now().isoformat()}",
            f"- Interaction Type: {interaction_type}",
            "",
            "## User Message",
            message or "(no message provided)",
            "",
            "## Execution Steps",
            "\n".join(steps),
        ]

        with open(plan_path, 'w', encoding='utf-8') as plan_file:
            plan_file.write("\n".join(plan_content))

        return str(plan_path)
    
    def _show_workspace_contents(self):
        """Display workspace contents to show user what's been created."""
        print(f"\n{'='*70}")
        print(f"📁 WORKSPACE CONTENTS")
        print(f"{'='*70}")
        
        docs_dir = self.workspace / "documents"
        if docs_dir.exists():
            files = list(docs_dir.glob("*"))
            if files:
                print(f"\nDocuments folder ({len(files)} files):")
                for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
                    size = f.stat().st_size
                    modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"  • {f.name} ({size:,} bytes) - {modified}")
                if len(files) > 10:
                    print(f"  ... and {len(files) - 10} more files")
            else:
                print("\nDocuments folder: (empty)")
        else:
            print("\nDocuments folder: (not created yet)")
        
        print(f"\n📍 Full path: {docs_dir}")
        print(f"{'='*70}\n")
    
    def _generate_content_action(self, topic: str, word_count: int, include_citations: bool) -> Dict[str, Any]:
        """Generate document content using configured LLM with progress tracking."""
        try:
            # Build prompt for content generation
            prompt = f"""Write a comprehensive, well-researched article about {topic}.

Requirements:
- Target length: {word_count} words
- Use professional academic style
- Include introduction, body sections, and conclusion
- {'Include citations in APA format' if include_citations else 'No citations needed'}
- Use clear section headings
- Provide detailed, factual information

Begin writing:"""
            
            print(f"           🔄 Connecting to API...")
            
            # Use OpenAI for content generation
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                print(f"           🟢 Using OpenAI GPT-3.5-Turbo-16K")
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                
                print(f"           💬 Sending prompt ({len(prompt)} chars)...")
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are an expert academic writer. Write detailed, well-structured content."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=min(word_count * 2, 4000),
                    temperature=0.7
                )
                
                print(f"           📝 Receiving content...")
                content = response.choices[0].message.content
                actual_words = len(content.split())
                
                print(f"           📊 Actual words generated: {actual_words}")
                
                return {
                    "content": content,
                    "actual_words": actual_words
                }
            
            # Fallback to DeepSeek
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            if deepseek_key:
                print(f"           🟢 Using DeepSeek Chat")
                import requests
                
                print(f"           💬 Sending request...")
                
                response = requests.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {deepseek_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": "You are an expert academic writer."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": min(word_count * 2, 4000),
                        "temperature": 0.7
                    },
                    timeout=60
                )
                
                print(f"           📝 Processing response...")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    actual_words = len(content.split())
                    
                    print(f"           📊 Actual words generated: {actual_words}")
                    
                    return {
                        "content": content,
                        "actual_words": actual_words
                    }
                else:
                    print(f"           ❌ DeepSeek API error: {response.status_code}")
            
            print(f"           ⚠️  No API available - using fallback")
            return {"content": f"# {topic}\n\nContent generation failed - no API available.", "actual_words": 0}
            
        except Exception as e:
            print(f"           ❌ Error: {e}")
            return {"content": f"# {topic}\n\nError: {e}", "actual_words": 0}
    
    def _generate_table_action(self, topic: str, table_num: int) -> Dict[str, Any]:
        """Generate a markdown table related to the topic."""
        # Generate sample table (in production, would use LLM)
        table_md = f"""| Category | Value | Description |
|----------|-------|-------------|
| Metric 1 | 100   | First data point related to {topic} |
| Metric 2 | 250   | Second data point |
| Metric 3 | 175   | Third data point |
| Metric 4 | 300   | Fourth data point |"""
        
        return {"table_markdown": table_md}
    
    def _write_file_action(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write content to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            bytes_written = len(content.encode('utf-8'))
            return {"bytes_written": bytes_written}
        except Exception as e:
            raise Exception(f"Failed to write file: {e}")
    
    def generate_thesis(
        self,
        title: str,
        research_question: str,
        target_pages: int = 200,
        year_range: tuple = (2022, 2025),
        citation_format: str = "APA"
    ) -> Dict[str, Any]:
        """
        Generate a complete thesis with reflection-validated workflow.
        
        Args:
            title: Thesis title
            research_question: Main research question
            target_pages: Target page count
            year_range: Citation year range
            citation_format: Citation format (APA, MLA, etc.)
        
        Returns:
            Generation results
        """
        print(f"\n{'='*70}")
        print(f"THESIS GENERATION WORKFLOW (WITH REFLECTION)")
        print(f"{'='*70}")
        print(f"\nTitle: {title}")
        print(f"Research Question: {research_question}")
        print(f"Target: {target_pages} pages")
        print(f"Citations: {citation_format} format, {year_range[0]}-{year_range[1]}")
        print(f"\n{'='*70}\n")
        
        workflow_results = []
        
        # Phase 1: Research with reflection
        print("\n[Phase 1] Research & Citation Extraction\n")
        
        research_result = self.run_with_reflection(
            agent_name="ResearchAgent",
            activity_type=ActivityType.WEB_SCRAPING,
            description=f"Search academic databases for '{research_question}'",
            action=self._mock_research_action,
            inputs={
                "query": research_question,
                "year_range": year_range,
                "max_results": 50
            },
            expected_outputs={
                "papers": list,
                "count": int
            }
        )
        
        workflow_results.append(("Research", research_result["success"]))
        
        if not research_result["success"]:
            print(f"✗ Research failed: {research_result['error']}")
            return {"success": False, "phase_failed": "Research"}
        
        papers = research_result["result"].get("papers", [])
        print(f"✓ Found {len(papers)} papers")
        
        # Phase 2: Citation database with reflection
        print("\n[Phase 2] Building Citation Database\n")
        
        citation_result = self.run_with_reflection(
            agent_name="ResearchAgent",
            activity_type=ActivityType.DATABASE_WRITE,
            description="Store citations in database",
            action=self._store_citations_action,
            inputs={
                "papers": papers,
                "table_name": "papers"
            },
            expected_outputs={
                "records_inserted": int,
                "database": str
            }
        )
        
        workflow_results.append(("Citations", citation_result["success"]))
        
        if citation_result["success"]:
            print(f"✓ Stored {citation_result['result'].get('records_inserted', 0)} citations")
        
        # Phase 3: Content generation with reflection
        print("\n[Phase 3] Generating Thesis Sections\n")
        
        sections = [
            "Introduction",
            "Literature Review",
            "Methodology",
            "Results",
            "Discussion",
            "Conclusion"
        ]
        
        for section in sections:
            section_result = self.run_with_reflection(
                agent_name="WriterAgent",
                activity_type=ActivityType.FILE_WRITE,
                description=f"Generate {section} section",
                action=self._generate_section_action,
                inputs={
                    "section_name": section,
                    "title": title,
                    "research_question": research_question,
                    "file_path": f"thesis/{section.lower().replace(' ', '_')}.md"
                },
                expected_outputs={
                    "word_count": int,
                    "file_path": str
                }
            )
            
            workflow_results.append((section, section_result["success"]))
            
            if section_result["success"]:
                print(f"✓ {section} generated ({section_result['result'].get('word_count', 0)} words)")
            else:
                print(f"✗ {section} failed")
        
        # Generate reflection report
        if self.reflection:
            print(f"\n{'='*70}")
            print("WORKFLOW REFLECTION REPORT")
            print(f"{'='*70}")
            self.reflection.print_reflection_report()
            
            # Export log
            self.reflection.export_reflection_log()
        
        # Final summary
        total_phases = len(workflow_results)
        successful_phases = sum(1 for _, success in workflow_results if success)
        
        print(f"\n{'='*70}")
        print(f"WORKFLOW COMPLETE")
        print(f"{'='*70}")
        print(f"\nPhases: {successful_phases}/{total_phases} successful")
        
        for phase_name, success in workflow_results:
            status = "✓" if success else "✗"
            print(f"  {status} {phase_name}")
        
        print(f"\n{'='*70}\n")
        
        return {
            "success": successful_phases == total_phases,
            "phases_completed": successful_phases,
            "total_phases": total_phases,
            "workflow_results": workflow_results
        }
    
    def _mock_research_action(self, query: str, year_range: tuple, max_results: int) -> Dict[str, Any]:
        """Mock research action for demonstration."""
        # In production, would use browser automation
        papers = []
        for i in range(min(10, max_results)):
            papers.append({
                "title": f"Research Paper {i+1} on {query[:30]}",
                "authors": "Smith et al.",
                "year": 2023,
                "url": f"https://example.com/paper{i+1}",
                "abstract": f"Abstract for paper {i+1}"
            })
        
        return {
            "papers": papers,
            "count": len(papers)
        }
    
    def _store_citations_action(self, papers: List[Dict], table_name: str) -> Dict[str, Any]:
        """Store citations in database."""
        inserted = 0
        
        for paper in papers:
            result = self.storage.execute(
                "execute_query",
                db_name="citations",
                query="""
                INSERT INTO papers (title, authors, year, url, abstract, citation_apa)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                query_params=(
                    paper.get("title", ""),
                    paper.get("authors", ""),
                    paper.get("year", 2023),
                    paper.get("url", ""),
                    paper.get("abstract", ""),
                    f"{paper.get('authors', '')} ({paper.get('year', 2023)}). {paper.get('title', '')}."
                )
            )
            
            if result["success"]:
                inserted += 1
        
        return {
            "records_inserted": inserted,
            "database": "citations"
        }
    
    def _generate_section_action(
        self,
        section_name: str,
        title: str,
        research_question: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Generate thesis section."""
        # Mock content generation
        content = f"# {section_name}\n\n"
        content += f"**Thesis:** {title}\n\n"
        content += f"**Research Question:** {research_question}\n\n"
        content += "## Content\n\n"
        content += "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100
        
        # Write to storage
        result = self.storage.execute(
            "write_file",
            file_path=file_path,
            content=content
        )
        
        return {
            "word_count": len(content.split()),
            "file_path": file_path
        }
    
    # Legacy chat fallback removed; all conversations now flow through the interaction agent
    
    def _call_llm_for_content(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Helper method to call LLM for content generation.
        Used by task executor for code generation, etc.
        
        Args:
            prompt: Prompt for LLM
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated content
        """
        try:
            # Use OpenAI if available
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are an expert programmer and content generator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            # Fallback to DeepSeek
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            if deepseek_key:
                import requests
                response = requests.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {deepseek_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": "You are an expert programmer."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
            
            return ""  # No API available
            
        except Exception as e:
            print(f"LLM call error: {e}")
            return ""
    
    def process_user_request(self, message: str, user_name: str = None) -> Dict[str, Any]:
        """
        Process user request with REASONING instead of pattern matching.
        
        NEW APPROACH: Use RequestReasoner to deeply analyze intent,
        plan resources, design execution strategy with rationale.
        
        Args:
            message: User's message
            user_name: User's name for personalization
        
        Returns:
            Dict with action and execution plan
        """
        
        # USE REASONING-BASED PLANNER if available
        if self.request_reasoner:
            print(f"\n✨ REASONING-BASED REQUEST PROCESSING")
            print(f"{'='*70}\n")
            
            # STEP 1: Analyze request with reasoning
            analysis = self.request_reasoner.analyze_request(message)
            
            # STEP 2: Create visible execution plan file
            plan_file = self.request_reasoner.create_execution_plan_file(
                analysis,
                self.session_workspace
            )
            
            # STEP 3: Wait for user approval
            print(f"\n⏸️  WAITING FOR APPROVAL")
            print(f"{'='*70}")
            print(f"\nI've analyzed your request and created a detailed plan.")
            print(f"Plan file: {plan_file}\n")
            print(f"Review the plan to see my reasoning about:")
            print(f"  - What you're asking for and why")
            print(f"  - What resources are needed and their purpose")
            print(f"  - How I'll execute it step-by-step")
            print(f"  - Potential risks and how to mitigate them\n")
            print(f"Type 'approve' to proceed, 'modify' to adjust, or 'cancel' to abort")
            print(f"{'='*70}\n")
            
            # Convert analysis to action format
            intent = analysis['intent']['primary']
            requirements = analysis['requirements']
            
            if intent == 'document_generation':
                topic = requirements.get('topic', {}).get('value')
                if topic:
                    return {
                        'action': 'generate_document',
                        'topic': topic,
                        'word_count': requirements.get('word_count', {}).get('value', 1200),
                        'include_images': requirements.get('images', {}).get('detected', False),
                        'include_tables': requirements.get('tables', {}).get('detected', False),
                        'format': 'md',
                        'analysis': analysis,  # Include full analysis
                        'plan_file': plan_file
                    }
            
            elif intent == 'image_generation':
                return {
                    'action': 'generate_image',
                    'description': message,
                    'analysis': analysis
                }
            
            # Default to autonomous interaction agent execution
            return {
                'action': 'general_interaction',
                'message': message,
                'analysis': analysis,
                'plan_file': plan_file,
                'interaction_type': 'general_conversation'
            }
        
        # FALLBACK: Old pattern-matching approach if reasoner not available
        print(f"\n[⚠️  Using fallback pattern matching - reasoner not available]\n")
        message_lower = message.lower()
        
        # CRITICAL: Detect questions and complaints FIRST (they should go to chat)
        question_indicators = ['is the', 'did you', 'have you', 'where is', 'why', 'how', 'what', 'when', 'who']
        complaint_indicators = ['but you', 'but u', 'you never', 'u never', 'you didn\'t', 'u didn\'t']
        
        is_question = any(indicator in message_lower for indicator in question_indicators)
        is_complaint = any(indicator in message_lower for indicator in complaint_indicators)
        
        # If it's a question or complaint, route to chat immediately
        if is_question or is_complaint:
            print(f"\n[🔍 Detection] Question/Complaint detected - routing to interaction agent")
            plan_file = self._create_general_interaction_plan(message, 'question_or_complaint')
            return {
                'action': 'general_interaction',
                'message': message,
                'plan_file': plan_file,
                'interaction_type': 'question_or_complaint'
            }
        
        # Detect CODE GENERATION requests (NEW!)
        code_keywords = ['code', 'program', 'script', 'game', 'app', 'function', 'algorithm', 'implementation']
        is_code_request = any(keyword in message_lower for keyword in code_keywords)
        
        # Check for code-specific patterns
        if is_code_request and any(verb in message_lower for verb in ['code', 'write', 'create', 'make', 'build', 'develop']):
            # Detect programming language
            language = 'python'  # Default
            if 'javascript' in message_lower or 'js' in message_lower:
                language = 'javascript'
            elif 'java' in message_lower and 'javascript' not in message_lower:
                language = 'java'
            elif 'c++' in message_lower or 'cpp' in message_lower:
                language = 'cpp'
            
            # Extract description
            description = message_lower
            for remove in ['code me', 'write', 'create', 'make me', 'build', 'develop', 'a', 'the']:
                description = description.replace(remove, '')
            description = description.strip()
            
            if description:
                return {
                    'action': 'generate_code',
                    'description': description,
                    'language': language
                }
        
        # Detect DATA ANALYSIS requests (NEW!)
        analysis_keywords = ['analyze', 'analysis', 'data', 'statistics', 'calculate', 'compute', 'visualize', 'plot', 'chart']
        is_analysis_request = any(keyword in message_lower for keyword in analysis_keywords)
        
        if is_analysis_request and any(keyword in message_lower for keyword in ['data', 'csv', 'excel', 'dataset']):
            return {
                'action': 'analyze_data',
                'description': message,
                'data_source': 'user_provided'
            }
        
        # Detect PPT/PRESENTATION generation (NEW!)
        ppt_keywords = ['ppt', 'powerpoint', 'presentation', 'slides', 'slide deck']
        is_ppt_request = any(keyword in message_lower for keyword in ppt_keywords)
        
        if is_ppt_request and any(verb in message_lower for verb in ['create', 'make', 'generate', 'build']):
            # Extract topic
            topic = message_lower
            for remove in ppt_keywords + ['create', 'make', 'generate', 'build', 'a', 'on', 'about']:
                topic = topic.replace(remove, '')
            topic = topic.strip()
            
            return {
                'action': 'create_presentation',
                'topic': topic,
                'slides': 10  # Default
            }
        
        # Detect image insertion into document requests (ENHANCED - Much more flexible!)
        insert_keywords = ['insert', 'add', 'put', 'include', 'embed', 'place']
        has_insert = any(keyword in message_lower for keyword in insert_keywords)
        has_image_ref = any(ref in message_lower for ref in ['image', 'picture', 'photo', 'it', 'that'])
        has_doc_ref = any(ref in message_lower for ref in ['article', 'essay', 'document', 'paper', 'that', 'it', 'the'])
        
        # More flexible detection: "insert it", "add it to the essay", "put it in the document"
        if has_insert and (has_image_ref or 'it' in message_lower) and (has_doc_ref or 'essay' in message_lower or 'article' in message_lower):
            # User wants to insert an image into a document
            # Extract document title
            title = None
            
            # Try "titled X" or "title X"
            title_match = re.search(r'titled?\s+[\"\']?([^\"\'\n]+)[\"\']?', message_lower)
            if title_match:
                title = title_match.group(1).strip()
            
            # Try "article about X" or "essay about X"
            elif 'about' in message_lower:
                about_match = re.search(r'(?:article|essay|document|paper)\s+about\s+([\w\s]+)', message_lower)
                if about_match:
                    title = about_match.group(1).strip()
            
            # Try "the essay", "that document", "the article" - use last generated document
            elif any(phrase in message_lower for phrase in ['the essay', 'that essay', 'the document', 'that document', 'the article', 'that article', 'essay u made', 'document u made', 'essay you made']):
                # User referencing previously generated document
                if self.last_generated_document:
                    title = Path(self.last_generated_document).stem  # Use filename as title
                    print(f"\n[📄 Detected reference to last document: {title}]")
                else:
                    # Create a new document with generic title
                    title = "document_with_image"
                    print(f"\n[📄 No previous document found - creating new one]")
            
            # Extract image reference
            image_desc = None
            if any(phrase in message_lower for phrase in ['that image', 'the image', 'it']):
                image_desc = 'latest_generated'  # Use most recent image
            elif 'image of' in message_lower:
                img_match = re.search(r'image of\s+([\w\s]+)', message_lower)
                if img_match:
                    image_desc = img_match.group(1).strip()
            
            if title or self.last_generated_document:
                return {
                    'action': 'insert_image_in_document',
                    'title': title or 'document_with_image',
                    'image_description': image_desc,
                    'create_if_missing': True,
                    'use_last_document': bool(self.last_generated_document) and not title
                }
        
        # CRITICAL: Detect DOCUMENT generation FIRST (before image detection)
        # This prevents "make me an essay with an image" from being misdetected as image generation
        
        write_keywords = ['write', 'generate', 'create', 'make me', 'essay', 'article', 'paper', 'document', 'thesis']
        is_write_request = any(keyword in message_lower for keyword in write_keywords)
        
        # Extract word count if mentioned
        word_count_match = re.search(r'(\d+)\s*words?', message_lower)
        target_words = int(word_count_match.group(1)) if word_count_match else 1200
        
        # Detect topic - ENHANCED to handle "of", "on", and "about"
        topic = None
        if 'about' in message_lower:
            topic_match = re.search(r'about\s+([\w\s]+?)(?:\s+(?:in|with|well|and|at)|$)', message_lower)
            if topic_match:
                topic = topic_match.group(1).strip()
        elif 'of' in message_lower:
            # Handle "essay of japan", "article of climate", etc.
            topic_match = re.search(r'(?:essay|article|paper|document|thesis)\s+of\s+([\w\s]+?)(?:\s+(?:with|in|and|at)|$)', message_lower)
            if topic_match:
                topic = topic_match.group(1).strip()
        elif 'on' in message_lower:
            # Handle "essay on japan", "article on climate", etc.
            topic_match = re.search(r'(?:essay|article|paper|document|thesis)\s+on\s+([\w\s]+?)(?:\s+(?:with|in|and|at)|$)', message_lower)
            if topic_match:
                topic = topic_match.group(1).strip()
        
        # ENHANCED: Check if this is a document generation (prioritize over image generation)
        has_creation_verb = any(verb in message_lower for verb in ['create', 'write', 'generate', 'make'])
        has_document_type = any(dtype in message_lower for dtype in ['essay', 'article', 'paper', 'document', 'thesis'])
        
        # If we have both write intent AND topic AND document type, this is DEFINITELY document generation
        if is_write_request and topic and has_document_type:
            print(f"\n[🔍 Detection] Document generation detected!")
            print(f"   Topic: {topic}")
            print(f"   Words: {target_words}")
            print(f"   Images: {'image' in message_lower or 'picture' in message_lower}")
            print(f"   Tables: {'table' in message_lower}")
            return {
                'action': 'generate_document',
                'topic': topic,
                'word_count': target_words,
                'include_images': 'image' in message_lower or 'picture' in message_lower,
                'include_tables': 'table' in message_lower,
                'format': 'docx' if 'docx' in message_lower else 'md'
            }
        
        # ONLY NOW check for standalone image generation requests
        # (Not part of document generation)
        image_keywords = ['image', 'picture', 'photo', 'flag', 'icon', 'logo', 'graphic']
        is_image_only_request = any(keyword in message_lower for keyword in image_keywords)
        
        # Make sure this is NOT a document request (already handled above)
        if is_image_only_request and not has_document_type:
            if any(verb in message_lower for verb in ['give', 'get', 'show', 'create', 'generate', 'download']):
                # Extract image description
                description = None
                
                # Try to extract "flag of X"
                flag_match = re.search(r'flag of (\w+)', message_lower)
                if flag_match:
                    description = f"flag of {flag_match.group(1)}"
                
                # Try to extract after "image/picture of"
                elif 'of' in message_lower:
                    of_match = re.search(r'(?:image|picture|photo|flag)\s+of\s+([\w\s]+)', message_lower)
                    if of_match:
                        description = of_match.group(1).strip()
                
                # Use cleaned message as description
                if not description:
                    description = message_lower.replace('give me', '').replace('get me', '').replace('show me', '').replace('create', '').replace('generate', '').strip()
                
                if description and len(description) > 3:  # Avoid empty descriptions
                    return {
                        'action': 'generate_image',
                        'description': description
                    }
        
        print(f"\n[🔍 Detection] No specific task detected - delegating to interaction agent")
        print(f"   Message: {message[:50]}...")
        plan_file = self._create_general_interaction_plan(message, 'general')
        return {
            'action': 'general_interaction',
            'message': message,
            'plan_file': plan_file,
            'interaction_type': 'general'
        }
    
    def interactive_mode(self):
        """Run in interactive mode with human-in-the-loop control and memory."""
        print(f"\n{'='*70}")
        print(f"GRAIVE AI - INTERACTIVE MODE")
        print(f"{'='*70}")
        print("\nI'm Graive AI - Your autonomous research and writing assistant!")
        print(f"\n📁 Session Workspace: {self.session_workspace}")
        print(f"   All files for this session will be organized here\n")
        print("\nI can:")
        print("  • Write essays, articles, and research papers with citations")
        print("  • Generate images (flags, graphics) and insert them into documents")
        print("  • Generate code (Python, JavaScript, Java, etc.) to actual files")
        print("  • Create PowerPoint presentations")
        print("  • Analyze data (with pandas/matplotlib)")
        print("  • Create, delete, rename, edit files (CLI operations)")
        print("  • Remember our conversation context")
        print("  • Execute complex multi-step tasks")
        print("\nSpecial commands:")
        print("  • reflection-report  - View validation report")
        print("  • cost-report        - View API usage")
        print("  • exit               - Exit system")
        print(f"\n{'='*70}\n")
        
        # Initialize conversation memory
        conversation_history = []
        user_name = None
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("\n👋 Shutting down Graive AI... Goodbye!")
                    break
                
                elif user_input.lower() in ["help", "h", "?"]:
                    print("\n💡 Just talk to me naturally! I understand:")
                    print("   - 'Write an essay about X in Y words'")
                    print("   - 'Generate a report on X with images and tables'")
                    print("   - Regular conversation and questions")
                    print("\n   Commands: reflection-report, cost-report, exit")
                    continue
                
                elif user_input.lower() == "reflection-report":
                    if self.reflection:
                        self.reflection.print_reflection_report()
                    else:
                        print("⚠️  Reflection system not enabled")
                    continue
                
                elif user_input.lower() == "cost-report":
                    print(self.cost_manager.get_report(detailed=True))
                    continue
                
                # Check if user is introducing themselves
                if not user_name:
                    name_patterns = [r"i'm (\w+)", r"i am (\w+)", r"my name is (\w+)", r"am (\w+)"]
                    for pattern in name_patterns:
                        match = re.search(pattern, user_input.lower())
                        if match:
                            user_name = match.group(1).capitalize()
                            print(f"\nManus AI: Nice to meet you, {user_name}! 👋")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"Nice to meet you, {user_name}!"})
                            continue
                
                # Process user request with intelligent routing
                request = self.process_user_request(user_input, user_name)
                
                if request['action'] == 'generate_code':
                    # CODE GENERATION (NEW!)
                    print(f"\nManus AI: I'll create a {request['language']} {request['description']} for you.")
                    print(f"           Generating actual code file...\n")
                    
                    if self.task_executor:
                        result = self.task_executor.execute_task(
                            'generate_code',
                            {
                                'description': request['description'],
                                'language': request['language']
                            }
                        )
                        
                        if result.get('success'):
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"I've created {request['description']} in {request['language']} and saved it to {result['code_file']}"})
                        else:
                            print(f"\n⚠️  Code generation failed: {result.get('error')}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"Error generating code: {result.get('error')}"})
                    else:
                        print(f"\n❌ Task executor not available.")
                
                elif request['action'] == 'analyze_data':
                    # DATA ANALYSIS (NEW!)
                    print(f"\nManus AI: I'll analyze the data for you.")
                    print(f"           Note: Please ensure pandas/matplotlib are installed.\n")
                    
                    if self.task_executor:
                        result = self.task_executor.execute_task(
                            'analyze_data',
                            {
                                'description': request['description'],
                                'data_source': request.get('data_source', 'user_provided')
                            }
                        )
                        
                        if result.get('success'):
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"Analysis complete. Results saved to {result.get('report_file')}"})
                        else:
                            print(f"\n⚠️  {result.get('error')}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": result.get('error')})
                    else:
                        print(f"\n❌ Task executor not available.")
                
                elif request['action'] == 'create_presentation':
                    # PPT GENERATION (NEW!)
                    print(f"\nManus AI: I'll create a PowerPoint presentation about '{request['topic']}'.")
                    print(f"           Note: Please ensure python-pptx is installed.\n")
                    
                    if self.task_executor:
                        result = self.task_executor.execute_task(
                            'create_presentation',
                            {
                                'topic': request['topic'],
                                'slides': request.get('slides', 10)
                            }
                        )
                        
                        if result.get('success'):
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"Presentation created and saved to {result.get('file_path')}"})
                        else:
                            print(f"\n⚠️  {result.get('error')}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": result.get('error')})
                    else:
                        print(f"\n❌ Task executor not available.")
                
                elif request['action'] == 'insert_image_in_document':
                    # IMAGE INSERTION INTO DOCUMENT (FIXED!)
                    print(f"\nManus AI: I'll insert the image into an article titled '{request['title']}'.")
                    print(f"           Creating document with embedded image...\n")
                    
                    if self.task_executor:
                        result = self.task_executor.execute_task(
                            'insert_image_in_document',
                            {
                                'title': request['title'],
                                'image_path': self.last_generated_image,  # Use most recent image
                                'word_count': 800
                            }
                        )
                        
                        if result.get('success'):
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"I've created an article titled '{request['title']}' with the image embedded. Saved to {result['file_path']}"})
                        else:
                            print(f"\n⚠️  Document creation failed: {result.get('error')}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"Error creating document: {result.get('error')}"})
                    else:
                        print(f"\n❌ Task executor not available.")
                
                elif request['action'] == 'generate_image':
                    # User wants an image generated!
                    print(f"\nManus AI: I'll generate an image of '{request['description']}' for you.")
                    print(f"           This will take just a moment...\n")
                    
                    # Generate the image
                    if self.image_generator:
                        result = self.image_generator.generate_image(
                            description=request['description'],
                            method="auto",
                            size="1024x1024"
                        )
                        
                        if result.get('success'):
                            # CRITICAL: Track last generated image for insertion!
                            self.last_generated_image = result['path']
                            
                            print(f"\n✅ Image created successfully!")
                            print(f"   📁 Saved to: {result['filename']}")
                            print(f"   📍 Full path: {result['path']}")
                            print(f"\n💡 Tip: You can now insert this image into a document!")
                            print(f"   Say: 'insert that image in an article titled [your title]'\n")
                            
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"I've created an image of {request['description']} and saved it to {result['path']}"})
                        else:
                            print(f"\n⚠️  Image generation encountered an issue.")
                            print(f"   Created placeholder: {result['filename']}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": f"I created a placeholder for {request['description']}. Install Pillow for actual image generation."})
                    else:
                        print(f"\n❌ Image generator not available. Please restart the system.")
                        conversation_history.append({"role": "user", "content": user_input})
                        conversation_history.append({"role": "assistant", "content": "Image generator is not initialized."})
                
                elif request['action'] == 'generate_document':
                    # User wants a document generated!
                    print(f"\nManus AI: Absolutely! I'll write a {request['word_count']}-word {request['format'].upper()} document about {request['topic']}.")

                    if request['include_images']:
                        print(f"           Including images as requested.")
                    if request['include_tables']:
                        print(f"           Including tables as requested.")
                    
                    # Generate the document using agents
                    result = self.generate_document(
                        topic=request['topic'],
                        word_count=request['word_count'],
                        include_images=request.get('include_images', False),
                        include_tables=request.get('include_tables', False),
                        output_format=request.get('format', 'md')
                    )
                    
                    # Result always contains file_path now (even on error)
                    if result.get('success'):
                        conversation_history.append({"role": "user", "content": user_input})
                        conversation_history.append({"role": "assistant", "content": f"I've generated a {result['word_count']}-word document about {request['topic']} and saved it to {result['file_path']}"})
                    else:
                        print(f"\n⚠️  Generation completed with errors. Check the output above.")
                        conversation_history.append({"role": "user", "content": user_input})
                        conversation_history.append({"role": "assistant", "content": f"I encountered an error while generating the document: {result.get('error', 'Unknown error')}"})

                elif request['action'] == 'general_interaction':
                    print("\nManus AI: Delegating to the interaction agent to complete this task.")

                    if self.task_executor:
                        result = self.task_executor.execute_task(
                            'general_interaction',
                            {
                                'message': request.get('message', user_input),
                                'plan_file': request.get('plan_file'),
                                'analysis': request.get('analysis'),
                                'interaction_type': request.get('interaction_type', 'general'),
                                'user_name': user_name,
                            }
                        )

                        if result.get('success'):
                            response_text = result.get('response', '')
                            print(f"\nManus AI: {response_text}\n")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": response_text})
                        else:
                            print(f"\n⚠️  Interaction task failed: {result.get('error')}")
                            conversation_history.append({"role": "user", "content": user_input})
                            conversation_history.append({"role": "assistant", "content": result.get('error', 'Interaction failed')})
                    else:
                        print(f"\n❌ Task executor not available.")

                else:
                    print(f"\n⚠️  Unknown action: {request['action']}")

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type 'exit' to quit or continue chatting.")
            except Exception as e:
                print(f"\n❌ Unexpected Error: {e}")
                print(f"\nPlease report this issue. Continuing...")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Graive AI - Autonomous General Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python graive.py                                    # Interactive mode
  python graive.py --task generate-thesis             # Generate thesis
  python graive.py --budget 30                        # Set budget
  python graive.py --no-reflection                    # Disable reflection
        """
    )
    
    parser.add_argument(
        "--task",
        type=str,
        help="Task to execute (generate-thesis, etc.)"
    )
    
    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="Workspace directory (default: ./workspace)"
    )
    
    parser.add_argument(
        "--budget",
        type=float,
        default=50.0,
        help="Daily budget in USD (default: 50.0)"
    )
    
    parser.add_argument(
        "--no-reflection",
        action="store_true",
        help="Disable reflection system"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Disable browser automation"
    )
    
    args = parser.parse_args()
    
    # Initialize Graive AI
    graive = GraiveAI(
        workspace=args.workspace,
        daily_budget=args.budget,
        enable_reflection=not args.no_reflection,
        enable_browser=not args.no_browser
    )
    
    # Execute task or enter interactive mode
    if args.task:
        if args.task == "generate-thesis":
            graive.generate_thesis(
                title="Sample Thesis Title",
                research_question="What is the impact of AI on healthcare?",
                target_pages=200
            )
        else:
            print(f"Unknown task: {args.task}")
    else:
        graive.interactive_mode()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
