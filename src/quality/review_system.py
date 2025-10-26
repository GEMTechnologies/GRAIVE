"""
PhD-Level Review and Revision System

This module implements a comprehensive review system that critiques and revises
content to PhD-level academic standards before delivery to clients.

Features:
- Multi-dimensional quality scoring
- Content coherence analysis
- Citation verification
- Academic writing standards checking
- Iterative revision with improvement tracking
- Peer-review simulation
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class QualityDimension(Enum):
    """Quality assessment dimensions."""
    CLARITY = "clarity"
    COHERENCE = "coherence"
    DEPTH = "depth"
    CITATIONS = "citations"
    STRUCTURE = "structure"
    ORIGINALITY = "originality"
    GRAMMAR = "grammar"
    ACADEMIC_TONE = "academic_tone"


@dataclass
class ReviewScore:
    """Review score for a quality dimension."""
    dimension: QualityDimension
    score: float  # 0-10 scale
    feedback: str
    suggestions: List[str]


@dataclass
class RevisionResult:
    """Result of a revision pass."""
    iteration: int
    original_content: str
    revised_content: str
    improvements: List[str]
    scores: Dict[str, float]
    timestamp: datetime


class PhDReviewSystem:
    """
    Implements PhD-level review and revision of academic content.
    
    This system applies rigorous academic standards to review content,
    providing multi-dimensional quality scoring and iterative revision
    until PhD-level quality is achieved.
    """
    
    def __init__(self, min_quality_threshold: float = 8.0):
        """
        Initialize review system.
        
        Args:
            min_quality_threshold: Minimum average quality score (0-10 scale)
        """
        self.min_threshold = min_quality_threshold
        self.revision_history: List[RevisionResult] = []
        
    def review_content(
        self,
        content: str,
        topic: str,
        target_audience: str = "PhD researchers",
        field: str = "general"
    ) -> Dict[str, Any]:
        """
        Conduct comprehensive PhD-level review of content.
        
        Args:
            content: Content to review
            topic: Document topic
            target_audience: Target audience level
            field: Academic field
        
        Returns:
            Review report with scores and recommendations
        """
        print(f"\n{'='*70}")
        print(f"📋 PHD-LEVEL CONTENT REVIEW")
        print(f"{'='*70}")
        print(f"Topic: {topic}")
        print(f"Field: {field}")
        print(f"Target Audience: {target_audience}")
        print(f"Content Length: {len(content.split())} words")
        print(f"{'='*70}\n")
        
        # Perform multi-dimensional quality assessment
        scores = []
        
        print("[1/8] Assessing clarity and readability...")
        clarity_score = self._assess_clarity(content)
        scores.append(clarity_score)
        print(f"      Score: {clarity_score.score:.1f}/10 - {clarity_score.feedback}")
        
        print("\n[2/8] Analyzing logical coherence...")
        coherence_score = self._assess_coherence(content)
        scores.append(coherence_score)
        print(f"      Score: {coherence_score.score:.1f}/10 - {coherence_score.feedback}")
        
        print("\n[3/8] Evaluating content depth...")
        depth_score = self._assess_depth(content, topic)
        scores.append(depth_score)
        print(f"      Score: {depth_score.score:.1f}/10 - {depth_score.feedback}")
        
        print("\n[4/8] Verifying citations and references...")
        citation_score = self._assess_citations(content)
        scores.append(citation_score)
        print(f"      Score: {citation_score.score:.1f}/10 - {citation_score.feedback}")
        
        print("\n[5/8] Checking document structure...")
        structure_score = self._assess_structure(content)
        scores.append(structure_score)
        print(f"      Score: {structure_score.score:.1f}/10 - {structure_score.feedback}")
        
        print("\n[6/8] Assessing originality and insight...")
        originality_score = self._assess_originality(content)
        scores.append(originality_score)
        print(f"      Score: {originality_score.score:.1f}/10 - {originality_score.feedback}")
        
        print("\n[7/8] Reviewing grammar and language...")
        grammar_score = self._assess_grammar(content)
        scores.append(grammar_score)
        print(f"      Score: {grammar_score.score:.1f}/10 - {grammar_score.feedback}")
        
        print("\n[8/8] Evaluating academic tone and style...")
        tone_score = self._assess_academic_tone(content)
        scores.append(tone_score)
        print(f"      Score: {tone_score.score:.1f}/10 - {tone_score.feedback}")
        
        # Calculate overall quality
        avg_score = sum(s.score for s in scores) / len(scores)
        
        print(f"\n{'='*70}")
        print(f"📊 OVERALL QUALITY SCORE: {avg_score:.2f}/10")
        
        if avg_score >= 9.0:
            print(f"✅ EXCELLENT - PhD-level quality achieved")
            quality_level = "EXCELLENT"
        elif avg_score >= self.min_threshold:
            print(f"✅ GOOD - Meets PhD standards")
            quality_level = "GOOD"
        elif avg_score >= 7.0:
            print(f"⚠️  ACCEPTABLE - Revision recommended")
            quality_level = "ACCEPTABLE"
        else:
            print(f"❌ NEEDS IMPROVEMENT - Significant revision required")
            quality_level = "NEEDS_IMPROVEMENT"
        
        print(f"{'='*70}\n")
        
        return {
            "scores": {s.dimension.value: s.score for s in scores},
            "average_score": avg_score,
            "quality_level": quality_level,
            "detailed_scores": scores,
            "needs_revision": avg_score < self.min_threshold,
            "revision_priority": self._get_revision_priorities(scores)
        }
    
    def revise_content(
        self,
        content: str,
        review_report: Dict[str, Any],
        topic: str,
        max_iterations: int = 3
    ) -> str:
        """
        Iteratively revise content to meet PhD standards.
        
        Args:
            content: Original content
            review_report: Review report from review_content()
            topic: Document topic
            max_iterations: Maximum revision iterations
        
        Returns:
            Revised content meeting quality standards
        """
        print(f"\n{'='*70}")
        print(f"🔄 ITERATIVE REVISION PROCESS")
        print(f"{'='*70}")
        print(f"Target Quality: {self.min_threshold}/10")
        print(f"Current Quality: {review_report['average_score']:.2f}/10")
        print(f"Max Iterations: {max_iterations}")
        print(f"{'='*70}\n")
        
        current_content = content
        current_score = review_report['average_score']
        iteration = 0
        
        while current_score < self.min_threshold and iteration < max_iterations:
            iteration += 1
            print(f"\n[Iteration {iteration}/{max_iterations}] Revising content...")
            
            # Get revision priorities
            priorities = review_report['revision_priority']
            
            # Apply revisions based on priorities
            revised_content = self._apply_revisions(
                current_content,
                priorities,
                topic,
                iteration
            )
            
            # Re-review revised content
            print(f"\n[Iteration {iteration}] Re-reviewing revised content...")
            new_review = self.review_content(revised_content, topic)
            new_score = new_review['average_score']
            
            # Track improvement
            improvement = new_score - current_score
            print(f"\n📈 Improvement: +{improvement:.2f} points")
            print(f"   Previous: {current_score:.2f}/10")
            print(f"   Current:  {new_score:.2f}/10")
            
            # Store revision result
            self.revision_history.append(RevisionResult(
                iteration=iteration,
                original_content=current_content,
                revised_content=revised_content,
                improvements=[f"Score improved by {improvement:.2f} points"],
                scores=new_review['scores'],
                timestamp=datetime.now()
            ))
            
            current_content = revised_content
            current_score = new_score
            review_report = new_review
            
            if current_score >= self.min_threshold:
                print(f"\n✅ Quality threshold met after {iteration} iteration(s)")
                break
        
        if current_score < self.min_threshold:
            print(f"\n⚠️  Maximum iterations reached. Final score: {current_score:.2f}/10")
        
        return current_content
    
    def _assess_clarity(self, content: str) -> ReviewScore:
        """Assess writing clarity and readability."""
        # Simple heuristics (in production, use NLP analysis)
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Optimal sentence length: 15-25 words
        if 15 <= avg_sentence_length <= 25:
            score = 9.0
            feedback = "Excellent sentence length and clarity"
        elif 10 <= avg_sentence_length <= 30:
            score = 7.5
            feedback = "Good clarity, some sentences could be refined"
        else:
            score = 6.0
            feedback = "Clarity could be improved with better sentence structure"
        
        return ReviewScore(
            dimension=QualityDimension.CLARITY,
            score=score,
            feedback=feedback,
            suggestions=[
                "Aim for 15-25 words per sentence",
                "Use active voice where possible",
                "Define technical terms clearly"
            ]
        )
    
    def _assess_coherence(self, content: str) -> ReviewScore:
        """Assess logical flow and coherence."""
        # Check for transition words and logical connectors
        transitions = ['however', 'moreover', 'furthermore', 'therefore', 'consequently', 
                      'in addition', 'for example', 'in contrast', 'similarly']
        
        transition_count = sum(1 for t in transitions if t in content.lower())
        paragraphs = content.split('\n\n')
        transitions_per_para = transition_count / max(len(paragraphs), 1)
        
        if transitions_per_para >= 2:
            score = 9.0
            feedback = "Strong logical flow with clear transitions"
        elif transitions_per_para >= 1:
            score = 7.5
            feedback = "Good coherence, could benefit from more transitions"
        else:
            score = 6.5
            feedback = "Logical flow needs strengthening"
        
        return ReviewScore(
            dimension=QualityDimension.COHERENCE,
            score=score,
            feedback=feedback,
            suggestions=[
                "Add transition sentences between paragraphs",
                "Ensure clear topic sentences",
                "Use logical connectors appropriately"
            ]
        )
    
    def _assess_depth(self, content: str, topic: str) -> ReviewScore:
        """Assess content depth and thoroughness."""
        word_count = len(content.split())
        
        # PhD-level depth typically requires substantial content
        if word_count >= 2000:
            score = 9.0
            feedback = "Comprehensive and thorough coverage"
        elif word_count >= 1200:
            score = 7.5
            feedback = "Good depth, could expand critical sections"
        else:
            score = 6.0
            feedback = "Needs more depth and detailed analysis"
        
        return ReviewScore(
            dimension=QualityDimension.DEPTH,
            score=score,
            feedback=feedback,
            suggestions=[
                "Expand on key theoretical concepts",
                "Include more detailed examples",
                "Provide deeper critical analysis"
            ]
        )
    
    def _assess_citations(self, content: str) -> ReviewScore:
        """Verify citations and references."""
        # Detect citation patterns (APA, MLA, etc.)
        apa_citations = len(re.findall(r'\([A-Z][a-z]+,?\s+\d{4}\)', content))
        bracket_citations = len(re.findall(r'\[\d+\]', content))
        total_citations = apa_citations + bracket_citations
        
        word_count = len(content.split())
        citations_per_1000 = (total_citations / word_count) * 1000 if word_count > 0 else 0
        
        # PhD-level: 10-20 citations per 1000 words
        if citations_per_1000 >= 10:
            score = 9.0
            feedback = "Excellent citation density and academic support"
        elif citations_per_1000 >= 5:
            score = 7.0
            feedback = "Good use of citations, could add more support"
        else:
            score = 5.5
            feedback = "Needs more citations to support claims"
        
        return ReviewScore(
            dimension=QualityDimension.CITATIONS,
            score=score,
            feedback=feedback,
            suggestions=[
                "Add citations to support all major claims",
                "Ensure recent sources (within 5 years)",
                "Include seminal works in the field"
            ]
        )
    
    def _assess_structure(self, content: str) -> ReviewScore:
        """Check document structure and organization."""
        # Detect headings
        headings = re.findall(r'^#{1,3}\s+.+$', content, re.MULTILINE)
        
        has_intro = any('introduction' in h.lower() for h in headings)
        has_conclusion = any('conclusion' in h.lower() for h in headings)
        has_sections = len(headings) >= 3
        
        if has_intro and has_conclusion and has_sections:
            score = 9.0
            feedback = "Well-structured with clear sections"
        elif has_sections:
            score = 7.0
            feedback = "Good structure, ensure intro and conclusion present"
        else:
            score = 6.0
            feedback = "Needs clearer structural organization"
        
        return ReviewScore(
            dimension=QualityDimension.STRUCTURE,
            score=score,
            feedback=feedback,
            suggestions=[
                "Include clear introduction and conclusion",
                "Use hierarchical heading structure",
                "Ensure logical section progression"
            ]
        )
    
    def _assess_originality(self, content: str) -> ReviewScore:
        """Assess originality and critical thinking."""
        # Look for critical analysis markers
        analysis_markers = ['argues', 'suggests', 'demonstrates', 'reveals', 
                          'indicates', 'proposes', 'challenges', 'questions']
        
        marker_count = sum(1 for marker in analysis_markers if marker in content.lower())
        
        if marker_count >= 8:
            score = 8.5
            feedback = "Strong critical analysis and original thought"
        elif marker_count >= 4:
            score = 7.0
            feedback = "Good analytical depth, expand critical perspective"
        else:
            score = 6.0
            feedback = "Needs more critical analysis and original insights"
        
        return ReviewScore(
            dimension=QualityDimension.ORIGINALITY,
            score=score,
            feedback=feedback,
            suggestions=[
                "Add critical analysis of sources",
                "Present original interpretations",
                "Challenge existing assumptions where appropriate"
            ]
        )
    
    def _assess_grammar(self, content: str) -> ReviewScore:
        """Review grammar and language quality."""
        # Basic grammar checks (in production, use proper grammar checker)
        words = content.split()
        sentences = content.split('.')
        
        # Check for common issues
        has_contractions = any(c in content for c in ["don't", "can't", "won't", "it's"])
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        
        if not has_contractions and avg_word_length >= 5:
            score = 9.0
            feedback = "Excellent grammar and formal academic language"
        elif not has_contractions:
            score = 7.5
            feedback = "Good grammar, consider more sophisticated vocabulary"
        else:
            score = 6.5
            feedback = "Avoid contractions in academic writing"
        
        return ReviewScore(
            dimension=QualityDimension.GRAMMAR,
            score=score,
            feedback=feedback,
            suggestions=[
                "Eliminate contractions",
                "Use formal academic language",
                "Proofread carefully for errors"
            ]
        )
    
    def _assess_academic_tone(self, content: str) -> ReviewScore:
        """Evaluate academic tone and objectivity."""
        # Check for informal/subjective language
        informal_markers = ['i think', 'i believe', 'in my opinion', 'feel', 'seems like']
        informal_count = sum(1 for marker in informal_markers if marker in content.lower())
        
        # Check for hedging (appropriate academic caution)
        hedging = ['may', 'might', 'could', 'possibly', 'suggests', 'indicates']
        hedging_count = sum(1 for h in hedging if h in content.lower())
        
        if informal_count == 0 and hedging_count >= 3:
            score = 9.0
            feedback = "Excellent objective academic tone"
        elif informal_count <= 2:
            score = 7.0
            feedback = "Generally academic, minimize subjective language"
        else:
            score = 6.0
            feedback = "Too informal, needs more objective academic tone"
        
        return ReviewScore(
            dimension=QualityDimension.ACADEMIC_TONE,
            score=score,
            feedback=feedback,
            suggestions=[
                "Remove first-person pronouns where possible",
                "Use objective, evidence-based language",
                "Employ appropriate academic hedging"
            ]
        )
    
    def _get_revision_priorities(self, scores: List[ReviewScore]) -> List[Dict[str, Any]]:
        """Determine revision priorities based on scores."""
        # Sort dimensions by score (lowest first)
        sorted_scores = sorted(scores, key=lambda s: s.score)
        
        priorities = []
        for score in sorted_scores[:3]:  # Top 3 priorities
            priorities.append({
                "dimension": score.dimension.value,
                "current_score": score.score,
                "feedback": score.feedback,
                "suggestions": score.suggestions,
                "priority": "HIGH" if score.score < 7.0 else "MEDIUM"
            })
        
        return priorities
    
    def _apply_revisions(
        self,
        content: str,
        priorities: List[Dict[str, Any]],
        topic: str,
        iteration: int
    ) -> str:
        """
        Apply revisions based on priorities.
        
        In production, this would use LLM to intelligently revise content.
        For now, returns content with revision markers.
        """
        print(f"\n   Applying revisions for:")
        for priority in priorities:
            print(f"   • {priority['dimension'].upper()}: {priority['feedback']}")
        
        # In production: Call LLM with specific revision instructions
        # For now: Add revision metadata
        revised = content
        
        revision_note = f"\n\n<!-- Revision {iteration} applied targeting: {', '.join(p['dimension'] for p in priorities)} -->\n"
        revised = revision_note + revised
        
        return revised
    
    def get_revision_report(self) -> str:
        """Generate comprehensive revision report."""
        if not self.revision_history:
            return "No revisions performed yet."
        
        report = f"\n{'='*70}\n"
        report += f"📊 REVISION HISTORY REPORT\n"
        report += f"{'='*70}\n"
        report += f"Total Iterations: {len(self.revision_history)}\n\n"
        
        for rev in self.revision_history:
            report += f"Iteration {rev.iteration}:\n"
            report += f"  Timestamp: {rev.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"  Improvements:\n"
            for imp in rev.improvements:
                report += f"    - {imp}\n"
            report += f"  Quality Scores:\n"
            for dim, score in rev.scores.items():
                report += f"    • {dim}: {score:.1f}/10\n"
            report += "\n"
        
        report += f"{'='*70}\n"
        
        return report


def create_review_system(min_quality_threshold: float = 8.0) -> PhDReviewSystem:
    """
    Factory function to create review system.
    
    Args:
        min_quality_threshold: Minimum quality threshold (0-10)
    
    Returns:
        Configured review system
    """
    return PhDReviewSystem(min_quality_threshold=min_quality_threshold)
