th#!/usr/bin/env python
"""Test detection priority fix"""

import re

def process_user_request(message: str):
    """Test version with priority detection"""
    message_lower = message.lower()
    
    # Layer 1: Questions and complaints FIRST
    question_indicators = ['is the', 'did you', 'have you', 'where is', 'why', 'how', 'what', 'when', 'who']
    complaint_indicators = ['but you', 'but u', 'you never', 'u never', 'you didn\'t', 'u didn\'t']
    
    is_question = any(indicator in message_lower for indicator in question_indicators)
    is_complaint = any(indicator in message_lower for indicator in complaint_indicators)
    
    if is_question or is_complaint:
        return {'action': 'general_interaction', 'reason': 'question/complaint'}
    
    # Layer 2: Document generation with enhanced verification
    write_keywords = ['write', 'generate', 'create', 'make me', 'essay', 'article', 'paper']
    is_write_request = any(keyword in message_lower for keyword in write_keywords)
    
    # Topic extraction
    topic = None
    if 'about' in message_lower:
        topic_match = re.search(r'about\s+([\w\s]+?)(?:\s+(?:in|with|well|and)|$)', message_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
    
    # Enhanced verification
    has_creation_verb = any(verb in message_lower for verb in ['create', 'write', 'generate', 'make'])
    has_document_type = any(dtype in message_lower for dtype in ['essay', 'article', 'paper', 'document'])
    
    if is_write_request and topic and has_creation_verb and has_document_type:
        return {
            'action': 'generate_document',
            'topic': topic,
            'include_images': 'image' in message_lower,
            'include_tables': 'table' in message_lower
        }
    
    # Layer 3: Image generation
    image_keywords = ['image', 'picture', 'photo', 'flag']
    is_image_request = any(keyword in message_lower for keyword in image_keywords)
    
    if is_image_request and any(verb in message_lower for verb in ['give', 'create', 'generate', 'make']):
        return {'action': 'generate_image'}
    
    return {'action': 'general_interaction', 'reason': 'default'}

# Test cases from user's actual conversation
tests = [
    ("create an essay about africa and put an image inside", "generate_document"),
    ("but u never created the image", "general_interaction"),
    ("is the image inserted into the article or not", "general_interaction"),
    ("write an essay of japan with an image", "generate_document"),
    ("give me flag of japan", "generate_image"),
    ("did you create the file", "general_interaction"),
    ("where is my document", "general_interaction"),
]

print("="*70)
print("DETECTION PRIORITY TESTS")
print("="*70)

passed = 0
failed = 0

for message, expected_action in tests:
    result = process_user_request(message)
    actual_action = result['action']
    
    status = "✅" if actual_action == expected_action else "❌"
    
    print(f"\n{status} Input: \"{message}\"")
    print(f"   Expected: {expected_action}")
    print(f"   Got: {actual_action}")
    
    if 'reason' in result:
        print(f"   Reason: {result['reason']}")
    if 'topic' in result:
        print(f"   Topic: {result.get('topic')}")
        print(f"   Images: {result.get('include_images')}")
        print(f"   Tables: {result.get('include_tables')}")
    
    if actual_action == expected_action:
        passed += 1
    else:
        failed += 1

print(f"\n{'='*70}")
print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
print(f"{'='*70}")

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! Detection priority is working correctly.")
else:
    print(f"\n⚠️  {failed} tests failed. Review detection logic.")
