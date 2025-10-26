# Document Generation System - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER REQUIREMENTS                                │
│  Document Type: PhD Thesis                                              │
│  Word Count: 200,000 words                                              │
│  Research Question: "How does AI improve healthcare?"                   │
│  Output Format: LaTeX/PDF                                               │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DOCUMENT ORCHESTRATOR                               │
│  - Coordinates entire workflow                                          │
│  - Manages parallel execution                                           │
│  - Maintains shared context                                             │
│  - Handles human-in-the-loop                                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────┴───────────────────────┐
         │                                               │
         ▼                                               ▼
┌─────────────────────┐                    ┌─────────────────────────────┐
│  DOCUMENT PLANNER   │                    │   SHARED CONTEXT STORE      │
│                     │                    │                             │
│ 1. Analyze Request  │◄───────────────────│  - Section summaries        │
│ 2. Generate Outline │                    │  - Citations                │
│ 3. Allocate Words   │────────────────────►  - Elements (tables/figs)   │
│ 4. Assign Agents    │                    │  - Terminology              │
│ 5. Order Execution  │                    │  - Results data             │
└─────────┬───────────┘                    └─────────────────────────────┘
          │
          │ Creates DocumentPlan
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION WAVES                                  │
│                                                                          │
│  WAVE 1 (Parallel):                                                     │
│  ┌──────────────────┐    ┌──────────────────┐                          │
│  │  Introduction    │    │     Abstract     │                          │
│  │  Technical Writer│    │ Technical Writer │                          │
│  │  15,000 words    │    │    300 words     │                          │
│  └──────────────────┘    └──────────────────┘                          │
│                                                                          │
│  WAVE 2 (Parallel):                                                     │
│  ┌──────────────────┐    ┌──────────────────┐                          │
│  │ Literature Review│    │   Methodology    │                          │
│  │Research Synthesis│    │Methodology Expert│                          │
│  │  40,000 words    │    │  20,000 words    │                          │
│  └──────────────────┘    └──────────────────┘                          │
│                                                                          │
│  WAVE 3:                                                                │
│  ┌──────────────────┐                                                   │
│  │     Results      │                                                   │
│  │  Data Analyst    │                                                   │
│  │  35,000 words    │                                                   │
│  │ + Python Scripts │                                                   │
│  │ + Visualizations │                                                   │
│  └──────────────────┘                                                   │
│                                                                          │
│  WAVE 4:                                                                │
│  ┌──────────────────┐    ┌──────────────────┐                          │
│  │   Discussion     │    │   Conclusion     │                          │
│  │Discussion Writer │    │ Technical Writer │                          │
│  │  25,000 words    │    │   5,000 words    │                          │
│  └──────────────────┘    └──────────────────┘                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  │ Section Outputs
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DOCUMENT ASSEMBLER                                  │
│                                                                          │
│  Step 1: Parse sections into paragraphs                                 │
│  Step 2: Find element references in text                                │
│          "As shown in Table 1..." → Reference found                     │
│  Step 3: Determine optimal element positions                            │
│          Table 1 → Place after paragraph 5 (first reference)            │
│  Step 4: Insert elements with captions                                  │
│  Step 5: Update cross-references                                        │
│  Step 6: Generate table of contents                                     │
│  Step 7: Apply formatting                                               │
│                                                                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   FINAL DOCUMENT        │
                    │                         │
                    │  200,000 words          │
                    │  Properly formatted     │
                    │  Elements placed        │
                    │  References correct     │
                    │  Ready for submission   │
                    └─────────────────────────┘
```

## Specialized Agent Detail

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      SPECIALIZED AGENTS                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐      ┌──────────────────────┐
│ Research Synthesis   │      │   Data Analyst       │
│      Agent           │      │      Agent           │
├──────────────────────┤      ├──────────────────────┤
│ • Search databases   │      │ • Plan analyses      │
│ • Synthesize sources │      │ • Generate Python    │
│ • Create citations   │      │ • Execute scripts    │
│ • Compare studies    │      │ • Create viz         │
│ • Identify gaps      │      │ • Format tables      │
└──────────────────────┘      └──────────────────────┘

┌──────────────────────┐      ┌──────────────────────┐
│ Methodology Expert   │      │  Discussion Writer   │
│      Agent           │      │       Agent          │
├──────────────────────┤      ├──────────────────────┤
│ • Describe design    │      │ • Interpret results  │
│ • Detail procedures  │      │ • Compare literature │
│ • Justify choices    │      │ • Discuss implications│
│ • Create flowcharts  │      │ • Address limitations│
│ • Technical specs    │      │ • Propose future work│
└──────────────────────┘      └──────────────────────┘

┌──────────────────────┐
│  Technical Writer    │
│      Agent           │
├──────────────────────┤
│ • Write intros       │
│ • Write conclusions  │
│ • General sections   │
│ • Maintain style     │
│ • Structure args     │
└──────────────────────┘
```

## Dynamic Code Generation Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   DATA ANALYST AGENT WORKFLOW                            │
└─────────────────────────────────────────────────────────────────────────┘

Section: Results
Goal: Analyze patient data and create visualizations

         │
         ▼
┌────────────────────┐
│  1. Plan Analyses  │
│                    │
│  - Descriptive     │
│  - Correlation     │
│  - Regression      │
│  - Visualization   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────────────────┐
│  2. Generate Python Code (LLM) │
│                                │
│  Prompt: "Generate code for    │
│  descriptive statistics with   │
│  outlier detection using IQR"  │
└─────────┬──────────────────────┘
          │
          ▼
┌───────────────────────────────────────────┐
│  3. Created: analysis_descriptive.py      │
│                                           │
│  import pandas as pd                      │
│  import matplotlib.pyplot as plt          │
│                                           │
│  data = pd.read_csv('data.csv')          │
│  stats = data.describe()                  │
│  # ... outlier detection ...             │
│  plt.savefig('histogram.png')            │
│  stats.to_json('output.json')            │
└─────────┬─────────────────────────────────┘
          │
          ▼
┌────────────────────────────┐
│  4. Execute in Sandbox     │
│                            │
│  Timeout: 300s             │
│  Memory: 2GB limit         │
│  Network: Restricted       │
│  File access: Sandbox only │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────────┐
│  5. Parse Results              │
│                                │
│  - output.json → Data          │
│  - histogram.png → Figure 3    │
│  - stdout → Statistics         │
└─────────┬──────────────────────┘
          │
          ▼
┌────────────────────────────────────────┐
│  6. Generate Narrative                 │
│                                        │
│  "Descriptive statistics revealed a    │
│  mean age of 54.3 years (SD=12.1).     │
│  As shown in Figure 3, the             │
│  distribution was approximately        │
│  normal with 3 outliers identified..." │
└────────────────────────────────────────┘
```

## Element Placement Intelligence

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ELEMENT PLACEMENT PROCESS                             │
└─────────────────────────────────────────────────────────────────────────┘

Section Content:
┌──────────────────────────────────────────────────────────────┐
│ Paragraph 1: Introduction to patient demographics           │
│ Paragraph 2: Data collection methodology                    │
│ Paragraph 3: Patient demographics are shown in Table 1.     │◄─┐
│ Paragraph 4: The cohort included diverse ages.              │  │
│ Paragraph 5: Clinical characteristics varied significantly. │  │
│ Paragraph 6: As illustrated in Figure 1, outcomes improved. │  │
└──────────────────────────────────────────────────────────────┘  │
                                                                   │
1. FIND REFERENCES                                                │
   "shown in Table 1" → Found in Paragraph 3 ─────────────────────┘
   "illustrated in Figure 1" → Found in Paragraph 6

2. DETERMINE PLACEMENT
   Table 1: Place after Paragraph 3 (first reference)
   Figure 1: Place after Paragraph 6 (first reference)

3. INSERT WITH FORMATTING

Final Output:
┌──────────────────────────────────────────────────────────────┐
│ Paragraph 1: Introduction to patient demographics           │
│ Paragraph 2: Data collection methodology                    │
│ Paragraph 3: Patient demographics are shown in Table 1.     │
│                                                              │
│ **Table 1: Patient Demographics**                           │
│ ┌────────────┬───────────┬──────────┐                       │
│ │Characteristic│Mean (SD) │  Range   │                       │
│ ├────────────┼───────────┼──────────┤                       │
│ │Age (years)  │54.3 (12.1)│  23-87   │                       │
│ │BMI          │26.8 (4.2) │  18-42   │                       │
│ └────────────┴───────────┴──────────┘                       │
│                                                              │
│ Paragraph 4: The cohort included diverse ages.              │
│ Paragraph 5: Clinical characteristics varied significantly. │
│ Paragraph 6: As illustrated in Figure 1, outcomes improved. │
│                                                              │
│ ![Figure 1: Treatment Outcomes](outcomes.png)               │
│ **Figure 1: Treatment Outcomes Over Time**                  │
└──────────────────────────────────────────────────────────────┘
```

## Parallel Execution with Dependencies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DEPENDENCY GRAPH & EXECUTION                          │
└─────────────────────────────────────────────────────────────────────────┘

Dependency Graph:
                    ┌─────────────┐
                    │ Introduction│
                    └──────┬──────┘
                           │
                           │ depends on
                           ▼
                    ┌─────────────┐
                    │ Methodology │
                    └──────┬──────┘
                           │
                           │ depends on
                           ▼
    ┌──────────────┐   ┌─────────────┐   ┌──────────────┐
    │  Literature  │   │   Results   │   │              │
    │   Review     │   └──────┬──────┘   │              │
    └──────┬───────┘          │          │              │
           │                  │          │              │
           │                  │          │              │
           └──────────────┐   │          │              │
                          │   │ both     │              │
                          │   │ depend   │              │
                          │   │          │              │
                          ▼   ▼          │              │
                     ┌───────────────┐   │              │
                     │  Discussion   │   │              │
                     └───────┬───────┘   │              │
                             │           │              │
                             │ depends   │              │
                             ▼           ▼              │
                           ┌────────────────┐           │
                           │  Conclusion    │           │
                           └────────────────┘           │

Execution Timeline (with 4 workers):
Time →
─────────────────────────────────────────────────────────────►

Wave 1 [═══════════════════════════════════════════]
       │ Introduction (Worker 1)                  │
       │ Literature Review (Worker 2)             │
       │ Abstract (Worker 3)                      │

Wave 2          [════════════════════════════════]
                │ Methodology (Worker 1)         │

Wave 3                   [═══════════════════════════════]
                         │ Results (Worker 1)            │

Wave 4                               [═══════════════════════]
                                     │ Discussion (Worker 1)│
                                     │ Conclusion (Worker 2)│

Total Time: ~60% faster than sequential execution
```

## Integration with Graive AI Platform

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GRAIVE AI PLATFORM                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐       ┌────────────────────┐
│   LLM Providers    │       │  Tool Orchestrator │
│                    │       │                    │
│ • OpenAI           │◄──────┤ • Web Scraping     │
│ • DeepSeek         │       │ • Data Analysis    │
│ • Gemini           │       │ • Visualization    │
└─────────┬──────────┘       │ • Document Tools   │
          │                  └─────────┬──────────┘
          │                            │
          └────────────┬───────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │ Document Orchestrator  │
          │                        │
          │ • Planning             │
          │ • Agent Coordination   │
          │ • Assembly             │
          └────────────┬───────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │  Infinite Memory       │
          │                        │
          │ • Context compression  │
          │ • Semantic search      │
          │ • Unlimited history    │
          └────────────┬───────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │      Database          │
          │                        │
          │ • PostgreSQL           │
          │ • ChromaDB (vectors)   │
          │ • Plans & outputs      │
          └────────────────────────┘
```

## Human-in-the-Loop Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTERACTIVE GENERATION FLOW                           │
└─────────────────────────────────────────────────────────────────────────┘

1. PLAN REVIEW
   ┌──────────────────┐
   │  System: Created │
   │  plan with 7     │
   │  sections        │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐     ┌─────────────────┐
   │  User: Review    │────►│ Approve         │
   │                  │     │ Modify sections │
   │                  │     │ Adjust words    │
   └──────────────────┘     └─────────────────┘

2. SECTION REVIEW (for each section)
   ┌──────────────────────┐
   │  System: Completed   │
   │  Introduction        │
   │  15,234 words        │
   └────────┬─────────────┘
            │
            ▼
   ┌──────────────────────┐     ┌──────────────────┐
   │  User: Review content│────►│ Approve          │
   │                      │     │ Revise with notes│
   │                      │     │ Regenerate       │
   └──────────────────────┘     └──────────────────┘

3. FINAL REVIEW
   ┌──────────────────────┐
   │  System: Complete    │
   │  document assembled  │
   │  200,234 words       │
   └────────┬─────────────┘
            │
            ▼
   ┌──────────────────────┐     ┌──────────────────┐
   │  User: Final review  │────►│ Approve & export │
   │                      │     │ Request revisions│
   └──────────────────────┘     └──────────────────┘

All feedback logged for audit trail and reproducibility
```

## Summary

The Document Orchestration System provides a complete solution for ultra-long document generation through:

- **Intelligent Planning:** LLM-powered outline generation with dependency tracking
- **Specialized Expertise:** Domain-expert agents for different section types
- **Dynamic Code Generation:** Custom Python scripts for analysis and visualization
- **Smart Element Placement:** LaTeX-like positioning of tables and figures
- **Parallel Execution:** Dependency-aware waves for maximum speed
- **Human Oversight:** Interactive review at multiple stages
- **Publication Quality:** Professional formatting in multiple formats

**Result:** Generate 200,000-word PhD theses in 8-16 hours instead of 12-18 months, with intelligent structure, specialized writing, automatic analysis, and publication-ready formatting.
