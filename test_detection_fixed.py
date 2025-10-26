#!/usr/bin/env python
"""Test the fixed detection priority"""

import re

def process_user_request(message: str):
    """Fixed detection with document generation FIRST"""
    message_lower = message.lower()
    
    # Layer 1: Questions/complaints
    question_indicators = ['is the', 'did you', 'have you', 'where is', 'why', 'how', 'what', 'when', 'who']
    complaint_indicators = ['but you', 'but u', 'you never', 'u never']
    
    is_question = any(indicator in message_lower for indicator in question_indicators)
    is_complaint = any(indicator in message_lower for indicator in complaint_indicators)
    
    if is_question or is_complaint:
        return {'action': 'chat', 'reason': 'question/complaint'}
    
    # Layer 2: DOCUMENT GENERATION FIRST (prioritize over image)
    write_keywords = ['write', 'generate', 'create', 'make me', 'essay', 'article', 'paper', 'document']
    is_write_request = any(keyword in message_lower for keyword in write_keywords)
    
    # Topic extraction
    topic = None
    if 'about' in message_lower:
        topic_match = re.search(r'about\s+([\w\s]+?)(?:\s+(?:in|with|well|and|at)|$)', message_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
    
    # Document type check
    has_document_type = any(dtype in message_lower for dtype in ['essay', 'article', 'paper', 'document', 'thesis'])
    
    # If document type AND topic, this is DEFINITELY document generation
    if is_write_request and topic and has_document_type:
        return {
            'action': 'generate_document',
            'topic': topic,
            'include_images': 'image' in message_lower,
            'include_tables': 'table' in message_lower
        }
    
    # Layer 3: Image generation (ONLY if NOT document)
    image_keywords = ['image', 'picture', 'photo', 'flag']
    is_image_only = any(keyword in message_lower for keyword in image_keywords)
    
    if is_image_only and not has_document_type:
        if any(verb in message_lower for verb in ['give', 'create', 'generate', 'show']):
            return {'action': 'generate_image'}
    
    return {'action': 'chat'}

# Test cases
tests = [
    ("make me an essay about wars in russia with atleast one image in the modle", "generate_document"),
    ("create an essay about africa and put an image inside", "generate_document"),
    ("write an article of japan with a table", "generate_document"),
    ("give me flag of japan", "generate_image"),
    ("create an image of a sunset", "generate_image"),
    ("where is the document", "chat"),
    ("u r lying", "chat"),
]

print("="*70)
print("FIXED DETECTION PRIORITY TESTS")
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
    
    if 'topic' in result:
        print(f"   Topic: {result.get('topic')}")
        print(f"   Images: {result.get('include_images')}")
    
    if actual_action == expected_action:
        passed += 1
    else:
        failed += 1

print(f"\n{'='*70}")
print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
print(f"{'='*70}")

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! Detection is now working correctly.")
    print("   'make me an essay with an image' → generate_document ✅")
    print("   'give me flag of japan' → generate_image ✅")
else:
    print(f"\n⚠️  {failed} tests failed.")
