# Quick Start Guide: Ultra-Long Document Generation

## Introduction

This guide demonstrates how to use the Graive AI Document Orchestration System to generate ultra-long documents like PhD theses (200,000+ words) with intelligent planning, specialized agents, and smart element placement.

## Basic Usage

### 1. Initialize the System

```python
from src.llm.llm_provider_factory import LLMProviderFactory
from src.tools.tool_orchestrator import ToolOrchestrator
from src.planning.document_orchestrator import DocumentOrchestrator

# Initialize LLM provider
llm_provider = LLMProviderFactory.create_provider(
    provider_name="openai",
    api_key="your-api-key",
    model="gpt-4"
)

# Initialize tool orchestrator
tool_orchestrator = ToolOrchestrator()

# Create orchestrator
orchestrator = DocumentOrchestrator(
    llm_provider=llm_provider,
    tool_orchestrator=tool_orchestrator,
    base_sandbox_path="./document_sandbox"
)
```

### 2. Define Document Requirements

```python
requirements = {
    "total_word_count": 200000,  # 200,000 words
    "research_question": "How does AI improve healthcare outcomes?",
    "methodology": "Mixed-methods: systematic review + quantitative analysis",
    "key_findings": [
        "AI improves diagnostic accuracy by 23%",
        "Reduces diagnosis time by 40%",
        "Implementation challenges include data quality"
    ],
    "output_format": "markdown",  # or "latex", "docx", "pdf"
    "citation_style": "apa",       # or "mla", "chicago", "ieee"
    "style_preferences": {
        "line_spacing": 2.0,
        "font_size": 12
    }
}
```

### 3. Generate Document

```python
result = orchestrator.generate_document(
    document_type="thesis",
    title="AI in Healthcare: Improving Diagnostic Accuracy",
    requirements=requirements,
    parallel_execution=True,
    max_workers=4
)

print(f"Document generated: {result['file_path']}")
print(f"Total words: {result['metadata']['total_word_count']:,}")
```

## How It Works

### Step 1: Intelligent Planning

The system analyzes your requirements and creates a detailed plan:

```
Planning Phase:
  ✓ Analyzed research question
  ✓ Generated outline with 7 major sections
  ✓ Allocated word counts: Introduction (15k), Literature (40k), Methods (20k)...
  ✓ Identified required elements: 12 tables, 18 figures
  ✓ Assigned specialized agents to each section
  ✓ Determined execution order respecting dependencies
```

### Step 2: Parallel Execution

Specialized agents work on different sections simultaneously:

```
Execution Phase:
  Wave 1 (Parallel):
    ✓ Introduction (Technical Writer Agent) - 15,234 words
    ✓ Abstract (Technical Writer Agent) - 342 words
  
  Wave 2 (Parallel):
    ✓ Literature Review (Research Synthesis Agent) - 38,567 words
    ✓ Methodology (Methodology Expert Agent) - 19,823 words
  
  Wave 3 (Parallel):
    ✓ Results (Data Analyst Agent) - 28,445 words
      - Generated 5 Python scripts for statistical analysis
      - Created 8 visualizations
      - Formatted 6 results tables
  
  Wave 4:
    ✓ Discussion (Discussion Writer Agent) - 24,891 words
```

### Step 3: Smart Element Placement

Tables and figures are placed optimally near their references:

```
Element Placement:
  ✓ Figure 1: Placed after paragraph 3 (first reference)
  ✓ Table 1: Placed after paragraph 5 (first reference)
  ✓ Figure 2: Placed after paragraph 8 (first reference)
  ✓ All cross-references updated with correct numbers
```

### Step 4: Document Assembly

The final document is assembled with proper formatting:

```
Assembly Phase:
  ✓ Combined 7 sections
  ✓ Inserted 12 tables and 18 figures
  ✓ Generated table of contents
  ✓ Applied style formatting
  ✓ Updated all cross-references
  ✓ Exported to markdown
```

## Advanced Features

### Dynamic Code Generation

The Data Analyst Agent generates custom Python code for analysis:

```python
# Example: Agent automatically generates this code for statistical analysis
# Located in: section_sandbox/analysis_descriptive.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('research_data.csv')

# Descriptive statistics
stats = data.describe()

# Create visualization
plt.figure(figsize=(10, 6))
plt.hist(data['accuracy'], bins=20)
plt.xlabel('Diagnostic Accuracy (%)')
plt.ylabel('Frequency')
plt.title('Distribution of AI Diagnostic Accuracy')
plt.savefig('accuracy_distribution.png', dpi=300)

# Save results
stats.to_json('output.json')
print("Analysis complete: Mean accuracy = 87.3%")
```

### Interactive Mode with Human Review

Use the interactive orchestrator for human-in-the-loop generation:

```python
from src.planning.document_orchestrator import InteractiveDocumentOrchestrator

interactive_orchestrator = InteractiveDocumentOrchestrator(
    llm_provider=llm_provider,
    tool_orchestrator=tool_orchestrator,
    base_sandbox_path="./interactive_sandbox"
)

def review_callback(stage, data):
    if stage == "plan":
        print(f"Review plan with {len(data.sections)} sections")
        user_input = input("Approve plan? (yes/modify): ")
        if user_input == "yes":
            return {"action": "approve"}
        else:
            return {"action": "modify", "changes": {...}}
    
    elif stage == "section":
        print(f"Review section: {data['word_count']} words")
        user_input = input("Action (approve/revise/regenerate): ")
        return {"action": user_input}
    
    return {"action": "approve"}

result = interactive_orchestrator.generate_document_interactive(
    document_type="thesis",
    title="My Research",
    requirements=requirements,
    review_callback=review_callback
)
```

## Document Types Supported

### PhD Thesis (150,000-300,000 words)

```python
orchestrator.generate_document(
    document_type="thesis",
    title="Your Thesis Title",
    requirements={
        "total_word_count": 200000,
        "research_question": "...",
        "methodology": "...",
        "output_format": "latex"
    }
)
```

**Generated Structure:**
- Abstract (300 words)
- Introduction (5,000-15,000 words)
- Literature Review (30,000-50,000 words)
- Methodology (15,000-25,000 words)
- Results (25,000-40,000 words)
- Discussion (20,000-35,000 words)
- Conclusion (3,000-5,000 words)
- References (automatically generated)
- Appendices (as needed)

### Research Paper (6,000-12,000 words)

```python
orchestrator.generate_document(
    document_type="paper",
    title="Your Paper Title",
    requirements={
        "total_word_count": 8000,
        "output_format": "latex",
        "citation_style": "ieee"
    }
)
```

**Generated Structure:**
- Abstract (250 words)
- Introduction (1,000 words)
- Related Work (1,500 words)
- Methodology (2,000 words)
- Results (2,500 words)
- Discussion (1,500 words)
- Conclusion (500 words)

### Technical Book (80,000-150,000 words)

```python
orchestrator.generate_document(
    document_type="book",
    title="Your Book Title",
    requirements={
        "total_word_count": 100000,
        "key_topics": [
            "Introduction to AI",
            "Machine Learning Fundamentals",
            "Deep Learning",
            "Applications",
            "Future Trends"
        ],
        "output_format": "markdown"
    }
)
```

### Business Report (30,000-60,000 words)

```python
orchestrator.generate_document(
    document_type="report",
    title="Market Analysis Report",
    requirements={
        "total_word_count": 50000,
        "style_preferences": {
            "executive_summary": True,
            "confidential": True
        },
        "output_format": "docx"
    }
)
```

## Specialized Agents Explained

### Research Synthesis Agent
- **Handles:** Literature review sections
- **Capabilities:** 
  - Searches academic databases
  - Synthesizes findings from multiple sources
  - Generates citations automatically
  - Creates comparison tables of studies
- **Example Output:** "Smith et al. (2023) found that AI improved diagnostic accuracy by 15%, while Jones et al. (2024) reported 23% improvement..."

### Data Analyst Agent
- **Handles:** Results sections with data analysis
- **Capabilities:**
  - Generates Python scripts for statistical analysis
  - Creates visualizations (histograms, scatter plots, heatmaps)
  - Formats results tables
  - Interprets statistical findings
- **Example Output:** Generates analysis code, executes it, produces tables/figures, writes narrative

### Methodology Expert Agent
- **Handles:** Methodology sections
- **Capabilities:**
  - Describes research design
  - Details data collection procedures
  - Explains analytical approaches
  - Justifies methodological choices
- **Example Output:** "A retrospective cohort study design was employed, analyzing electronic health records from 50,000 patients..."

### Discussion Writer Agent
- **Handles:** Discussion and interpretation sections
- **Capabilities:**
  - Interprets results in context
  - Compares with existing research
  - Discusses implications
  - Addresses limitations
- **Example Output:** "These findings align with Smith et al. (2023) but diverge from Jones et al. (2024), potentially due to differences in..."

### Technical Writer Agent
- **Handles:** General sections (introduction, conclusion, custom)
- **Capabilities:**
  - Creates engaging introductions
  - Writes clear conclusions
  - Maintains consistent style
  - Structures arguments logically
- **Example Output:** "This research addresses a critical gap in understanding how AI systems impact healthcare outcomes..."

## Smart Element Placement

The system automatically places tables, figures, and equations optimally:

### Automatic Placement

```python
# You define elements
DocumentElement(
    element_type=ElementType.TABLE,
    title="Patient Demographics",
    content=table_data,
    placement_hint="near_reference"  # Place near first mention
)

# System finds references in text
"Patient demographics are shown in Table 1..."

# System places table right after this paragraph
```

### Placement Strategies

- **near_reference**: Place after paragraph with first reference
- **end_of_section**: Place at end of section
- **appendix**: Place in appendix
- **inline**: Inline with text (for small elements)

### Cross-Reference Management

```markdown
# Generated text automatically references correctly

The data (Table 3) shows significant improvement...
As illustrated in Figure 5, the trend is clear...
These results (see Table 4 and Figure 6) indicate...

# System ensures all numbers are correct and hyperlinked
```

## Output Formats

### Markdown

```python
requirements = {"output_format": "markdown"}
# Output: thesis.md
# Best for: Web publishing, GitHub, documentation
```

### LaTeX

```python
requirements = {"output_format": "latex"}
# Output: thesis.tex
# Best for: Academic submission, journal publication
# Includes: \documentclass, proper packages, formatting
```

### DOCX

```python
requirements = {"output_format": "docx"}
# Output: thesis.docx
# Best for: Collaborative editing, track changes
# Includes: Proper styles, formatting, tables
```

### PDF

```python
requirements = {"output_format": "pdf"}
# Output: thesis.pdf
# Best for: Final submission, archival
# Requires: LaTeX installation
```

## Performance and Scalability

### Generation Times (Approximate)

| Document Type | Word Count | Parallel Execution | Time |
|--------------|------------|-------------------|------|
| Research Paper | 8,000 | 3 workers | 15-30 min |
| Master's Thesis | 50,000 | 4 workers | 2-4 hours |
| PhD Thesis | 200,000 | 6 workers | 8-16 hours |
| Technical Book | 100,000 | 6 workers | 4-8 hours |

*Times vary based on LLM provider speed, complexity, and data analysis requirements*

### Resource Requirements

- **Memory:** 4-8 GB RAM
- **Storage:** 1-5 GB for sandbox and outputs
- **CPU:** Multi-core recommended for parallel execution
- **API Credits:** Varies by provider and document length

## Troubleshooting

### Issue: Generation takes too long

**Solution:** Increase parallel workers or use faster LLM provider
```python
orchestrator.generate_document(
    ...,
    parallel_execution=True,
    max_workers=8  # Increase from 4
)
```

### Issue: Sections lack detail

**Solution:** Increase word count allocation or provide more specific topics
```python
requirements = {
    "total_word_count": 250000,  # Increase from 200000
    "key_topics": [
        "Topic 1: Detailed description",
        "Topic 2: Specific focus areas"
    ]
}
```

### Issue: Elements not placed correctly

**Solution:** Provide explicit placement hints
```python
DocumentElement(
    ...,
    placement_hint="end_of_section",  # Be explicit
    reference_text="Table 1 shows..."  # Specify reference
)
```

### Issue: Code generation fails

**Solution:** Check sandbox permissions and allowed imports
```python
SectionPlan(
    ...,
    sandbox_config={
        "allowed_imports": ["pandas", "numpy", "matplotlib", "scipy"]
    }
)
```

## Best Practices

1. **Provide Detailed Requirements:** More specific research questions and methodologies produce better results

2. **Use Appropriate Word Counts:** Don't under-allocate; academic standards exist for a reason

3. **Review Incrementally:** Use interactive mode to review sections as they generate

4. **Customize Style Guides:** Provide specific formatting preferences upfront

5. **Save Progress:** Use checkpointing for very long documents
   ```python
   orchestrator.save_progress("checkpoint.json")
   # Later:
   orchestrator.load_progress("checkpoint.json")
   ```

6. **Monitor Execution:** Check execution logs to identify issues
   ```python
   for entry in result['metadata']['execution_log']:
       if not entry['success']:
           print(f"Failed: {entry['section_title']} - {entry['error']}")
   ```

## Next Steps

- Read the [Complete Documentation](DOCUMENT_ORCHESTRATION_SYSTEM.md)
- Review [Example Code](../examples/document_generation_demo.py)
- Explore [Specialized Agent Customization](specialized_agents.py)
- Learn about [Element Placement Optimization](document_assembler.py)

## Support

For issues, questions, or feature requests, refer to the main Graive AI documentation or create an issue in the project repository.
