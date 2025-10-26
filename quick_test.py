#!/usr/bin/env python
"""
Simple Quick Test - Tests just the request routing without full system init
"""

import re
from typing import Dict, Any

def process_user_request(message: str) -> Dict[str, Any]:
    """Test version of process_user_request"""
    message_lower = message.lower()
    
    # Detect CODE GENERATION requests
    code_keywords = ['code', 'program', 'script', 'game', 'app']
    is_code_request = any(keyword in message_lower for keyword in code_keywords)
    
    if is_code_request and any(verb in message_lower for verb in ['code', 'write', 'create', 'make']):
        language = 'python'
        if 'javascript' in message_lower:
            language = 'javascript'
        
        description = message_lower
        for remove in ['code me', 'write', 'create', 'make me', 'a', 'the']:
            description = description.replace(remove, '')
        description = description.strip()
        
        return {
            'action': 'generate_code',
            'description': description,
            'language': language
        }
    
    # Detect DATA ANALYSIS requests
    analysis_keywords = ['analyze', 'analysis', 'data']
    if any(keyword in message_lower for keyword in analysis_keywords):
        return {
            'action': 'analyze_data',
            'description': message
        }
    
    # Detect PPT generation
    ppt_keywords = ['ppt', 'powerpoint', 'presentation']
    if any(keyword in message_lower for keyword in ppt_keywords):
        return {
            'action': 'create_presentation',
            'topic': message
        }
    
    # Detect image insertion
    if 'insert' in message_lower and 'image' in message_lower:
        title_match = re.search(r'titled?\s+[\"\']?([^\"\'\n]+)[\"\']?', message_lower)
        title = title_match.group(1).strip() if title_match else 'untitled'
        
        return {
            'action': 'insert_image_in_document',
            'title': title
        }
    
    # Detect image generation
    if 'image' in message_lower or 'flag' in message_lower:
        return {
            'action': 'generate_image',
            'description': message
        }
    
    # Detect document generation
    if any(word in message_lower for word in ['write', 'essay', 'article']):
        return {
            'action': 'generate_document',
            'topic': message
        }
    
    return {'action': 'chat', 'message': message}

def test_all():
    """Run all tests"""
    print("\n" + "="*70)
    print("GRAIVE AI - QUICK ROUTING TESTS")
    print("="*70)
    
    tests = [
        ("code me a python snake game", "generate_code", "python"),
        ("insert that image in an article titled the african boy", "insert_image_in_document", "the african boy"),
        ("analyze this dataset", "analyze_data", None),
        ("create a powerpoint about climate", "create_presentation", None),
        ("give me flag of japan", "generate_image", None),
        ("write an essay about AI", "generate_document", None),
        ("hello how are you", "chat", None),
    ]
    
    passed = 0
    failed = 0
    
    for message, expected_action, expected_value in tests:
        print(f"\n{'─'*70}")
        print(f"Input: \"{message}\"")
        
        result = process_user_request(message)
        
        print(f"Action: {result['action']}")
        
        if result['action'] == expected_action:
            print(f"✅ PASS")
            passed += 1
        else:
            print(f"❌ FAIL - Expected: {expected_action}, Got: {result['action']}")
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"RESULTS: {passed} passed, {failed} failed")
    print(f"{'='*70}\n")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = test_all()
    sys.exit(0 if success else 1)
