"""
Document Planning Module

Implements multi-stage document planning that transforms high-level
requests into detailed generation blueprints before content creation.

This module addresses the critical architectural gap where the system
previously jumped directly to content generation without strategic planning.
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime


class DocumentSection:
    """
    Represents a planned section within a document structure.
    
    Each section contains metadata about its role, content requirements,
    media needs, and quality criteria that guide generation.
    """
    
    def __init__(
        self,
        title: str,
        level: int,
        word_count: int,
        key_points: List[str],
        media_specs: List[Dict[str, Any]],
        quality_criteria: Dict[str, Any]
    ):
        self.title = title
        self.level = level  # 1=main section, 2=subsection, etc.
        self.word_count = word_count
        self.key_points = key_points
        self.media_specs = media_specs
        self.quality_criteria = quality_criteria
        self.generated_content = None
        self.quality_score = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize section to dictionary."""
        return {
            'title': self.title,
            'level': self.level,
            'word_count': self.word_count,
            'key_points': self.key_points,
            'media_specs': self.media_specs,
            'quality_criteria': self.quality_criteria
        }


class DocumentPlan:
    """
    Complete document generation blueprint.
    
    Contains hierarchical structure, resource specifications,
    quality criteria, and generation strategy.
    """
    
    def __init__(
        self,
        title: str,
        topic: str,
        document_type: str,
        total_words: int
    ):
        self.title = title
        self.topic = topic
        self.document_type = document_type
        self.total_words = total_words
        self.sections: List[DocumentSection] = []
        self.citation_strategy: Dict[str, Any] = {}
        self.overall_quality_criteria: Dict[str, Any] = {}
        self.generation_metadata: Dict[str, Any] = {}
    
    def add_section(self, section: DocumentSection):
        """Add a section to the plan."""
        self.sections.append(section)
    
    def get_total_planned_words(self) -> int:
        """Calculate total words across all sections."""
        return sum(section.word_count for section in self.sections)
    
    def get_media_count(self) -> Dict[str, int]:
        """Count media elements by type."""
        counts = {'image': 0, 'table': 0, 'chart': 0}
        for section in self.sections:
            for media in section.media_specs:
                media_type = media.get('type', 'unknown')
                counts[media_type] = counts.get(media_type, 0) + 1
        return counts
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize plan to dictionary."""
        return {
            'title': self.title,
            'topic': self.topic,
            'document_type': self.document_type,
            'total_words': self.total_words,
            'sections': [s.to_dict() for s in self.sections],
            'citation_strategy': self.citation_strategy,
            'quality_criteria': self.overall_quality_criteria,
            'metadata': self.generation_metadata,
            'planned_words': self.get_total_planned_words(),
            'media_counts': self.get_media_count()
        }
    
    def save_plan(self, filepath: str):
        """Save plan to JSON file for transparency."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class DocumentPlanner:
    """
    Strategic document planning system.
    
    Analyzes document requirements and generates detailed blueprints
    that guide content generation, media integration, and quality control.
    """
    
    def __init__(self, llm_caller=None):
        """
        Initialize document planner.
        
        Args:
            llm_caller: Function to call LLM for analysis tasks
        """
        self.llm_caller = llm_caller
        
        # Document type templates
        self.templates = {
            'essay': {
                'structure': ['Introduction', 'Body', 'Conclusion'],
                'body_sections': 3,
                'intro_ratio': 0.15,
                'body_ratio': 0.70,
                'conclusion_ratio': 0.15,
                'citation_density': 10  # citations per 1000 words
            },
            'article': {
                'structure': ['Introduction', 'Main Content', 'Conclusion'],
                'body_sections': 4,
                'intro_ratio': 0.10,
                'body_ratio': 0.80,
                'conclusion_ratio': 0.10,
                'citation_density': 8
            },
            'paper': {
                'structure': ['Abstract', 'Introduction', 'Methodology', 'Results', 'Discussion', 'Conclusion'],
                'body_sections': 0,  # Predefined structure
                'intro_ratio': 0.15,
                'body_ratio': 0.70,
                'conclusion_ratio': 0.10,
                'citation_density': 15
            },
            'thesis': {
                'structure': ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results', 'Discussion', 'Conclusion'],
                'body_sections': 0,
                'intro_ratio': 0.10,
                'body_ratio': 0.75,
                'conclusion_ratio': 0.10,
                'citation_density': 20
            }
        }
    
    def create_plan(
        self,
        topic: str,
        word_count: int,
        document_type: str = 'essay',
        include_images: bool = False,
        include_tables: bool = False,
        target_audience: str = 'general',
        academic_level: str = 'undergraduate'
    ) -> DocumentPlan:
        """
        Generate complete document plan from requirements.
        
        This is the main planning method that orchestrates all planning phases.
        
        Args:
            topic: Document subject
            word_count: Target word count
            document_type: Type of document (essay, article, paper, thesis)
            include_images: Whether to plan for images
            include_tables: Whether to plan for tables
            target_audience: Intended readership
            academic_level: Academic sophistication level
        
        Returns:
            Complete document plan ready for generation
        """
        print(f"\n{'='*70}")
        print(f"📋 DOCUMENT PLANNING PHASE")
        print(f"{'='*70}")
        print(f"Topic: {topic}")
        print(f"Type: {document_type}")
        print(f"Words: {word_count}")
        print(f"Images: {include_images}")
        print(f"Tables: {include_tables}")
        print(f"{'='*70}\n")
        
        # Phase 1: Analyze topic and determine structure
        print("[Phase 1/5] 🧠 Analyzing topic and determining structure...")
        structure = self._analyze_topic_and_plan_structure(
            topic, document_type, word_count
        )
        print(f"           ✅ Structure planned: {len(structure['sections'])} sections\n")
        
        # Phase 2: Allocate word counts to sections
        print("[Phase 2/5] 📊 Allocating word counts to sections...")
        word_allocation = self._allocate_word_counts(
            structure, word_count, document_type
        )
        print(f"           ✅ Word allocation complete\n")
        
        # Phase 3: Plan media integration
        print("[Phase 3/5] 🖼️  Planning media integration...")
        media_plan = self._plan_media_integration(
            structure, include_images, include_tables
        )
        print(f"           ✅ Media plan: {media_plan['total_images']} images, {media_plan['total_tables']} tables\n")
        
        # Phase 4: Define citation strategy
        print("[Phase 4/5] 📚 Defining citation strategy...")
        citation_strategy = self._define_citation_strategy(
            document_type, word_count, academic_level
        )
        print(f"           ✅ Target citations: {citation_strategy['target_citations']}\n")
        
        # Phase 5: Establish quality criteria
        print("[Phase 5/5] 🎯 Establishing quality criteria...")
        quality_criteria = self._establish_quality_criteria(
            document_type, academic_level, target_audience
        )
        print(f"           ✅ Quality threshold: {quality_criteria['min_score']}/10\n")
        
        # Build complete plan
        plan = DocumentPlan(
            title=self._generate_title(topic),
            topic=topic,
            document_type=document_type,
            total_words=word_count
        )
        
        # Add sections with all specifications
        for i, section_spec in enumerate(structure['sections']):
            section = DocumentSection(
                title=section_spec['title'],
                level=section_spec['level'],
                word_count=word_allocation[i],
                key_points=section_spec.get('key_points', []),
                media_specs=media_plan['sections'][i] if i < len(media_plan['sections']) else [],
                quality_criteria=quality_criteria
            )
            plan.add_section(section)
        
        plan.citation_strategy = citation_strategy
        plan.overall_quality_criteria = quality_criteria
        plan.generation_metadata = {
            'created_at': datetime.now().isoformat(),
            'target_audience': target_audience,
            'academic_level': academic_level,
            'planner_version': '1.0'
        }
        
        print(f"{'='*70}")
        print(f"✅ PLANNING COMPLETE")
        print(f"{'='*70}")
        print(f"Sections: {len(plan.sections)}")
        print(f"Planned Words: {plan.get_total_planned_words()}")
        print(f"Images: {plan.get_media_count()['image']}")
        print(f"Tables: {plan.get_media_count()['table']}")
        print(f"{'='*70}\n")
        
        return plan
    
    def _analyze_topic_and_plan_structure(
        self,
        topic: str,
        document_type: str,
        word_count: int
    ) -> Dict[str, Any]:
        """
        Analyze topic and generate appropriate document structure.
        
        Uses LLM if available to create topic-specific structure,
        otherwise falls back to template-based structure.
        """
        template = self.templates.get(document_type, self.templates['essay'])
        
        if self.llm_caller:
            # Use LLM to analyze topic and suggest structure
            prompt = f"""Analyze the topic "{topic}" for a {document_type} of approximately {word_count} words.

Generate a detailed section structure with:
1. Main sections (3-5 sections)
2. Key points for each section
3. Logical flow between sections

Format your response as a structured outline.
Be specific and relevant to {topic}."""
            
            try:
                llm_structure = self.llm_caller(prompt, max_tokens=800)
                # Parse LLM response into structure
                # For now, use template with topic-specific titles
                sections = self._parse_llm_structure(llm_structure, topic)
                if sections:
                    return {'sections': sections}
            except Exception as e:
                print(f"           ⚠️  LLM analysis failed: {e}, using template")
        
        # Fallback: Template-based structure
        return self._generate_template_structure(topic, template)
    
    def _generate_template_structure(
        self,
        topic: str,
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate structure from document type template."""
        sections = []
        
        if template['body_sections'] == 0:
            # Use predefined structure (e.g., research paper)
            for section_name in template['structure']:
                sections.append({
                    'title': section_name,
                    'level': 1,
                    'key_points': [f'Key aspects of {section_name.lower()}']
                })
        else:
            # Generate dynamic body sections
            sections.append({
                'title': 'Introduction',
                'level': 1,
                'key_points': [f'Overview of {topic}', 'Thesis statement']
            })
            
            # Body sections with topic-specific focus
            for i in range(template['body_sections']):
                sections.append({
                    'title': f'Section {i+1}',  # Would be topic-specific with LLM
                    'level': 1,
                    'key_points': [f'Aspect {i+1} of {topic}']
                })
            
            sections.append({
                'title': 'Conclusion',
                'level': 1,
                'key_points': ['Summary', 'Future implications']
            })
        
        return {'sections': sections}
    
    def _parse_llm_structure(
        self,
        llm_response: str,
        topic: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Parse LLM-generated structure into section specifications."""
        # Simplified parsing - in production would use more sophisticated NLP
        lines = llm_response.strip().split('\n')
        sections = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect section headers (lines starting with numbers or ##)
            if line[0].isdigit() or line.startswith('##'):
                if current_section:
                    sections.append(current_section)
                
                title = line.split('.', 1)[-1].strip().strip('#').strip()
                current_section = {
                    'title': title,
                    'level': 1,
                    'key_points': []
                }
            elif current_section and (line.startswith('-') or line.startswith('•')):
                # Key point
                point = line.lstrip('-•').strip()
                current_section['key_points'].append(point)
        
        if current_section:
            sections.append(current_section)
        
        return sections if sections else None
    
    def _allocate_word_counts(
        self,
        structure: Dict[str, Any],
        total_words: int,
        document_type: str
    ) -> List[int]:
        """
        Allocate word counts to sections based on importance.
        
        Uses document type templates to determine proportions.
        """
        template = self.templates.get(document_type, self.templates['essay'])
        sections = structure['sections']
        num_sections = len(sections)
        
        allocation = []
        
        # Identify intro, body, conclusion
        intro_count = 1
        conclusion_count = 1
        body_count = num_sections - 2
        
        intro_words = int(total_words * template['intro_ratio'])
        conclusion_words = int(total_words * template['conclusion_ratio'])
        body_words = total_words - intro_words - conclusion_words
        
        # Allocate
        allocation.append(intro_words)  # Introduction
        
        # Distribute body words equally (could be weighted by importance)
        if body_count > 0:
            words_per_body = body_words // body_count
            for _ in range(body_count):
                allocation.append(words_per_body)
        
        allocation.append(conclusion_words)  # Conclusion
        
        # Adjust for rounding
        total_allocated = sum(allocation)
        if total_allocated < total_words:
            allocation[1] += (total_words - total_allocated)  # Add remainder to first body section
        
        return allocation
    
    def _plan_media_integration(
        self,
        structure: Dict[str, Any],
        include_images: bool,
        include_tables: bool
    ) -> Dict[str, Any]:
        """Plan where and what type of media to include."""
        sections = structure['sections']
        section_media = []
        
        total_images = 0
        total_tables = 0
        
        for i, section in enumerate(sections):
            media_specs = []
            
            # Skip intro and conclusion for media (usually)
            if i == 0 or i == len(sections) - 1:
                section_media.append(media_specs)
                continue
            
            # Add image to every other body section if requested
            if include_images and i % 2 == 1:
                media_specs.append({
                    'type': 'image',
                    'subject': f"Illustration for {section['title']}",
                    'placement': 'after_section',
                    'method': 'auto'
                })
                total_images += 1
            
            # Add table to middle sections if requested
            if include_tables and i == len(sections) // 2:
                media_specs.append({
                    'type': 'table',
                    'subject': f"Data for {section['title']}",
                    'rows': 5,
                    'columns': 3
                })
                total_tables += 1
            
            section_media.append(media_specs)
        
        return {
            'sections': section_media,
            'total_images': total_images,
            'total_tables': total_tables
        }
    
    def _define_citation_strategy(
        self,
        document_type: str,
        word_count: int,
        academic_level: str
    ) -> Dict[str, Any]:
        """Define citation requirements and strategy."""
        template = self.templates.get(document_type, self.templates['essay'])
        
        # Calculate target citations
        base_density = template['citation_density']
        
        # Adjust for academic level
        level_multiplier = {
            'high_school': 0.5,
            'undergraduate': 1.0,
            'graduate': 1.5,
            'phd': 2.0
        }.get(academic_level, 1.0)
        
        citations_per_1000 = base_density * level_multiplier
        target_citations = int((word_count / 1000) * citations_per_1000)
        
        return {
            'target_citations': target_citations,
            'citation_format': 'APA',
            'min_sources': max(5, target_citations // 3),
            'source_types': {
                'journal_articles': 0.6,
                'books': 0.25,
                'web_sources': 0.15
            },
            'year_range': (2018, 2025)  # Recent sources preferred
        }
    
    def _establish_quality_criteria(
        self,
        document_type: str,
        academic_level: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Establish quality thresholds and criteria."""
        # Base quality thresholds
        min_scores = {
            'high_school': 6.0,
            'undergraduate': 7.0,
            'graduate': 8.0,
            'phd': 8.5
        }
        
        return {
            'min_score': min_scores.get(academic_level, 7.0),
            'dimensions': [
                'clarity',
                'coherence',
                'depth',
                'citations',
                'structure',
                'originality',
                'grammar',
                'tone'
            ],
            'revision_limit': 3,
            'target_audience': target_audience,
            'academic_level': academic_level
        }
    
    def _generate_title(self, topic: str) -> str:
        """Generate appropriate document title from topic."""
        # Capitalize properly
        words = topic.split()
        title_words = [w.capitalize() for w in words]
        return ' '.join(title_words)


def create_document_planner(llm_caller=None) -> DocumentPlanner:
    """
    Factory function to create document planner.
    
    Args:
        llm_caller: Function to call LLM for analysis
    
    Returns:
        Configured DocumentPlanner instance
    """
    return DocumentPlanner(llm_caller)
