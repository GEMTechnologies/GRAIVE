"""
Request Planning with Reasoning

This module implements deliberate planning with explicit reasoning
before execution. Instead of reactive pattern matching, the system
thinks through what needs to happen and why.

This is the CORRECT architecture for autonomous agents:
1. Understand the request deeply
2. Reason about what's needed
3. Plan the execution steps
4. Generate artifacts (plans, tasks, dependencies)
5. Execute with monitoring
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime


class RequestReasoner:
    """
    Reasons about user requests to create deliberate execution plans.
    
    Instead of: "User said 'essay' + 'image' → generate_document(include_images=True)"
    Does: "User wants essay about X with image → reason about:
           - What kind of image would enhance this topic?
           - Where should the image be placed for maximum impact?
           - Should I generate it or find it?
           - What should the image show specifically?"
    """
    
    def __init__(self, llm_caller=None):
        """
        Initialize request reasoner.
        
        Args:
            llm_caller: Function to call LLM for reasoning tasks
        """
        self.llm_caller = llm_caller
    
    def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """
        Deeply analyze user request with reasoning.
        
        This is NOT pattern matching. This is understanding intent,
        requirements, constraints, and success criteria.
        
        Args:
            user_request: Raw user input
        
        Returns:
            Analysis with reasoning traces
        """
        print(f"\n{'='*70}")
        print(f"🧠 REQUEST ANALYSIS & REASONING")
        print(f"{'='*70}\n")
        print(f"User Request: \"{user_request}\"\n")
        
        # STEP 1: Intent Classification with Reasoning
        print("[Step 1/5] 🎯 Understanding Intent...\n")
        intent = self._classify_intent_with_reasoning(user_request)
        
        print(f"Primary Intent: {intent['primary']}")
        print(f"Reasoning: {intent['reasoning']}\n")
        
        # STEP 2: Requirement Extraction with Analysis
        print("[Step 2/5] 📋 Extracting Requirements...\n")
        requirements = self._extract_requirements_with_reasoning(user_request, intent)
        
        for req_type, details in requirements.items():
            if details['detected']:
                print(f"✓ {req_type}: {details['value']}")
                print(f"  Reasoning: {details['reasoning']}")
        print()
        
        # STEP 3: Resource Planning with Justification
        print("[Step 3/5] 🛠️  Planning Resources...\n")
        resources = self._plan_resources_with_reasoning(user_request, requirements)
        
        for resource in resources:
            print(f"Resource: {resource['type']}")
            print(f"  Purpose: {resource['purpose']}")
            print(f"  Specification: {resource['specification']}")
            print(f"  Timing: {resource['timing']}")
            print(f"  Reasoning: {resource['reasoning']}\n")
        
        # STEP 4: Execution Strategy with Rationale
        print("[Step 4/5] 📝 Designing Execution Strategy...\n")
        strategy = self._design_execution_strategy(intent, requirements, resources)
        
        print(f"Strategy: {strategy['approach']}")
        print(f"Rationale: {strategy['rationale']}\n")
        
        print("Execution Steps:")
        for i, step in enumerate(strategy['steps'], 1):
            print(f"  {i}. {step['action']}")
            print(f"     Why: {step['reasoning']}")
            print(f"     Success Criteria: {step['success_criteria']}\n")
        
        # STEP 5: Risk Analysis
        print("[Step 5/5] ⚠️  Analyzing Risks...\n")
        risks = self._analyze_risks(strategy)
        
        for risk in risks:
            print(f"Risk: {risk['description']}")
            print(f"  Mitigation: {risk['mitigation']}\n")
        
        print(f"{'='*70}")
        print(f"✅ ANALYSIS COMPLETE")
        print(f"{'='*70}\n")
        
        return {
            'intent': intent,
            'requirements': requirements,
            'resources': resources,
            'strategy': strategy,
            'risks': risks,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _classify_intent_with_reasoning(self, request: str) -> Dict[str, Any]:
        """Classify intent with explicit reasoning."""
        request_lower = request.lower()
        
        # Document generation intent
        doc_keywords = ['essay', 'article', 'paper', 'document', 'thesis', 'write', 'create']
        doc_count = sum(1 for kw in doc_keywords if kw in request_lower)
        
        if doc_count >= 2:  # Strong signal
            return {
                'primary': 'document_generation',
                'confidence': 0.95,
                'reasoning': f"Request contains {doc_count} document-related keywords ({', '.join([kw for kw in doc_keywords if kw in request_lower])}), clearly indicating intent to create written content."
            }
        
        # Image generation intent
        image_keywords = ['image', 'picture', 'photo', 'flag', 'icon']
        image_count = sum(1 for kw in image_keywords if kw in request_lower)
        
        # But check if it's part of a document request
        if image_count > 0 and doc_count == 0:
            return {
                'primary': 'image_generation',
                'confidence': 0.90,
                'reasoning': f"Request mentions images ({image_count} keywords) without document context, indicating standalone image generation intent."
            }
        
        # Default to conversation
        return {
            'primary': 'conversation',
            'confidence': 0.70,
            'reasoning': "No clear task indicators found. Treating as general conversation or question."
        }
    
    def _extract_requirements_with_reasoning(
        self,
        request: str,
        intent: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Extract requirements with reasoning for each."""
        request_lower = request.lower()
        requirements = {}
        
        # Topic extraction
        topic_markers = ['about', 'of', 'on']
        topic = None
        reasoning = "No explicit topic marker found"
        
        for marker in topic_markers:
            if marker in request_lower:
                # Extract after marker
                import re
                pattern = f"{marker}\\s+([\\w\\s]+?)(?:\\s+(?:with|in|and|at)|$)"
                match = re.search(pattern, request_lower)
                if match:
                    topic = match.group(1).strip()
                    reasoning = f"Topic explicitly stated after '{marker}' marker"
                    break
        
        requirements['topic'] = {
            'detected': topic is not None,
            'value': topic,
            'reasoning': reasoning
        }
        
        # Word count
        import re
        word_match = re.search(r'(\\d+)\\s*words?', request_lower)
        if word_match:
            requirements['word_count'] = {
                'detected': True,
                'value': int(word_match.group(1)),
                'reasoning': "Explicit word count specified by user"
            }
        else:
            requirements['word_count'] = {
                'detected': False,
                'value': 1200,
                'reasoning': "No word count specified, using default 1200 words for standard essay"
            }
        
        # Images
        image_mentioned = 'image' in request_lower or 'picture' in request_lower
        requirements['images'] = {
            'detected': image_mentioned,
            'value': 1 if image_mentioned else 0,
            'reasoning': "User explicitly mentioned images in request" if image_mentioned else "No image requirement stated"
        }
        
        # Tables
        table_mentioned = 'table' in request_lower
        requirements['tables'] = {
            'detected': table_mentioned,
            'value': 1 if table_mentioned else 0,
            'reasoning': "User explicitly mentioned tables in request" if table_mentioned else "No table requirement stated"
        }
        
        return requirements
    
    def _plan_resources_with_reasoning(
        self,
        request: str,
        requirements: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Plan resources with reasoning for each."""
        resources = []
        
        # Document resource
        if requirements.get('topic', {}).get('detected'):
            resources.append({
                'type': 'document',
                'purpose': f"Main written content about {requirements['topic']['value']}",
                'specification': {
                    'format': 'markdown',
                    'word_count': requirements['word_count']['value'],
                    'sections': 'introduction, main content, conclusion'
                },
                'timing': 'generate first (foundation for other resources)',
                'reasoning': "Document is the primary deliverable and must be created before supplementary resources"
            })
        
        # Image resources
        if requirements.get('images', {}).get('detected'):
            topic = requirements.get('topic', {}).get('value', 'the topic')
            resources.append({
                'type': 'image',
                'purpose': f"Visual illustration related to {topic}",
                'specification': {
                    'subject': f"Relevant visual for {topic}",
                    'method': 'AI generation (DALL-E)',
                    'placement': 'within main content section for context'
                },
                'timing': 'generate before document assembly',
                'reasoning': f"Images enhance understanding of {topic} and should be contextually relevant, not decorative placeholders"
            })
        
        # Table resources
        if requirements.get('tables', {}).get('detected'):
            topic = requirements.get('topic', {}).get('value', 'the topic')
            resources.append({
                'type': 'table',
                'purpose': f"Structured data presentation for {topic}",
                'specification': {
                    'content': f"Relevant data about {topic}",
                    'rows': 5,
                    'columns': 3,
                    'format': 'markdown table'
                },
                'timing': 'generate during content creation',
                'reasoning': f"Tables should present factual data about {topic}, not generic placeholders"
            })
        
        return resources
    
    def _design_execution_strategy(
        self,
        intent: Dict[str, Any],
        requirements: Dict[str, Dict[str, Any]],
        resources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Design execution strategy with rationale."""
        
        if intent['primary'] == 'document_generation':
            return {
                'approach': 'multi-phase_document_generation',
                'rationale': "Document generation with media requires phased approach: plan → generate content → generate media → assemble → review",
                'steps': [
                    {
                        'action': 'Create detailed content plan',
                        'reasoning': "Planning prevents incoherent structure and ensures all requirements are addressed",
                        'success_criteria': "Plan includes section breakdown, word allocation, and media placement points"
                    },
                    {
                        'action': 'Generate text content section-by-section',
                        'reasoning': "Section-by-section generation allows quality control at granular level",
                        'success_criteria': "Each section meets quality threshold before proceeding"
                    },
                    {
                        'action': 'Generate required images with specific prompts',
                        'reasoning': f"Images must be contextually relevant to {requirements.get('topic', {}).get('value', 'the topic')}, not generic",
                        'success_criteria': "Images generated successfully and saved to workspace"
                    },
                    {
                        'action': 'Assemble complete document with media integration',
                        'reasoning': "Assembly phase combines all components with proper formatting and references",
                        'success_criteria': "Document contains all sections and media in logical positions"
                    },
                    {
                        'action': 'Quality review and validation',
                        'reasoning': "Final review ensures document meets user requirements and quality standards",
                        'success_criteria': "Document meets word count, includes all required elements, quality score > 8.0"
                    }
                ]
            }
        
        return {
            'approach': 'direct_execution',
            'rationale': "Simple request requires no multi-phase planning",
            'steps': []
        }
    
    def _analyze_risks(self, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze execution risks."""
        risks = []
        
        if 'multi-phase' in strategy['approach']:
            risks.append({
                'description': "Image generation API may fail or timeout",
                'likelihood': 'medium',
                'impact': 'medium',
                'mitigation': "Implement retry logic and fallback to placeholder with clear note"
            })
            
            risks.append({
                'description': "Generated content may not meet quality threshold",
                'likelihood': 'low',
                'impact': 'high',
                'mitigation': "Iterative revision with quality scoring system"
            })
            
            risks.append({
                'description': "User may not have required API keys configured",
                'likelihood': 'medium',
                'impact': 'high',
                'mitigation': "Check API key availability before execution, provide clear setup instructions if missing"
            })
        
        return risks
    
    def create_execution_plan_file(
        self,
        analysis: Dict[str, Any],
        workspace: Path
    ) -> str:
        """
        Create visible execution plan file that user can review.
        
        This is the CRITICAL missing piece - making planning visible!
        """
        plan_dir = workspace / "planning"
        plan_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_file = plan_dir / f"execution_plan_{timestamp}.md"
        
        # Generate markdown plan
        plan_content = self._generate_plan_markdown(analysis)
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        print(f"\n✅ EXECUTION PLAN CREATED")
        print(f"📄 File: {plan_file.name}")
        print(f"📍 Location: {plan_file}\n")
        
        return str(plan_file)
    
    def _generate_plan_markdown(self, analysis: Dict[str, Any]) -> str:
        """Generate markdown execution plan."""
        
        intent = analysis['intent']
        requirements = analysis['requirements']
        resources = analysis['resources']
        strategy = analysis['strategy']
        risks = analysis['risks']
        
        md = f"""# Execution Plan

**Created**: {analysis['analyzed_at']}
**Status**: Awaiting Approval

---

## Intent Analysis

**Primary Intent**: {intent['primary']}
**Confidence**: {intent['confidence']*100:.0f}%

**Reasoning**: {intent['reasoning']}

---

## Requirements

"""
        
        for req_name, req_details in requirements.items():
            if req_details['detected']:
                md += f"### {req_name.replace('_', ' ').title()}\n"
                md += f"- **Value**: {req_details['value']}\n"
                md += f"- **Reasoning**: {req_details['reasoning']}\n\n"
        
        md += "---\n\n## Planned Resources\n\n"
        
        for i, resource in enumerate(resources, 1):
            md += f"### Resource {i}: {resource['type'].title()}\n"
            md += f"- **Purpose**: {resource['purpose']}\n"
            md += f"- **Timing**: {resource['timing']}\n"
            md += f"- **Reasoning**: {resource['reasoning']}\n\n"
            md += "**Specification**:\n"
            for key, value in resource['specification'].items():
                md += f"- {key}: {value}\n"
            md += "\n"
        
        md += "---\n\n## Execution Strategy\n\n"
        md += f"**Approach**: {strategy['approach']}\n\n"
        md += f"**Rationale**: {strategy['rationale']}\n\n"
        md += "**Steps**:\n\n"
        
        for i, step in enumerate(strategy['steps'], 1):
            md += f"{i}. **{step['action']}**\n"
            md += f"   - Why: {step['reasoning']}\n"
            md += f"   - Success: {step['success_criteria']}\n\n"
        
        md += "---\n\n## Risk Analysis\n\n"
        
        for risk in risks:
            md += f"### {risk['description']}\n"
            md += f"- **Likelihood**: {risk['likelihood']}\n"
            md += f"- **Impact**: {risk['impact']}\n"
            md += f"- **Mitigation**: {risk['mitigation']}\n\n"
        
        md += """---

## Approval

To proceed with this plan:
- Type `approve` to execute as planned
- Type `modify` to adjust the plan
- Type `cancel` to abort

"""
        
        return md


def create_request_reasoner(llm_caller=None) -> RequestReasoner:
    """Factory function to create request reasoner."""
    return RequestReasoner(llm_caller)
