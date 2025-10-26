# Graive AI Quality System - Quick Reference

## What's New

Your system now includes **PhD-level quality review** and **professional document formatting** that ensures every document meets the highest academic standards before delivery to clients.

## The 6-Phase Quality Pipeline

### Phase 1: Initial Content Generation (15-30 seconds)
- Connects to OpenAI/DeepSeek API
- Generates content with academic prompts
- Shows real-time progress and word count
- **Output**: Raw academic content

### Phase 2: PhD-Level Review (10-15 seconds)
- **8 Quality Dimensions Assessed**:
  1. Clarity & Readability
  2. Logical Coherence
  3. Content Depth
  4. Citations & References
  5. Document Structure
  6. Originality & Analysis
  7. Grammar & Language
  8. Academic Tone

- **Scoring**: Each dimension rated 0-10
- **Overall Score**: Average across all dimensions
- **Threshold**: Must achieve 8.0/10 or higher

### Phase 3: Automatic Revision (if needed, 20-40 seconds)
- **Triggered**: If overall score < 8.0/10
- **Iterations**: Up to 3 automatic revisions
- **Targeting**: Focuses on lowest-scoring dimensions
- **Re-assessment**: Each iteration is re-reviewed
- **Output**: Revised content meeting PhD standards

### Phase 4: Image Integration (instant)
- Generates image placeholders or AI-generated visuals
- Proper captions and numbering
- Strategic placement in document
- **Optional**: Can be disabled if not needed

### Phase 5: Table Addition (1-2 seconds per table)
- Generates data tables relevant to topic
- Professional formatting with headers
- Proper markdown/Word table structure
- **Optional**: Can be disabled if not needed

### Phase 6: Professional Formatting (5-10 seconds)
- Applies academic styling
- Generates table of contents
- Adds headers, footers, page numbers
- Exports to requested format (MD/DOCX/PDF)
- **Output**: Publication-ready document

## Quality Score Interpretation

| Score Range | Quality Level | Action | Client Readiness |
|-------------|---------------|--------|------------------|
| 9.0 - 10.0 | EXCELLENT | Deliver immediately | Exceeds expectations |
| 8.0 - 8.9 | GOOD | Deliver | Meets PhD standards |
| 7.0 - 7.9 | ACCEPTABLE | Optional revision | Minor improvements possible |
| Below 7.0 | NEEDS WORK | Automatic revision | Not ready for delivery |

## Example Session

```
You: write an essay about climate change in 2000 words with images and tables

======================================================================
📝 DOCUMENT GENERATION - CLIMATE CHANGE
======================================================================
Target: 2000 words | Format: MD
Quality: PhD-Level Review ENABLED
======================================================================

[Step 1/6] 🤖 Generating initial content...
           🟢 Using OpenAI GPT-3.5-Turbo-16K
           ✅ Generated 2047 words

[Step 2/6] 🎓 PhD-Level Quality Review...

[1/8] Assessing clarity... Score: 8.5/10
[2/8] Analyzing coherence... Score: 7.8/10  
[3/8] Evaluating depth... Score: 9.0/10
[4/8] Verifying citations... Score: 7.2/10
[5/8] Checking structure... Score: 9.0/10
[6/8] Assessing originality... Score: 8.0/10
[7/8] Reviewing grammar... Score: 9.0/10
[8/8] Evaluating tone... Score: 8.5/10

📊 OVERALL QUALITY SCORE: 8.38/10
✅ GOOD - Meets PhD standards

[Step 3/6] 🖼️  Adding images...
           ✅ Added 3 images

[Step 4/6] 📊 Adding tables...
           ✅ Added 2 tables

[Step 5/6] 📝 Professional formatting...
           ✅ Document professionally formatted

[Step 6/6] 📊 Final quality verification...
           Quality Score: 8.38/10
           Revision Iterations: 0
           ✅ Quality verification complete

======================================================================
✅ DOCUMENT GENERATION COMPLETE
======================================================================
📄 File: climate_change_20251026_163422.md
📊 Words: 2047
🎓 Quality Score: 8.38/10 (GOOD)
🖼️  Images: 3
📈 Tables: 2
======================================================================
```

## When Revision is Triggered

If initial content scores below 8.0/10, you'll see:

```
📊 OVERALL QUALITY SCORE: 7.6/10
❌ NEEDS IMPROVEMENT - Significant revision required

🔄 Quality below threshold - starting revision...

[Iteration 1/3] Revising content...
   Applying revisions for:
   • CITATIONS: Good use of citations, could add more support
   • COHERENCE: Good coherence, could benefit from more transitions

[Iteration 1] Re-reviewing revised content...
📊 OVERALL QUALITY SCORE: 8.2/10
📈 Improvement: +0.6 points
✅ Quality threshold met after 1 iteration(s)
```

## Benefits

### For Clients
✅ **Guaranteed Quality**: Every document ≥ 8.0/10 PhD-level standard  
✅ **Transparent Scoring**: See exact quality metrics  
✅ **Professional Format**: Publication-ready output  
✅ **No Revisions Needed**: Content pre-vetted before delivery

### For You
✅ **Automated QA**: No manual review required  
✅ **Progress Tracking**: See every step in real-time  
✅ **Error Prevention**: Issues caught before delivery  
✅ **Client Confidence**: Deliver with quality guarantee

## How to Use

### Enable PhD Review (Default)
```python
result = graive.generate_document(
    topic="Your Topic",
    word_count=2000,
    enable_phd_review=True  # This is the default
)
```

### Disable if You Want Faster Generation
```python
result = graive.generate_document(
    topic="Your Topic",
    word_count=1000,
    enable_phd_review=False  # Skips review, faster but no quality guarantee
)
```

### Request Professional Formatting
```python
result = graive.generate_document(
    topic="Your Topic",
    output_format="docx",  # Word document with professional styling
    include_images=True,
    include_tables=True
)
```

## Quality Dimensions Explained

**Clarity**: Can readers easily understand the content?  
**Coherence**: Do ideas flow logically from one to the next?  
**Depth**: Is analysis thorough and comprehensive?  
**Citations**: Are claims properly supported with sources?  
**Structure**: Is the document well-organized?  
**Originality**: Does content show critical thinking?  
**Grammar**: Is language formal and error-free?  
**Tone**: Is the writing objective and academic?

## Files Generated

All documents saved to:
```
workspace/documents/
  ├── topic_name_20251026_163422.md      (Markdown)
  ├── topic_name_20251026_163422.docx    (Word) 
  └── topic_name_20251026_163422_formatted.md (With metadata)
```

Images (when generated):
```
workspace/images/
  ├── topic_name_figure_1.png
  ├── topic_name_figure_2.png
  └── topic_name_figure_3.png
```

## System Requirements

**Included**: PhD Review System, Document Formatter  
**Optional**: python-docx (for Word export)  
**APIs**: OpenAI or DeepSeek (for content generation)

## Quick Commands

```
You: write essay about [topic] in [number] words with images and tables
     → Generates PhD-reviewed document with full pipeline

You: cost-report
     → Shows API usage costs

You: reflection-report  
     → Shows all system activities
```

---

**Your documents now undergo the same rigorous review process as PhD dissertations, ensuring clients receive only the highest quality academic content.**
