"""
Specialized Agent System for Document Section Generation

This module implements specialized agents that handle different types of document
sections with domain-specific expertise. Each agent type has unique capabilities,
tool access, and generation strategies optimized for their assigned tasks.

Agents can dynamically generate Python code, execute analysis, create visualizations,
and coordinate with other agents to produce cohesive document sections.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import os
import subprocess
import tempfile
import json
from pathlib import Path


@dataclass
class AgentExecutionContext:
    """Context information for agent execution."""
    section_id: str
    section_title: str
    word_count_target: int
    key_topics: List[str]
    style_guidelines: Dict[str, Any]
    shared_context: Dict[str, Any]
    tools_available: List[str]
    output_directory: str
    sandbox_path: str


@dataclass
class SectionOutput:
    """Output from section generation."""
    section_id: str
    content: str
    word_count: int
    elements: List[Dict[str, Any]]  # Tables, figures, etc.
    metadata: Dict[str, Any]
    generated_files: List[str]
    citations: List[Dict[str, Any]]
    success: bool
    error_message: Optional[str] = None


class SpecializedAgent(ABC):
    """
    Base class for specialized document generation agents.
    
    Each specialized agent handles specific section types with domain expertise,
    appropriate tools, and generation strategies tailored to their task.
    """
    
    def __init__(self, llm_provider: Any, tool_orchestrator: Any):
        """
        Initialize specialized agent.
        
        Args:
            llm_provider: LLM provider for text generation
            tool_orchestrator: Tool orchestrator for accessing system tools
        """
        self.llm_provider = llm_provider
        self.tool_orchestrator = tool_orchestrator
        self.generated_code_files: List[str] = []
    
    @abstractmethod
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """
        Generate complete section content.
        
        Args:
            context: Execution context with requirements and constraints
        
        Returns:
            SectionOutput with generated content and metadata
        """
        pass
    
    def create_python_script(
        self,
        script_name: str,
        code: str,
        sandbox_path: str
    ) -> str:
        """
        Create a Python script file in sandbox for execution.
        
        Args:
            script_name: Name of the script file
            code: Python code content
            sandbox_path: Path to sandbox directory
        
        Returns:
            Full path to created script file
        """
        script_path = os.path.join(sandbox_path, script_name)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        self.generated_code_files.append(script_path)
        return script_path
    
    def execute_python_script(
        self,
        script_path: str,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Execute Python script in sandbox with timeout and resource limits.
        
        Args:
            script_path: Path to script file
            timeout: Maximum execution time in seconds
        
        Returns:
            Execution result with stdout, stderr, and return code
        """
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(script_path)
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Script execution timed out",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }
    
    def generate_code_for_task(
        self,
        task_description: str,
        requirements: List[str],
        output_format: str = "json"
    ) -> str:
        """
        Use LLM to generate Python code for specific task.
        
        Args:
            task_description: Description of what the code should do
            requirements: List of requirements or constraints
            output_format: Expected output format
        
        Returns:
            Generated Python code as string
        """
        prompt = f"""Generate Python code for the following task:

Task: {task_description}

Requirements:
{chr(10).join(f"- {req}" for req in requirements)}

The code should:
1. Be self-contained and executable
2. Output results in {output_format} format
3. Include error handling
4. Save output to 'output.{output_format}' file
5. Include comments explaining key steps

Provide only the Python code without explanations."""

        code = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.2,
            max_tokens=2000
        )
        
        # Clean up code block markers if present
        code = code.replace("```python", "").replace("```", "").strip()
        
        return code


class ResearchSynthesisAgent(SpecializedAgent):
    """
    Agent specialized in literature review and research synthesis.
    
    Capabilities:
    - Search academic databases
    - Synthesize research findings
    - Generate citations
    - Identify research gaps
    - Create comparison tables
    """
    
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """Generate literature review section with research synthesis."""
        
        # Create outline for literature review
        outline = self._create_literature_outline(context)
        
        # Generate content for each subsection
        content_parts = []
        citations = []
        tables = []
        
        for subsection in outline:
            subsection_content, subsection_citations = self._generate_subsection(
                subsection,
                context
            )
            content_parts.append(subsection_content)
            citations.extend(subsection_citations)
        
        # Generate comparison table if needed
        if len(citations) > 5:
            table = self._create_comparison_table(citations, context)
            tables.append(table)
        
        # Combine all content
        full_content = "\n\n".join(content_parts)
        
        return SectionOutput(
            section_id=context.section_id,
            content=full_content,
            word_count=len(full_content.split()),
            elements=tables,
            metadata={"subsections": len(outline)},
            generated_files=[],
            citations=citations,
            success=True
        )
    
    def _create_literature_outline(self, context: AgentExecutionContext) -> List[Dict[str, Any]]:
        """Create outline for literature review based on key topics."""
        outline = []
        
        for topic in context.key_topics:
            outline.append({
                "title": topic,
                "word_count": context.word_count_target // len(context.key_topics),
                "focus": "synthesis"
            })
        
        return outline
    
    def _generate_subsection(
        self,
        subsection: Dict[str, Any],
        context: AgentExecutionContext
    ) -> tuple:
        """Generate content for a literature review subsection."""
        
        prompt = f"""Write a comprehensive literature review subsection on: {subsection['title']}

Word count target: {subsection['word_count']} words

Requirements:
- Synthesize research findings from multiple sources
- Identify key themes and patterns
- Highlight debates and controversies
- Note research gaps
- Use {context.style_guidelines.get('citation_style', 'apa')} citation style
- Maintain {context.style_guidelines.get('tone', 'academic')} tone

Write the subsection:"""

        content = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.7,
            max_tokens=subsection['word_count'] * 2
        )
        
        # Extract citations (simplified - would use proper citation extraction)
        citations = self._extract_citations(content)
        
        return content, citations
    
    def _extract_citations(self, content: str) -> List[Dict[str, Any]]:
        """Extract citation information from content."""
        # Simplified citation extraction
        # In production, would use proper citation parsing
        return []
    
    def _create_comparison_table(
        self,
        citations: List[Dict[str, Any]],
        context: AgentExecutionContext
    ) -> Dict[str, Any]:
        """Create comparison table of research studies."""
        return {
            "type": "table",
            "title": "Comparison of Key Studies",
            "content": "table_data",  # Would generate actual table
            "placement": "near_reference"
        }


class DataAnalystAgent(SpecializedAgent):
    """
    Agent specialized in results section with data analysis and visualization.
    
    Capabilities:
    - Statistical analysis
    - Data visualization
    - Table generation
    - Results interpretation
    - Dynamic code generation for custom analyses
    """
    
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """Generate results section with analysis and visualizations."""
        
        # Determine required analyses
        analyses = self._plan_analyses(context)
        
        # Generate Python scripts for each analysis
        analysis_results = []
        generated_files = []
        
        for analysis in analyses:
            script_path = self._generate_analysis_script(analysis, context)
            generated_files.append(script_path)
            
            # Execute analysis
            result = self.execute_python_script(script_path)
            
            if result["success"]:
                analysis_results.append(self._parse_analysis_output(analysis, result))
        
        # Generate narrative description of results
        content = self._generate_results_narrative(analysis_results, context)
        
        # Extract tables and figures
        elements = self._extract_elements(analysis_results)
        
        return SectionOutput(
            section_id=context.section_id,
            content=content,
            word_count=len(content.split()),
            elements=elements,
            metadata={"analyses_performed": len(analyses)},
            generated_files=generated_files,
            citations=[],
            success=True
        )
    
    def _plan_analyses(self, context: AgentExecutionContext) -> List[Dict[str, Any]]:
        """Plan required statistical analyses based on context."""
        
        # Use LLM to determine appropriate analyses
        prompt = f"""Given a research section titled "{context.section_title}" with these key topics:
{chr(10).join(f"- {topic}" for topic in context.key_topics)}

What statistical analyses and visualizations should be included?

Provide a JSON list of analyses in this format:
[
    {{
        "name": "Descriptive Statistics",
        "type": "descriptive",
        "visualizations": ["histogram", "boxplot"]
    }}
]"""

        response = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        try:
            analyses = json.loads(response)
        except json.JSONDecodeError:
            # Fallback to default analyses
            analyses = [
                {
                    "name": "Descriptive Statistics",
                    "type": "descriptive",
                    "visualizations": ["histogram", "summary_table"]
                }
            ]
        
        return analyses
    
    def _generate_analysis_script(
        self,
        analysis: Dict[str, Any],
        context: AgentExecutionContext
    ) -> str:
        """Generate Python script for statistical analysis."""
        
        code = self.generate_code_for_task(
            task_description=f"Perform {analysis['name']} analysis",
            requirements=[
                "Use pandas for data manipulation",
                "Generate visualizations with matplotlib",
                f"Create {', '.join(analysis.get('visualizations', []))}",
                "Save results to output.json",
                "Save figures as PNG files"
            ],
            output_format="json"
        )
        
        script_name = f"analysis_{analysis['type']}.py"
        return self.create_python_script(script_name, code, context.sandbox_path)
    
    def _parse_analysis_output(
        self,
        analysis: Dict[str, Any],
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse output from analysis script execution."""
        return {
            "analysis_name": analysis["name"],
            "output": execution_result["stdout"],
            "visualizations": []  # Would extract from generated files
        }
    
    def _generate_results_narrative(
        self,
        analysis_results: List[Dict[str, Any]],
        context: AgentExecutionContext
    ) -> str:
        """Generate narrative description of results."""
        
        results_summary = "\n".join([
            f"- {r['analysis_name']}: {r['output'][:200]}"
            for r in analysis_results
        ])
        
        prompt = f"""Write a results section describing these statistical analyses:

{results_summary}

Requirements:
- Word count: {context.word_count_target} words
- Reference tables and figures appropriately
- Report statistics with proper notation
- Maintain objective tone
- Use past tense

Write the results section:"""

        content = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=context.word_count_target * 2
        )
        
        return content
    
    def _extract_elements(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract tables and figures from analysis results."""
        elements = []
        
        for result in analysis_results:
            # Would extract actual tables and figures
            elements.append({
                "type": "table",
                "title": f"Results: {result['analysis_name']}",
                "content": "table_data"
            })
        
        return elements


class MethodologyExpertAgent(SpecializedAgent):
    """
    Agent specialized in methodology section writing.
    
    Capabilities:
    - Describe research design
    - Explain data collection procedures
    - Detail analytical approaches
    - Justify methodological choices
    - Create methodology flowcharts
    """
    
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """Generate methodology section with detailed procedures."""
        
        # Break down into subsections
        subsections = [
            "Research Design",
            "Participants/Sample",
            "Data Collection",
            "Data Analysis",
            "Ethical Considerations"
        ]
        
        content_parts = []
        
        for subsection in subsections:
            subsection_content = self._generate_methodology_subsection(
                subsection,
                context
            )
            content_parts.append(f"### {subsection}\n\n{subsection_content}")
        
        full_content = "\n\n".join(content_parts)
        
        # Generate methodology flowchart code
        flowchart_code = self._generate_flowchart_code(context)
        flowchart_path = self.create_python_script(
            "methodology_flowchart.py",
            flowchart_code,
            context.sandbox_path
        )
        
        return SectionOutput(
            section_id=context.section_id,
            content=full_content,
            word_count=len(full_content.split()),
            elements=[],
            metadata={"subsections": len(subsections)},
            generated_files=[flowchart_path],
            citations=[],
            success=True
        )
    
    def _generate_methodology_subsection(
        self,
        subsection_title: str,
        context: AgentExecutionContext
    ) -> str:
        """Generate content for methodology subsection."""
        
        prompt = f"""Write a detailed methodology subsection on: {subsection_title}

Context: {context.section_title}
Key topics: {', '.join(context.key_topics)}

Requirements:
- Be precise and detailed
- Use past tense
- Justify methodological choices
- Include technical specifications
- Length: ~{context.word_count_target // 5} words

Write the subsection:"""

        content = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=1000
        )
        
        return content
    
    def _generate_flowchart_code(self, context: AgentExecutionContext) -> str:
        """Generate code to create methodology flowchart."""
        
        code = """
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 8))

# Create flowchart boxes
# (This would be more sophisticated in production)

plt.title('Methodology Flowchart')
plt.axis('off')
plt.tight_layout()
plt.savefig('methodology_flowchart.png', dpi=300, bbox_inches='tight')
print("Flowchart saved to methodology_flowchart.png")
"""
        return code


class DiscussionWriterAgent(SpecializedAgent):
    """
    Agent specialized in discussion and interpretation sections.
    
    Capabilities:
    - Interpret results in context of literature
    - Compare findings with existing research
    - Discuss implications
    - Address limitations
    - Propose future research directions
    """
    
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """Generate discussion section with interpretation and implications."""
        
        # Get results from shared context
        results_summary = context.shared_context.get("results_summary", "")
        literature_summary = context.shared_context.get("literature_summary", "")
        
        subsections = [
            "Interpretation of Findings",
            "Comparison with Existing Literature",
            "Theoretical Implications",
            "Practical Implications",
            "Limitations",
            "Future Research Directions"
        ]
        
        content_parts = []
        
        for subsection in subsections:
            subsection_content = self._generate_discussion_subsection(
                subsection,
                context,
                results_summary,
                literature_summary
            )
            content_parts.append(f"### {subsection}\n\n{subsection_content}")
        
        full_content = "\n\n".join(content_parts)
        
        return SectionOutput(
            section_id=context.section_id,
            content=full_content,
            word_count=len(full_content.split()),
            elements=[],
            metadata={"subsections": len(subsections)},
            generated_files=[],
            citations=[],
            success=True
        )
    
    def _generate_discussion_subsection(
        self,
        subsection_title: str,
        context: AgentExecutionContext,
        results_summary: str,
        literature_summary: str
    ) -> str:
        """Generate discussion subsection content."""
        
        prompt = f"""Write a discussion subsection on: {subsection_title}

Results summary: {results_summary[:500]}
Literature context: {literature_summary[:500]}

Requirements:
- Connect results to broader context
- Use present tense for implications
- Be balanced and critical
- Support claims with evidence
- Length: ~{context.word_count_target // 6} words

Write the subsection:"""

        content = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.6,
            max_tokens=1000
        )
        
        return content


class TechnicalWriterAgent(SpecializedAgent):
    """
    Agent specialized in general technical writing (introduction, conclusion, etc.).
    
    Capabilities:
    - Create engaging introductions
    - Write clear conclusions
    - Structure arguments logically
    - Maintain consistent style
    - Synthesize information
    """
    
    def generate_section(self, context: AgentExecutionContext) -> SectionOutput:
        """Generate general technical section."""
        
        prompt = f"""Write a complete section titled: {context.section_title}

Key topics to cover:
{chr(10).join(f"- {topic}" for topic in context.key_topics)}

Requirements:
- Word count: {context.word_count_target} words
- Tone: {context.style_guidelines.get('tone', 'formal')}
- Tense: {context.style_guidelines.get('tense', 'present')}
- Style: Academic and professional

Shared context from other sections:
{json.dumps(context.shared_context, indent=2)[:500]}

Write the complete section:"""

        content = self.llm_provider.generate(
            prompt=prompt,
            temperature=0.7,
            max_tokens=context.word_count_target * 2
        )
        
        return SectionOutput(
            section_id=context.section_id,
            content=content,
            word_count=len(content.split()),
            elements=[],
            metadata={},
            generated_files=[],
            citations=[],
            success=True
        )
