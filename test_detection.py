#!/usr/bin/env python
"""Test detection for 'write an essay of japan with an image and a table inside'"""

import re

def process_user_request(message: str):
    """Test version"""
    message_lower = message.lower()
    
    # Detect document generation requests
    write_keywords = ['write', 'generate', 'create', 'make me', 'essay', 'article', 'paper', 'document', 'thesis']
    is_write_request = any(keyword in message_lower for keyword in write_keywords)
    
    # Extract word count
    word_count_match = re.search(r'(\d+)\s*words?', message_lower)
    target_words = int(word_count_match.group(1)) if word_count_match else 1200
    
    # Detect topic - ENHANCED
    topic = None
    if 'about' in message_lower:
        topic_match = re.search(r'about\s+([\w\s]+?)(?:\s+(?:in|with|well|and)|$)', message_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
    elif 'of' in message_lower:
        topic_match = re.search(r'(?:essay|article|paper|document|thesis)\s+of\s+([\w\s]+?)(?:\s+(?:with|in|and)|$)', message_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
    elif 'on' in message_lower:
        topic_match = re.search(r'(?:essay|article|paper|document|thesis)\s+on\s+([\w\s]+?)(?:\s+(?:with|in|and)|$)', message_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
    
    print(f"is_write_request: {is_write_request}")
    print(f"topic: {topic}")
    print(f"word_count: {target_words}")
    print(f"include_images: {'image' in message_lower}")
    print(f"include_tables: {'table' in message_lower}")
    
    if is_write_request and topic:
        return {
            'action': 'generate_document',
            'topic': topic,
            'word_count': target_words,
            'include_images': 'image' in message_lower,
            'include_tables': 'table' in message_lower
        }
    return {'action': 'chat'}

# Test
print("Test: 'write an essay of japan with an image and a table inside'")
result = process_user_request("write an essay of japan with an image and a table inside")
print(f"\nResult: {result}")
