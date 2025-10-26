# 📋 Document Planner Integration - Complete Implementation Guide

## Overview

You've correctly identified that the current [generate_document()](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py#L477-L682) method bypasses the planning stage and proceeds directly to content generation. This document provides the complete integration strategy to transform the execution flow into a proper plan-then-generate architecture.

## ✅ What's Been Implemented

### Document Planner Module (COMPLETE)

**File Created**: [src/planning/document_planner.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\src\planning\document_planner.py) (550 lines)

The planner implements a comprehensive 5-phase planning process:

#### Phase 1: Topic Analysis and Structure Determination

The planner analyzes the requested topic and generates an appropriate document structure. When LLM access is available, it uses AI to create topic-specific section titles and key points. When LLM is unavailable, it falls back to template-based structures that adapt to the document type (essay, article, paper, thesis).

```python
def _analyze_topic_and_plan_structure(self, topic, document_type, word_count):
    # Attempts LLM-based analysis first
    # Falls back to template-based structure
    return {'sections': [list of section specifications]}
```

#### Phase 2: Word Count Allocation

Based on document type templates, the planner distributes the total word count across sections using proportional allocation. Introduction and conclusion receive fixed percentages while body sections share the remainder equally or according to importance weights.

```python
def _allocate_word_counts(self, structure, total_words, document_type):
    # Uses template ratios (intro: 15%, body: 70%, conclusion: 15%)
    return [list of word counts per section]
```

#### Phase 3: Media Integration Planning

The planner determines optimal locations for images and tables based on section content and document flow. It avoids placing media in introductions and conclusions, distributing visual elements strategically throughout body sections.

```python
def _plan_media_integration(self, structure, include_images, include_tables):
    return {
        'sections': [media specs per section],
        'total_images': count,
        'total_tables': count
    }
```

#### Phase 4: Citation Strategy Definition

Based on document type and academic level, the planner calculates appropriate citation density, determines minimum source requirements, and establishes the balance between source types (journal articles, books, web sources).

```python
def _define_citation_strategy(self, document_type, word_count, academic_level):
    return {
        'target_citations': calculated count,
        'citation_format': 'APA',
        'min_sources': minimum required,
        'source_types': proportional distribution
    }
```

#### Phase 5: Quality Criteria Establishment

The planner sets quality thresholds based on academic level, defines which quality dimensions to evaluate, and establishes revision limits to prevent infinite improvement loops.

```python
def _establish_quality_criteria(self, document_type, academic_level, target_audience):
    return {
        'min_score': threshold (6.0-8.5),
        'dimensions': list of 8 quality dimensions,
        'revision_limit': 3
    }
```

### Planner Initialization (COMPLETE)

**Modified File**: [graive.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py) lines 252-270

The document planner is now initialized during system startup as step 12/12:

```python
# 12. Initialize Document Planner (CRITICAL - NEW!)
print("\n[12/12] Initializing Strategic Document Planner...")
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
```

### Detection Priority Fix (COMPLETE)

**Modified File**: [graive.py](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py) lines 1177-1195

Questions and complaints are now detected first and routed to chat, preventing false task execution. Document generation requires both topic extraction AND creation verb verification to avoid misclassification.

## ⚠️ What Needs Integration

### Modified generate_document() Method

The current [generate_document()](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py#L477-L682) method needs to be replaced with a planner-first implementation. Here's the complete new implementation:

```python
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
    Generate document using plan-then-generate architecture.
    
    NEW FLOW:
    1. Create detailed document plan
    2. Generate content section-by-section
    3. Integrate planned media
    4. Review and revise
    5. Format and save
    
    Args:
        topic: Document subject
        word_count: Target word count
        include_images: Include images
        include_tables: Include tables
        output_format: Output format (md, docx, pdf)
        enable_phd_review: Enable quality review
        document_type: Type (essay, article, paper, thesis)
        academic_level: Academic level (undergraduate, graduate, phd)
    
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
            print(f"Quality: PhD-Level Review ENABLED")
        print(f"{'='*70}\n")
        
        # CRITICAL: Use planner if available, otherwise fallback to direct generation
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
        else:
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
    """
    Generate document using strategic planning.
    
    PLAN-THEN-GENERATE ARCHITECTURE:
    This method implements the proper multi-stage pipeline.
    """
    
    # STAGE 1: CREATE PLAN
    print("=" * 70)
    print("STAGE 1: STRATEGIC PLANNING")
    print("=" * 70 + "\n")
    
    plan = self.document_planner.create_plan(
        topic=topic,
        word_count=word_count,
        document_type=document_type,
        include_images=include_images,
        include_tables=include_tables,
        target_audience="academic",
        academic_level=academic_level
    )
    
    # Save plan for transparency
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = re.sub(r'[^\w\s-]', '', topic).strip().replace(' ', '_')
    plan_file = self.session_workspace / "plans" / f"{safe_topic}_plan_{timestamp}.json"
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    plan.save_plan(str(plan_file))
    print(f"💾 Plan saved: {plan_file.name}\n")
    
    # STAGE 2: GENERATE CONTENT SECTION-BY-SECTION
    print("=" * 70)
    print("STAGE 2: CONTENT GENERATION")
    print("=" * 70 + "\n")
    
    generated_sections = []
    total_words = 0
    
    for i, section in enumerate(plan.sections, 1):
        print(f"[Section {i}/{len(plan.sections)}] Generating: {section.title}")
        print(f"                Target: {section.word_count} words")
        
        # Generate section content
        section_prompt = self._build_section_prompt(
            section_title=section.title,
            key_points=section.key_points,
            word_count=section.word_count,
            topic=topic,
            previous_sections=generated_sections
        )
        
        section_content = self._call_llm_for_content(section_prompt, max_tokens=section.word_count * 2)
        section_words = len(section_content.split())
        total_words += section_words
        
        # Quality check for this section
        if enable_phd_review and self.review_system:
            section_quality = self.review_system.assess_section_quality(section_content)
            if section_quality < 7.0:
                print(f"                ⚠️  Quality: {section_quality:.1f}/10 - revising...")
                section_content = self._revise_section(section_content, section_quality)
                section_quality = self.review_system.assess_section_quality(section_content)
                print(f"                ✅  Revised: {section_quality:.1f}/10")
            else:
                print(f"                ✅  Quality: {section_quality:.1f}/10")
        
        generated_sections.append({
            'title': section.title,
            'content': section_content,
            'word_count': section_words,
            'media_specs': section.media_specs
        })
        
        print(f"                ✓ Generated: {section_words} words\n")
    
    print(f"✅ All sections generated: {total_words} total words\n")
    
    # STAGE 3: MEDIA GENERATION
    print("=" * 70)
    print("STAGE 3: MEDIA INTEGRATION")
    print("=" * 70 + "\n")
    
    generated_media = []
    
    for i, section in enumerate(generated_sections):
        if section['media_specs']:
            for media_spec in section['media_specs']:
                if media_spec['type'] == 'image' and self.image_generator:
                    print(f"🖼️  Generating image: {media_spec['subject']}")
                    
                    img_result = self.image_generator.generate_image(
                        description=media_spec['subject'],
                        method=media_spec.get('method', 'auto')
                    )
                    
                    if img_result['success']:
                        generated_media.append({
                            'type': 'image',
                            'section_index': i,
                            'path': img_result['path'],
                            'description': media_spec['subject']
                        })
                        print(f"   ✅ Image created: {img_result['filename']}\n")
                
                elif media_spec['type'] == 'table':
                    print(f"📊 Generating table: {media_spec['subject']}")
                    
                    table_content = self._generate_table_for_section(
                        subject=media_spec['subject'],
                        topic=topic,
                        rows=media_spec.get('rows', 5),
                        columns=media_spec.get('columns', 3)
                    )
                    
                    generated_media.append({
                        'type': 'table',
                        'section_index': i,
                        'markdown': table_content,
                        'subject': media_spec['subject']
                    })
                    print(f"   ✅ Table created\n")
    
    print(f"✅ Media integration complete: {len(generated_media)} items\n")
    
    # STAGE 4: DOCUMENT ASSEMBLY
    print("=" * 70)
    print("STAGE 4: DOCUMENT ASSEMBLY")
    print("=" * 70 + "\n")
    
    document_content = self._assemble_document(
        title=plan.title,
        sections=generated_sections,
        media=generated_media,
        citations=plan.citation_strategy
    )
    
    print(f"✅ Document assembled: {len(document_content)} characters\n")
    
    # STAGE 5: FINAL QUALITY REVIEW
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
        
        if review_report['needs_revision']:
            print(f"🔄 Overall quality: {review_report['average_score']:.2f}/10 - revising...\n")
            document_content = self.review_system.revise_content(
                content=document_content,
                review_report=review_report,
                topic=topic,
                max_iterations=2
            )
            # Re-evaluate
            review_report = self.review_system.review_content(
                content=document_content,
                topic=topic
            )
            print(f"✅ Revised quality: {review_report['average_score']:.2f}/10\n")
        else:
            print(f"✅ Quality approved: {review_report['average_score']:.2f}/10\n")
    
    # STAGE 6: FORMAT AND SAVE
    print("=" * 70)
    print("STAGE 6: FORMATTING AND PERSISTENCE")
    print("=" * 70 + "\n")
    
    file_name = f"{safe_topic}_{timestamp}.{output_format}"
    file_path = str(self.session_workspace / "documents" / file_name)
    
    docs_dir = self.session_workspace / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    if self.document_formatter and output_format in ["docx", "pdf"]:
        print(f"📝 Applying professional formatting...")
        format_result = self.document_formatter.format_document(
            content=document_content,
            title=plan.title,
            author="Graive AI",
            output_format=output_format
        )
        file_path = format_result['file_path']
        print(f"   ✅ Professionally formatted\n")
    else:
        print(f"💾 Saving to file...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(document_content)
        file_size = os.path.getsize(file_path)
        print(f"   ✅ File written ({file_size:,} bytes)\n")
    
    # Track for future reference
    self.last_generated_document = file_path
    
    # Final summary
    print("=" * 70)
    print("✅ DOCUMENT GENERATION COMPLETE")
    print("=" * 70)
    print(f"📄 File: {Path(file_path).name}")
    print(f"📍 Location: {file_path}")
    print(f"📊 Words: {total_words}")
    if enable_phd_review and review_report:
        print(f"🎓 Quality: {review_report['average_score']:.2f}/10 ({review_report['quality_level']})")
    print(f"🖼️  Images: {len([m for m in generated_media if m['type'] == 'image'])}")
    print(f"📈 Tables: {len([m for m in generated_media if m['type'] == 'table'])}")
    print(f"📋 Plan: {plan_file.name}")
    print("=" * 70 + "\n")
    
    return {
        "success": True,
        "file_path": file_path,
        "word_count": total_words,
        "sections": len(generated_sections),
        "images": len([m for m in generated_media if m['type'] == 'image']),
        "tables": len([m for m in generated_media if m['type'] == 'table']),
        "plan_file": str(plan_file),
        "quality_score": review_report['average_score'] if review_report else None
    }


def _build_section_prompt(self, section_title, key_points, word_count, topic, previous_sections):
    """Build prompt for section generation with context."""
    context = ""
    if previous_sections:
        context = "Previous sections covered:\n"
        for prev in previous_sections[-2:]:  # Last 2 sections for context
            context += f"- {prev['title']}: {prev['content'][:200]}...\n"
        context += "\n"
    
    prompt = f"""{context}Write the section titled "{section_title}" for a document about {topic}.

Requirements:
- Target length: {word_count} words
- Key points to address: {', '.join(key_points)}
- Use professional academic style
- Include specific details and examples
- Maintain coherent flow with previous content
- Do NOT repeat information from previous sections

Begin writing the {section_title} section:"""
    
    return prompt


def _assemble_document(self, title, sections, media, citations):
    """Assemble complete document from sections and media."""
    content = f"# {title}\n\n"
    
    for i, section in enumerate(sections):
        # Add section
        content += f"## {section['title']}\n\n"
        content += section['content'] + "\n\n"
        
        # Add media for this section
        section_media = [m for m in media if m.get('section_index') == i]
        for media_item in section_media:
            if media_item['type'] == 'image':
                content += f"![{media_item['description']}]({media_item['path']})\n\n"
                content += f"*Figure: {media_item['description']}*\n\n"
            elif media_item['type'] == 'table':
                content += media_item['markdown'] + "\n\n"
    
    return content
```

## Integration Steps

### Step 1: Replace generate_document() Method

Replace the current [generate_document()](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py#L477-L682) method with the new implementation above. This requires replacing approximately 200 lines starting at line 477.

### Step 2: Add Helper Methods

Add the new helper methods:
- `_generate_document_with_planner()` - Main planner-based generation
- `_generate_document_direct()` - Fallback for when planner unavailable (rename current generate_document logic)
- `_build_section_prompt()` - Creates contextual prompts for sections
- `_assemble_document()` - Combines sections and media

### Step 3: Update Interactive Mode

The [interactive_mode()](file://c:\Users\GEMTECH%201\Desktop\GRAIVE\graive.py#L1583-1604) handler already calls `generate_document()` correctly, so no changes needed there. The enhanced parameters will be passed through automatically.

### Step 4: Testing

Test the complete pipeline with:

```python
python graive.py

You: create an essay about africa and put an image inside
```

Expected output should show:
```
📋 DOCUMENT PLANNING PHASE
[Phase 1/5] 🧠 Analyzing topic...
[Phase 2/5] 📊 Allocating word counts...
[Phase 3/5] 🖼️  Planning media...
[Phase 4/5] 📚 Defining citations...
[Phase 5/5] 🎯 Establishing quality...

STAGE 1: STRATEGIC PLANNING
✅ PLANNING COMPLETE

STAGE 2: CONTENT GENERATION
[Section 1/5] Generating: Introduction
...
```

## Benefits of Planner Integration

### ✅ Structured Approach

Documents are generated with deliberate structure rather than ad-hoc organization. Each section has defined purpose, word allocation, and quality criteria established before generation begins.

### ✅ Intelligent Media Placement

Images and tables are integrated at semantically appropriate locations based on the plan rather than appended arbitrarily. Media enhances rather than interrupts the narrative flow.

### ✅ Granular Quality Control

Section-by-section generation enables targeted quality assessment and revision. Weak sections can be improved without regenerating the entire document.

### ✅ Cost Optimization

Generating sections individually with context allows for smaller, more efficient API calls. Failed sections can be regenerated without discarding successful content.

### ✅ Transparency

The saved plan file provides complete documentation of the generation strategy, enabling users to understand how decisions were made and potentially modify the plan before execution.

## Current Status

### ✅ Implemented
- Document planner module (550 lines)
- Planner initialization in graive.py
- Detection priority fixes
- Plan saving and loading infrastructure

### ⚠️ Ready for Integration
- New `generate_document()` implementation (provided above)
- Helper methods for section generation and assembly
- Fallback logic when planner unavailable

### 🎯 Next Step

Replace the current direct-generation implementation of `generate_document()` with the planner-based implementation provided in this guide. This single change will transform the entire pipeline from chat-like monolithic generation to professional multi-stage document creation.

The architecture is complete. The planner is implemented. The integration code is ready. The system just needs the final connection to activate the plan-then-generate pipeline.
