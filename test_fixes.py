#!/usr/bin/env python
"""
Quick Test Script for Graive AI Fixes
Tests all the new autonomous execution capabilities
"""

import sys
from pathlib import Path

# Add GRAIVE to path
sys.path.insert(0, str(Path(__file__).parent))

from graive import GraiveAI

def test_code_generation():
    """Test autonomous code generation"""
    print("\n" + "="*70)
    print("TEST 1: CODE GENERATION")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for code
    request = graive.process_user_request("code me a python snake game")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Description: {request.get('description', 'N/A')}")
    print(f"Language: {request.get('language', 'N/A')}")
    
    assert request['action'] == 'generate_code', "Should detect code generation"
    assert request['language'] == 'python', "Should detect Python language"
    
    print("\n✅ Code generation detection PASSED")
    return True

def test_image_insertion():
    """Test image insertion detection"""
    print("\n" + "="*70)
    print("TEST 2: IMAGE INSERTION")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for image insertion
    request = graive.process_user_request("insert that image in an article titled the african boy")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Title: {request.get('title', 'N/A')}")
    print(f"Image Desc: {request.get('image_description', 'N/A')}")
    
    assert request['action'] == 'insert_image_in_document', "Should detect image insertion"
    assert 'african boy' in request.get('title', '').lower(), "Should extract title"
    
    print("\n✅ Image insertion detection PASSED")
    return True

def test_data_analysis():
    """Test data analysis detection"""
    print("\n" + "="*70)
    print("TEST 3: DATA ANALYSIS")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for data analysis
    request = graive.process_user_request("analyze this dataset for me")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Description: {request.get('description', 'N/A')}")
    
    assert request['action'] == 'analyze_data', "Should detect data analysis"
    
    print("\n✅ Data analysis detection PASSED")
    return True

def test_ppt_generation():
    """Test PPT generation detection"""
    print("\n" + "="*70)
    print("TEST 4: PPT GENERATION")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for PPT
    request = graive.process_user_request("create a powerpoint presentation about climate change")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Topic: {request.get('topic', 'N/A')}")
    
    assert request['action'] == 'create_presentation', "Should detect PPT generation"
    
    print("\n✅ PPT generation detection PASSED")
    return True

def test_image_generation():
    """Test image generation detection"""
    print("\n" + "="*70)
    print("TEST 5: IMAGE GENERATION")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for image
    request = graive.process_user_request("give me flag of japan image now")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Description: {request.get('description', 'N/A')}")
    
    assert request['action'] == 'generate_image', "Should detect image generation"
    assert 'japan' in request.get('description', '').lower(), "Should detect Japan flag"
    
    print("\n✅ Image generation detection PASSED")
    return True

def test_document_generation():
    """Test document generation detection"""
    print("\n" + "="*70)
    print("TEST 6: DOCUMENT GENERATION")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate user request for document
    request = graive.process_user_request("write an essay about AI in 1000 words")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Topic: {request.get('topic', 'N/A')}")
    print(f"Word Count: {request.get('word_count', 'N/A')}")
    
    assert request['action'] == 'generate_document', "Should detect document generation"
    assert request['word_count'] == 1000, "Should extract word count"
    
    print("\n✅ Document generation detection PASSED")
    return True

def test_chat_fallback():
    """Test that chat still works for non-task requests"""
    print("\n" + "="*70)
    print("TEST 7: CHAT FALLBACK")
    print("="*70)
    
    graive = GraiveAI(workspace="./test_workspace")
    
    # Simulate regular conversation
    request = graive.process_user_request("hello, how are you?")
    
    print(f"\nDetected Action: {request['action']}")
    print(f"Message: {request.get('message', 'N/A')}")
    
    assert request['action'] == 'chat', "Should fallback to chat"
    
    print("\n✅ Chat fallback PASSED")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("GRAIVE AI - AUTONOMOUS EXECUTION TESTS")
    print("="*70)
    print("\nTesting all new detection and routing capabilities...")
    
    tests = [
        ("Code Generation", test_code_generation),
        ("Image Insertion", test_image_insertion),
        ("Data Analysis", test_data_analysis),
        ("PPT Generation", test_ppt_generation),
        ("Image Generation", test_image_generation),
        ("Document Generation", test_document_generation),
        ("Chat Fallback", test_chat_fallback),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            failed += 1
    
    # Final summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"\n✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")
    print("\n" + "="*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for autonomous execution.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
