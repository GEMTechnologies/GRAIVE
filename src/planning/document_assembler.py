"""
Document Assembly and Element Placement Engine

This module handles intelligent placement of document elements (tables, figures,
equations) within the generated content. It analyzes text flow, identifies optimal
positions, manages numbering, and ensures proper cross-references.

Similar to Overleaf's smart positioning, this engine places elements near their
textual references while maintaining document flow and readability.
"""

from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import re
from enum import Enum


class PlacementStrategy(Enum):
    """Strategies for element placement."""
    NEAR_REFERENCE = "near_reference"  # Place near first textual reference
    END_OF_SECTION = "end_of_section"  # Place at end of section
    DEDICATED_PAGE = "dedicated_page"  # Place on dedicated page
    APPENDIX = "appendix"  # Place in appendix
    INLINE = "inline"  # Inline with text


@dataclass
class TextReference:
    """A reference to an element within text."""
    element_id: str
    reference_text: str  # e.g., "as shown in Figure 1"
    position: int  # Character position in text
    paragraph_index: int
    sentence_index: int


@dataclass
class PlacedElement:
    """An element with determined placement position."""
    element: Any  # DocumentElement
    placement_position: int  # Character position for insertion
    paragraph_index: int
    caption_number: int
    cross_references: List[TextReference]


class DocumentAssembler:
    """
    Intelligent document assembly system that combines sections and places
    elements (tables, figures) optimally within the document flow.
    """
    
    def __init__(self):
        """Initialize document assembler."""
        self.figure_counter = 0
        self.table_counter = 0
        self.equation_counter = 0
        self.placement_history: List[PlacedElement] = []
    
    def assemble_document(
        self,
        sections: List[Dict[str, Any]],
        elements: List[Any],
        style_guide: Dict[str, Any]
    ) -> str:
        """
        Assemble complete document from sections with intelligent element placement.
        
        Args:
            sections: List of section outputs from specialized agents
            elements: List of DocumentElement objects to place
            style_guide: Global style guide for formatting
        
        Returns:
            Complete assembled document as string
        """
        assembled_parts = []
        
        # Process each section
        for section in sections:
            # Find elements belonging to this section
            section_elements = [
                elem for elem in elements
                if elem.section_id == section["section_id"]
            ]
            
            # Assemble section with elements
            section_content = self._assemble_section(
                section["content"],
                section_elements,
                style_guide
            )
            
            assembled_parts.append(section_content)
        
        # Combine all sections
        full_document = "\n\n".join(assembled_parts)
        
        # Post-processing
        full_document = self._apply_formatting(full_document, style_guide)
        full_document = self._generate_table_of_contents(full_document)
        full_document = self._update_cross_references(full_document)
        
        return full_document
    
    def _assemble_section(
        self,
        content: str,
        elements: List[Any],
        style_guide: Dict[str, Any]
    ) -> str:
        """
        Assemble section with intelligent element placement.
        
        Analyzes the text to find references to elements, determines optimal
        placement positions, inserts elements with proper captions and numbering.
        """
        if not elements:
            return content
        
        # Parse content into paragraphs
        paragraphs = self._parse_paragraphs(content)
        
        # Find all element references in text
        references = self._find_element_references(paragraphs, elements)
        
        # Determine placement for each element
        placements = self._determine_placements(elements, references, paragraphs)
        
        # Insert elements at determined positions
        assembled_content = self._insert_elements(paragraphs, placements, style_guide)
        
        return assembled_content
    
    def _parse_paragraphs(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse content into paragraphs with metadata.
        
        Returns list of paragraphs with text, position, and sentence information.
        """
        paragraphs = []
        current_pos = 0
        
        # Split by double newlines (paragraphs)
        raw_paragraphs = content.split('\n\n')
        
        for para_idx, para_text in enumerate(raw_paragraphs):
            if not para_text.strip():
                continue
            
            sentences = self._split_sentences(para_text)
            
            paragraphs.append({
                "index": para_idx,
                "text": para_text,
                "start_pos": current_pos,
                "end_pos": current_pos + len(para_text),
                "sentences": sentences,
                "word_count": len(para_text.split())
            })
            
            current_pos += len(para_text) + 2  # Account for '\n\n'
        
        return paragraphs
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split paragraph into sentences."""
        # Simple sentence splitting (would use more sophisticated approach in production)
        sentence_endings = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentence_endings if s.strip()]
    
    def _find_element_references(
        self,
        paragraphs: List[Dict[str, Any]],
        elements: List[Any]
    ) -> Dict[str, List[TextReference]]:
        """
        Find all textual references to elements.
        
        Searches for patterns like "Figure 1", "Table 2", "as shown in",
        "the following table", etc.
        """
        references = {elem.element_id: [] for elem in elements}
        
        # Reference patterns
        patterns = {
            "table": [
                r'\btable\s+(\d+)\b',
                r'\bthe\s+(?:following|above|below)\s+table\b',
                r'\bas\s+shown\s+in\s+table\b'
            ],
            "figure": [
                r'\bfigure\s+(\d+)\b',
                r'\bfig\.\s+(\d+)\b',
                r'\bthe\s+(?:following|above|below)\s+figure\b',
                r'\bas\s+shown\s+in\s+figure\b'
            ]
        }
        
        for paragraph in paragraphs:
            para_text = paragraph["text"].lower()
            
            for sentence_idx, sentence in enumerate(paragraph["sentences"]):
                sentence_lower = sentence.lower()
                
                # Check each element type
                for elem in elements:
                    elem_type = elem.element_type.value
                    
                    if elem_type in patterns:
                        for pattern in patterns[elem_type]:
                            matches = re.finditer(pattern, sentence_lower, re.IGNORECASE)
                            
                            for match in matches:
                                ref = TextReference(
                                    element_id=elem.element_id,
                                    reference_text=match.group(0),
                                    position=paragraph["start_pos"] + sentence_lower.find(match.group(0)),
                                    paragraph_index=paragraph["index"],
                                    sentence_index=sentence_idx
                                )
                                references[elem.element_id].append(ref)
        
        return references
    
    def _determine_placements(
        self,
        elements: List[Any],
        references: Dict[str, List[TextReference]],
        paragraphs: List[Dict[str, Any]]
    ) -> List[PlacedElement]:
        """
        Determine optimal placement position for each element.
        
        Considers:
        - Proximity to textual reference
        - Document flow
        - Page break considerations
        - Element size
        - User-specified placement hints
        """
        placements = []
        
        for element in elements:
            elem_refs = references.get(element.element_id, [])
            
            # Determine placement strategy
            strategy = self._choose_placement_strategy(element, elem_refs)
            
            # Calculate placement position
            if strategy == PlacementStrategy.NEAR_REFERENCE and elem_refs:
                # Place after paragraph containing first reference
                first_ref = min(elem_refs, key=lambda r: r.position)
                target_paragraph = paragraphs[first_ref.paragraph_index]
                placement_pos = target_paragraph["end_pos"]
                para_idx = first_ref.paragraph_index
            
            elif strategy == PlacementStrategy.END_OF_SECTION:
                # Place at end of last paragraph
                last_para = paragraphs[-1]
                placement_pos = last_para["end_pos"]
                para_idx = last_para["index"]
            
            else:
                # Default: after first paragraph
                first_para = paragraphs[0]
                placement_pos = first_para["end_pos"]
                para_idx = 0
            
            # Assign caption number
            caption_number = self._get_next_caption_number(element.element_type)
            
            placed = PlacedElement(
                element=element,
                placement_position=placement_pos,
                paragraph_index=para_idx,
                caption_number=caption_number,
                cross_references=elem_refs
            )
            
            placements.append(placed)
        
        # Sort by placement position
        placements.sort(key=lambda p: p.placement_position)
        
        return placements
    
    def _choose_placement_strategy(
        self,
        element: Any,
        references: List[TextReference]
    ) -> PlacementStrategy:
        """Choose placement strategy based on element and references."""
        
        # Check user hint
        if hasattr(element, 'placement_hint'):
            hint_map = {
                "near_reference": PlacementStrategy.NEAR_REFERENCE,
                "end_of_section": PlacementStrategy.END_OF_SECTION,
                "appendix": PlacementStrategy.APPENDIX
            }
            if element.placement_hint in hint_map:
                return hint_map[element.placement_hint]
        
        # Default strategy based on references
        if references:
            return PlacementStrategy.NEAR_REFERENCE
        else:
            return PlacementStrategy.END_OF_SECTION
    
    def _get_next_caption_number(self, element_type: Any) -> int:
        """Get next caption number for element type."""
        if element_type.value == "figure":
            self.figure_counter += 1
            return self.figure_counter
        elif element_type.value == "table":
            self.table_counter += 1
            return self.table_counter
        elif element_type.value == "equation":
            self.equation_counter += 1
            return self.equation_counter
        return 0
    
    def _insert_elements(
        self,
        paragraphs: List[Dict[str, Any]],
        placements: List[PlacedElement],
        style_guide: Dict[str, Any]
    ) -> str:
        """
        Insert elements into paragraphs at determined positions.
        
        Generates properly formatted element insertions with captions,
        numbering, and spacing.
        """
        # Build paragraph insertion map
        insertions = {}
        for placement in placements:
            para_idx = placement.paragraph_index
            if para_idx not in insertions:
                insertions[para_idx] = []
            insertions[para_idx].append(placement)
        
        # Assemble content with insertions
        result_parts = []
        
        for paragraph in paragraphs:
            # Add paragraph text
            result_parts.append(paragraph["text"])
            
            # Add any elements that should be placed after this paragraph
            if paragraph["index"] in insertions:
                for placement in insertions[paragraph["index"]]:
                    element_text = self._format_element(placement, style_guide)
                    result_parts.append(element_text)
        
        return "\n\n".join(result_parts)
    
    def _format_element(
        self,
        placement: PlacedElement,
        style_guide: Dict[str, Any]
    ) -> str:
        """
        Format element with caption and proper styling.
        
        Generates markdown/LaTeX formatted element with caption, number,
        and styling according to style guide.
        """
        element = placement.element
        elem_type = element.element_type.value
        caption_num = placement.caption_number
        
        # Get caption position from style guide
        caption_config = style_guide.get(f"{elem_type}_caption", {})
        caption_position = caption_config.get("position", "below")
        
        # Format caption
        caption_text = f"{elem_type.title()} {caption_num}: {element.title}"
        
        # Format element content
        if elem_type == "table":
            content = self._format_table(element.content)
        elif elem_type == "figure":
            content = self._format_figure(element.content)
        else:
            content = str(element.content)
        
        # Assemble with caption
        if caption_position == "above":
            formatted = f"\n\n**{caption_text}**\n\n{content}\n\n"
        else:  # below
            formatted = f"\n\n{content}\n\n**{caption_text}**\n\n"
        
        return formatted
    
    def _format_table(self, table_content: Any) -> str:
        """Format table in markdown."""
        if isinstance(table_content, str):
            return table_content
        
        # Would generate proper markdown table from data structure
        return "| Column 1 | Column 2 |\n|----------|----------|\n| Data 1   | Data 2   |"
    
    def _format_figure(self, figure_content: Any) -> str:
        """Format figure reference in markdown."""
        if isinstance(figure_content, str):
            # Assume it's a file path
            return f"![Figure]({figure_content})"
        
        return "[Figure placeholder]"
    
    def _apply_formatting(self, content: str, style_guide: Dict[str, Any]) -> str:
        """Apply global formatting rules to document."""
        # Would apply formatting like:
        # - Heading styles
        # - Paragraph spacing
        # - Font specifications
        # - Line spacing
        return content
    
    def _generate_table_of_contents(self, content: str) -> str:
        """Generate table of contents from section headings."""
        # Extract all headings
        headings = re.findall(r'^(#{1,3})\s+(.+)$', content, re.MULTILINE)
        
        if not headings:
            return content
        
        # Build TOC
        toc_lines = ["# Table of Contents\n"]
        
        for level, title in headings:
            indent = "  " * (len(level) - 1)
            # Create anchor link
            anchor = title.lower().replace(" ", "-").replace(".", "")
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
        
        toc = "\n".join(toc_lines) + "\n\n---\n\n"
        
        # Insert TOC after title
        lines = content.split('\n')
        if lines and lines[0].startswith('#'):
            # Insert after first heading
            return '\n'.join(lines[:1]) + '\n\n' + toc + '\n'.join(lines[1:])
        else:
            return toc + content
    
    def _update_cross_references(self, content: str) -> str:
        """
        Update all cross-references to use correct numbers.
        
        Replaces generic references like "Figure X" with actual figure numbers
        based on placement order.
        """
        # Track element numbers
        figure_map = {}
        table_map = {}
        
        # Find all figure/table definitions and assign numbers
        figure_pattern = r'\*\*Figure (\d+):'
        table_pattern = r'\*\*Table (\d+):'
        
        for match in re.finditer(figure_pattern, content):
            figure_map[match.group(1)] = match.group(1)
        
        for match in re.finditer(table_pattern, content):
            table_map[match.group(1)] = match.group(1)
        
        # Replace references (would be more sophisticated in production)
        return content
    
    def export_document(
        self,
        content: str,
        output_path: str,
        format: str = "markdown"
    ):
        """
        Export assembled document to file.
        
        Args:
            content: Assembled document content
            output_path: Path to output file
            format: Output format (markdown, latex, docx, pdf)
        """
        if format == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        elif format == "latex":
            # Convert markdown to LaTeX
            latex_content = self._convert_to_latex(content)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
        
        elif format == "docx":
            # Would use python-docx to generate DOCX
            pass
        
        elif format == "pdf":
            # Would use LaTeX or reportlab to generate PDF
            pass
    
    def _convert_to_latex(self, markdown_content: str) -> str:
        """Convert markdown to LaTeX format."""
        # Basic conversion (would use pandoc or similar in production)
        latex = r"""\documentclass{article}
\usepackage{graphicx}
\usepackage{booktabs}

\begin{document}

"""
        # Convert headings
        content = re.sub(r'^# (.+)$', r'\\section{\1}', markdown_content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        
        latex += content
        latex += r"""

\end{document}
"""
        return latex


class ElementPlacementOptimizer:
    """
    Advanced optimizer for element placement using readability metrics
    and document flow analysis.
    """
    
    def __init__(self):
        """Initialize placement optimizer."""
        pass
    
    def optimize_placements(
        self,
        placements: List[PlacedElement],
        paragraphs: List[Dict[str, Any]]
    ) -> List[PlacedElement]:
        """
        Optimize element placements for better readability and flow.
        
        Considers:
        - Distance from reference
        - Paragraph length balance
        - Page break avoidance
        - Element clustering avoidance
        """
        optimized = []
        
        for placement in placements:
            # Calculate placement score
            score = self._calculate_placement_score(placement, paragraphs)
            
            # Find alternative placements if score is low
            if score < 0.5:
                alternative = self._find_better_placement(placement, paragraphs)
                optimized.append(alternative)
            else:
                optimized.append(placement)
        
        return optimized
    
    def _calculate_placement_score(
        self,
        placement: PlacedElement,
        paragraphs: List[Dict[str, Any]]
    ) -> float:
        """Calculate quality score for placement (0-1)."""
        score = 1.0
        
        # Penalize if far from reference
        if placement.cross_references:
            first_ref = placement.cross_references[0]
            distance = abs(placement.paragraph_index - first_ref.paragraph_index)
            score -= min(distance * 0.1, 0.3)
        
        # Penalize if disrupts short paragraphs
        if placement.paragraph_index < len(paragraphs):
            para = paragraphs[placement.paragraph_index]
            if para["word_count"] < 50:
                score -= 0.2
        
        return max(score, 0.0)
    
    def _find_better_placement(
        self,
        current: PlacedElement,
        paragraphs: List[Dict[str, Any]]
    ) -> PlacedElement:
        """Find better placement position."""
        # Would implement optimization algorithm
        return current
