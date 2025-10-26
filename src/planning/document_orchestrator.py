"""
Document Orchestration System

This module coordinates the entire document generation process, managing the
workflow from planning through execution to final assembly. It handles parallel
execution of specialized agents, maintains shared context, and ensures consistency.
"""

from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import tempfile
from pathlib import Path
from datetime import datetime
import json

from src.planning.document_planner import (
    DocumentPlanner, DocumentPlan, SectionPlan, AgentSpecialization
)
from src.planning.specialized_agents import (
    SpecializedAgent, ResearchSynthesisAgent, DataAnalystAgent,
    MethodologyExpertAgent, DiscussionWriterAgent, TechnicalWriterAgent,
    AgentExecutionContext, SectionOutput
)
from src.planning.document_assembler import DocumentAssembler


class DocumentOrchestrator:
    """
    Central orchestrator for ultra-long document generation.
    
    Coordinates planning, execution, and assembly phases while managing
    specialized agents, shared context, and parallel execution.
    """
    
    def __init__(self, llm_provider: Any, tool_orchestrator: Any, base_sandbox_path: str):
        """
        Initialize document orchestrator.
        
        Args:
            llm_provider: LLM provider for text generation
            tool_orchestrator: Tool orchestrator for system tools
            base_sandbox_path: Base path for sandbox directories
        """
        self.llm_provider = llm_provider
        self.tool_orchestrator = tool_orchestrator
        self.base_sandbox_path = base_sandbox_path
        
        # Initialize components
        self.planner = DocumentPlanner(llm_provider)
        self.assembler = DocumentAssembler()
        
        # Initialize specialized agents
        self.agents = {
            AgentSpecialization.RESEARCH_SYNTHESIS: ResearchSynthesisAgent(
                llm_provider, tool_orchestrator
            ),
            AgentSpecialization.DATA_ANALYST: DataAnalystAgent(
                llm_provider, tool_orchestrator
            ),
            AgentSpecialization.METHODOLOGY_EXPERT: MethodologyExpertAgent(
                llm_provider, tool_orchestrator
            ),
            AgentSpecialization.DISCUSSION_WRITER: DiscussionWriterAgent(
                llm_provider, tool_orchestrator
            ),
            AgentSpecialization.TECHNICAL_WRITER: TechnicalWriterAgent(
                llm_provider, tool_orchestrator
            )
        }
        
        # Shared context across all agents
        self.shared_context: Dict[str, Any] = {}
        
        # Execution tracking
        self.execution_log: List[Dict[str, Any]] = []
    
    def generate_document(
        self,
        document_type: str,
        title: str,
        requirements: Dict[str, Any],
        parallel_execution: bool = True,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """
        Generate complete document from high-level requirements.
        
        This is the main entry point that orchestrates the entire process:
        1. Create detailed plan
        2. Execute sections in optimal order
        3. Assemble final document
        4. Export to desired format
        
        Args:
            document_type: Type of document (thesis, paper, book, report)
            title: Document title
            requirements: Detailed requirements dictionary
            parallel_execution: Whether to execute sections in parallel
            max_workers: Maximum parallel workers
        
        Returns:
            Dictionary containing:
                - document_content: Final assembled document
                - plan: Execution plan used
                - section_outputs: Individual section outputs
                - metadata: Execution metadata
                - file_path: Path to exported document
        """
        print(f"Starting document generation: {title}")
        print(f"Type: {document_type}, Target: {requirements.get('total_word_count', 'N/A')} words")
        
        # Phase 1: Planning
        print("\n=== PHASE 1: PLANNING ===")
        plan = self.planner.create_plan(document_type, title, requirements)
        print(f"Created plan with {len(plan.sections)} sections")
        
        # Export plan for review
        plan_path = os.path.join(self.base_sandbox_path, f"{title}_plan.json")
        self.planner.export_plan(plan, plan_path)
        print(f"Plan exported to: {plan_path}")
        
        # Phase 2: Section Execution
        print("\n=== PHASE 2: SECTION EXECUTION ===")
        section_outputs = self._execute_sections(
            plan,
            parallel_execution,
            max_workers
        )
        print(f"Completed {len(section_outputs)} sections")
        
        # Phase 3: Document Assembly
        print("\n=== PHASE 3: DOCUMENT ASSEMBLY ===")
        assembled_document = self.assembler.assemble_document(
            sections=section_outputs,
            elements=plan.elements,
            style_guide=plan.style_guide
        )
        print(f"Assembled document: {len(assembled_document.split())} words")
        
        # Phase 4: Export
        print("\n=== PHASE 4: EXPORT ===")
        output_format = requirements.get("output_format", "markdown")
        output_path = os.path.join(
            self.base_sandbox_path,
            f"{title.replace(' ', '_')}.{output_format}"
        )
        self.assembler.export_document(assembled_document, output_path, output_format)
        print(f"Document exported to: {output_path}")
        
        # Collect metadata
        metadata = {
            "generation_time": datetime.utcnow().isoformat(),
            "total_sections": len(plan.sections),
            "total_word_count": len(assembled_document.split()),
            "execution_mode": "parallel" if parallel_execution else "sequential",
            "sections_executed": len(section_outputs),
            "execution_log": self.execution_log
        }
        
        return {
            "document_content": assembled_document,
            "plan": plan,
            "section_outputs": section_outputs,
            "metadata": metadata,
            "file_path": output_path
        }
    
    def _execute_sections(
        self,
        plan: DocumentPlan,
        parallel: bool,
        max_workers: int
    ) -> List[Dict[str, Any]]:
        """
        Execute all sections according to plan.
        
        Respects dependencies while maximizing parallelization when possible.
        Updates shared context as sections complete.
        """
        section_outputs = []
        completed_sections = set()
        
        if parallel:
            section_outputs = self._execute_parallel(
                plan,
                max_workers,
                completed_sections
            )
        else:
            section_outputs = self._execute_sequential(
                plan,
                completed_sections
            )
        
        return section_outputs
    
    def _execute_parallel(
        self,
        plan: DocumentPlan,
        max_workers: int,
        completed_sections: set
    ) -> List[Dict[str, Any]]:
        """Execute sections in parallel respecting dependencies."""
        section_outputs = []
        sections_by_id = {s.section_id: s for s in plan.sections}
        
        # Group sections into execution waves based on dependencies
        waves = self._create_execution_waves(plan.sections)
        
        print(f"Executing in {len(waves)} waves with up to {max_workers} parallel workers")
        
        for wave_idx, wave_sections in enumerate(waves):
            print(f"\nWave {wave_idx + 1}/{len(waves)}: {len(wave_sections)} sections")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all sections in this wave
                future_to_section = {
                    executor.submit(
                        self._execute_section,
                        section,
                        plan
                    ): section
                    for section in wave_sections
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_section):
                    section = future_to_section[future]
                    try:
                        output = future.result()
                        section_outputs.append(output)
                        completed_sections.add(section.section_id)
                        
                        # Update shared context with completed section
                        self._update_shared_context(section, output)
                        
                        print(f"  ✓ Completed: {section.title} ({output['word_count']} words)")
                        
                    except Exception as e:
                        print(f"  ✗ Failed: {section.title} - {str(e)}")
                        self._log_execution(section, success=False, error=str(e))
        
        return section_outputs
    
    def _execute_sequential(
        self,
        plan: DocumentPlan,
        completed_sections: set
    ) -> List[Dict[str, Any]]:
        """Execute sections sequentially in dependency order."""
        section_outputs = []
        
        for section in plan.sections:
            # Check dependencies
            if not self._dependencies_satisfied(section, completed_sections):
                print(f"Skipping {section.title} - dependencies not satisfied")
                continue
            
            print(f"\nExecuting: {section.title}")
            
            try:
                output = self._execute_section(section, plan)
                section_outputs.append(output)
                completed_sections.add(section.section_id)
                
                # Update shared context
                self._update_shared_context(section, output)
                
                print(f"  ✓ Completed ({output['word_count']} words)")
                
            except Exception as e:
                print(f"  ✗ Failed: {str(e)}")
                self._log_execution(section, success=False, error=str(e))
        
        return section_outputs
    
    def _execute_section(
        self,
        section: SectionPlan,
        plan: DocumentPlan
    ) -> Dict[str, Any]:
        """
        Execute a single section using appropriate specialized agent.
        
        Creates sandbox environment, builds execution context, invokes agent,
        and processes output.
        """
        # Create section-specific sandbox
        sandbox_path = self._create_section_sandbox(section)
        
        # Build execution context
        context = AgentExecutionContext(
            section_id=section.section_id,
            section_title=section.title,
            word_count_target=section.target_word_count,
            key_topics=section.key_topics,
            style_guidelines=section.style_guidelines,
            shared_context=self.shared_context.copy(),
            tools_available=section.tools_allowed,
            output_directory=sandbox_path,
            sandbox_path=sandbox_path
        )
        
        # Get appropriate agent
        agent = self.agents.get(section.assigned_agent)
        if not agent:
            raise ValueError(f"No agent found for {section.assigned_agent}")
        
        # Execute section generation
        start_time = datetime.utcnow()
        output = agent.generate_section(context)
        end_time = datetime.utcnow()
        
        # Log execution
        execution_time = (end_time - start_time).total_seconds()
        self._log_execution(
            section,
            success=output.success,
            execution_time=execution_time,
            word_count=output.word_count
        )
        
        # Convert output to dictionary
        output_dict = {
            "section_id": output.section_id,
            "content": output.content,
            "word_count": output.word_count,
            "elements": output.elements,
            "metadata": output.metadata,
            "generated_files": output.generated_files,
            "citations": output.citations,
            "success": output.success,
            "execution_time": execution_time
        }
        
        return output_dict
    
    def _create_section_sandbox(self, section: SectionPlan) -> str:
        """Create isolated sandbox directory for section execution."""
        sandbox_path = os.path.join(
            self.base_sandbox_path,
            f"section_{section.section_id}"
        )
        os.makedirs(sandbox_path, exist_ok=True)
        return sandbox_path
    
    def _dependencies_satisfied(
        self,
        section: SectionPlan,
        completed_sections: set
    ) -> bool:
        """Check if all section dependencies are satisfied."""
        return all(dep_id in completed_sections for dep_id in section.depends_on)
    
    def _create_execution_waves(
        self,
        sections: List[SectionPlan]
    ) -> List[List[SectionPlan]]:
        """
        Group sections into execution waves based on dependencies.
        
        Sections in the same wave can execute in parallel.
        Each wave must complete before the next begins.
        """
        waves = []
        remaining = sections.copy()
        completed = set()
        
        while remaining:
            # Find sections with satisfied dependencies
            wave = [
                s for s in remaining
                if all(dep in completed for dep in s.depends_on)
            ]
            
            if not wave:
                # Circular dependency or error
                print("Warning: Circular dependency detected, breaking...")
                wave = remaining[:1]
            
            waves.append(wave)
            
            # Remove from remaining and mark as completed
            for section in wave:
                remaining.remove(section)
                completed.add(section.section_id)
        
        return waves
    
    def _update_shared_context(
        self,
        section: SectionPlan,
        output: Dict[str, Any]
    ):
        """
        Update shared context with completed section information.
        
        This allows later sections to reference and build upon earlier work.
        """
        # Store section summary
        summary_key = f"{section.section_type.value}_summary"
        content_preview = output["content"][:500] + "..." if len(output["content"]) > 500 else output["content"]
        
        self.shared_context[summary_key] = content_preview
        self.shared_context[f"{section.section_id}_word_count"] = output["word_count"]
        
        # Store citations for later sections
        if output.get("citations"):
            if "all_citations" not in self.shared_context:
                self.shared_context["all_citations"] = []
            self.shared_context["all_citations"].extend(output["citations"])
        
        # Store elements
        if output.get("elements"):
            if "all_elements" not in self.shared_context:
                self.shared_context["all_elements"] = []
            self.shared_context["all_elements"].extend(output["elements"])
    
    def _log_execution(
        self,
        section: SectionPlan,
        success: bool,
        execution_time: Optional[float] = None,
        word_count: Optional[int] = None,
        error: Optional[str] = None
    ):
        """Log section execution details."""
        log_entry = {
            "section_id": section.section_id,
            "section_title": section.title,
            "agent": section.assigned_agent.value,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_seconds": execution_time,
            "word_count": word_count,
            "error": error
        }
        self.execution_log.append(log_entry)
    
    def save_progress(self, checkpoint_path: str):
        """Save current execution progress for resumption."""
        checkpoint = {
            "shared_context": self.shared_context,
            "execution_log": self.execution_log,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
    
    def load_progress(self, checkpoint_path: str):
        """Load previous execution progress."""
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        self.shared_context = checkpoint.get("shared_context", {})
        self.execution_log = checkpoint.get("execution_log", [])


class InteractiveDocumentOrchestrator(DocumentOrchestrator):
    """
    Enhanced orchestrator with human-in-the-loop capabilities.
    
    Allows user to:
    - Review and modify plan before execution
    - Pause and review section outputs
    - Provide feedback and request revisions
    - Modify requirements mid-execution
    """
    
    def __init__(self, llm_provider: Any, tool_orchestrator: Any, base_sandbox_path: str):
        """Initialize interactive orchestrator."""
        super().__init__(llm_provider, tool_orchestrator, base_sandbox_path)
        self.user_feedback: List[Dict[str, Any]] = []
    
    def generate_document_interactive(
        self,
        document_type: str,
        title: str,
        requirements: Dict[str, Any],
        review_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Generate document with interactive review points.
        
        Args:
            document_type: Type of document
            title: Document title
            requirements: Requirements dictionary
            review_callback: Function called at review points, returns user feedback
        
        Returns:
            Complete document generation result
        """
        # Phase 1: Planning with review
        print("\n=== PLANNING PHASE ===")
        plan = self.planner.create_plan(document_type, title, requirements)
        
        if review_callback:
            print("\nPlan created. Requesting user review...")
            feedback = review_callback("plan", plan)
            if feedback.get("action") == "modify":
                plan = self._apply_plan_modifications(plan, feedback.get("changes", {}))
        
        # Phase 2: Execution with section reviews
        print("\n=== EXECUTION PHASE ===")
        section_outputs = []
        
        for section in plan.sections:
            print(f"\nExecuting: {section.title}")
            output = self._execute_section(section, plan)
            
            if review_callback:
                print("Section complete. Requesting user review...")
                feedback = review_callback("section", output)
                
                if feedback.get("action") == "revise":
                    print("Revising section based on feedback...")
                    output = self._revise_section(section, output, feedback, plan)
                elif feedback.get("action") == "regenerate":
                    print("Regenerating section...")
                    output = self._execute_section(section, plan)
            
            section_outputs.append(output)
            self._update_shared_context(section, output)
        
        # Phase 3: Assembly
        print("\n=== ASSEMBLY PHASE ===")
        assembled_document = self.assembler.assemble_document(
            sections=section_outputs,
            elements=plan.elements,
            style_guide=plan.style_guide
        )
        
        # Final review
        if review_callback:
            print("\nDocument assembled. Requesting final review...")
            feedback = review_callback("final", {"content": assembled_document})
            
            if feedback.get("action") == "approve":
                print("Document approved!")
            else:
                print("Additional revisions requested...")
        
        # Export
        output_format = requirements.get("output_format", "markdown")
        output_path = os.path.join(
            self.base_sandbox_path,
            f"{title.replace(' ', '_')}.{output_format}"
        )
        self.assembler.export_document(assembled_document, output_path, output_format)
        
        return {
            "document_content": assembled_document,
            "plan": plan,
            "section_outputs": section_outputs,
            "user_feedback": self.user_feedback,
            "file_path": output_path
        }
    
    def _apply_plan_modifications(
        self,
        plan: DocumentPlan,
        changes: Dict[str, Any]
    ) -> DocumentPlan:
        """Apply user modifications to plan."""
        # Would implement plan modification logic
        self.user_feedback.append({
            "type": "plan_modification",
            "timestamp": datetime.utcnow().isoformat(),
            "changes": changes
        })
        return plan
    
    def _revise_section(
        self,
        section: SectionPlan,
        output: Dict[str, Any],
        feedback: Dict[str, Any],
        plan: DocumentPlan
    ) -> Dict[str, Any]:
        """Revise section based on user feedback."""
        self.user_feedback.append({
            "type": "section_revision",
            "section_id": section.section_id,
            "timestamp": datetime.utcnow().isoformat(),
            "feedback": feedback
        })
        
        # Would implement revision logic using feedback
        return output
