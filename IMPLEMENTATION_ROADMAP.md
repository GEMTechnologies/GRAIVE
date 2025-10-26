# Graive AI - Implementation Roadmap for Remaining Features

## Current Status

The system now has comprehensive capabilities including PhD-level document generation, image generation with multiple methods, conversation memory, and progress tracking. However, several requested features require additional implementation.

## Features Requiring Implementation

### 1. Image Insertion into Documents ⚠️ CRITICAL

**Current Issue:** When user says "insert that image into an article titled X", the system chats about doing it instead of executing it.

**Required Implementation:**
```python
def insert_image_in_document(self, title: str, image_path: str = None) -> Dict[str, Any]:
    """
    Create or update document to include specified image.
    
    Args:
        title: Document title
        image_path: Path to image (if None, use last_generated_image)
    
    Returns:
        Dict with document path and status
    """
    # 1. Find or create document
    # 2. Determine best insertion point (after introduction, relevant section)
    # 3. Insert image with proper markdown/HTML syntax
    # 4. Add caption with description
    # 5. Save updated document
    # 6. Show user the result with progress tracking
```

**Integration Point:** `interactive_mode()` should handle `'insert_image_in_document'` action:
```python
elif request['action'] == 'insert_image_in_document':
    print(f"\nManus AI: I'll create an article titled '{request['title']}' with the image.")
    result = self.insert_image_in_document(
        title=request['title'],
        image_path=self.last_generated_image
    )
```

### 2. Multi-Model Image Generation Based on Complexity

**Current:** Always uses same method (DALL-E or programmatic)

**Required:** Intelligent routing based on complexity analysis

```python
def _analyze_image_complexity(self, description: str) -> str:
    """
    Analyze description complexity to choose best model.
    
    Simple (flags, logos) → Programmatic
    Medium (photos, portraits) → Web download or Banana
    Complex (creative, artistic) → DALL-E 3 or Gemini Imagen
    
    Returns:
        Recommended method: 'programmatic', 'web', 'banana', 'dalle', 'gemini'
    """
    complexity_indicators = {
        'simple': ['flag', 'logo', 'icon', 'chart', 'graph'],
        'medium': ['photo', 'portrait', 'landscape', 'building'],
        'complex': ['artistic', 'creative', 'surreal', 'fantasy', 'abstract']
    }
    
    # Analyze and return appropriate method
```

**API Integration Needed:**
- Banana API for cost-effective medium complexity
- Google Gemini Imagen for alternative to DALL-E
- Fallback chain: DALL-E → Gemini → Banana → Programmatic

### 3. OCR Capability for Image Understanding

**Required:** Ability to read text from images and generate descriptions

```python
def analyze_image_with_ocr(self, image_path: str) -> Dict[str, Any]:
    """
    Extract text and generate description from image.
    
    Uses:
    - Tesseract OCR for text extraction
    - GPT-4 Vision or Gemini Vision for image description
    
    Returns:
        Dict with extracted_text, description, objects_detected
    """
    # 1. Run OCR (Tesseract or cloud OCR)
    # 2. Send to vision model for description
    # 3. Return comprehensive analysis
```

**Installation Required:**
```bash
pip install pytesseract pillow
# Also install Tesseract binary: https://github.com/tesseract-ocr/tesseract
```

**Usage:**
```
You: describe that image
Graive AI: [Runs OCR and vision analysis]
          The image shows: [detailed description]
          Text detected: [extracted text]
```

### 4. Web Scraping with Playwright/Selenium + Progress Tracking

**Current:** Browser automation exists but not fully integrated with progress tracking

**Required Implementation:**

```python
def scrape_web_with_progress(self, url: str, extract_type: str = "text") -> Dict[str, Any]:
    """
    Scrape web content with real-time progress reporting.
    
    Shows:
    - Browser launching
    - Page loading progress
    - Element extraction
    - Data collection status
    
    Returns:
        Scraped content with metadata
    """
    print(f"\n{'='*70}")
    print(f"🌐 WEB SCRAPING - {url}")
    print(f"{'='*70}\n")
    
    print("[Step 1/5] 🚀 Launching browser...")
    # Launch Playwright/Selenium
    
    print("[Step 2/5] 📡 Navigating to URL...")
    # Navigate with progress
    
    print("[Step 3/5] 🔍 Extracting content...")
    # Extract with element-by-element progress
    
    print("[Step 4/5] 📊 Processing data...")
    # Process and structure
    
    print("[Step 5/5] 💾 Saving results...")
    # Save to workspace
    
    print(f"\n✅ Scraping complete!")
```

**Integration with Playwright:**
```bash
pip install playwright
playwright install
```

**Progress Example:**
```
[Step 3/5] 🔍 Extracting content...
           ✓ Found 15 paragraphs
           ✓ Extracted 8 images  
           ✓ Collected 3 tables
           ✓ Identified 42 links
```

### 5. Real-Time Writing Progress Display

**Current:** Shows final word count only

**Required:** Stream content generation with live word count

```python
def generate_content_with_streaming(self, topic: str, word_count: int):
    """
    Generate content with streaming progress display.
    
    Shows:
    - Words generated: 0/1500 (updating in real-time)
    - Current section being written
    - Estimated completion time
    """
    print(f"[Generating] Words: 0/{word_count}")
    
    # Use streaming API
    for chunk in stream_from_llm(prompt):
        current_words += len(chunk.split())
        # Update progress bar
        print(f"\r[Generating] Words: {current_words}/{word_count}", end="", flush=True)
    
    print(f"\n✅ Generation complete: {current_words} words")
```

## Priority Implementation Order

### Phase 1: Critical Fixes (Immediate)
1. **Image Insertion into Documents** - Users expect this to work NOW
2. **Fix chat-instead-of-execute** - Route insert requests to actual execution

### Phase 2: Enhanced Capabilities (Next Sprint)
3. **Multi-model image generation** - Cost optimization and quality
4. **Streaming progress for writing** - Better user experience
5. **OCR for image understanding** - Enables image descriptions

### Phase 3: Advanced Features (Future)
6. **Web scraping with progress** - Research automation
7. **Playwright integration** - Modern web automation
8. **Vision API integration** - Advanced image analysis

## Code Snippets Ready to Integrate

### Image Insertion Handler (Add to interactive_mode)

```python
elif request['action'] == 'insert_image_in_document':
    print(f"\nManus AI: I'll create '{request['title']}' with your image.")
    print(f"           Generating article content...")
    
    # Generate article
    doc_result = self.generate_document(
        topic=request['title'],
        word_count=800,
        include_images=False,  # We'll add manually
        include_tables=False
    )
    
    if doc_result.get('success'):
        # Insert the image
        print(f"\n           📝 Inserting image into document...")
        
        if self.last_generated_image:
            # Read document
            with open(doc_result['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find good insertion point (after first paragraph)
            lines = content.split('\n')
            insertion_point = 3  # After title and first paragraph
            
            # Insert image
            img_markdown = f"\n\n![Generated Image]({self.last_generated_image})\n*Figure 1: Illustration for {request['title']}*\n\n"
            lines.insert(insertion_point, img_markdown)
            
            # Save updated document
            updated_content = '\n'.join(lines)
            with open(doc_result['file_path'], 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"           ✅ Image inserted successfully!")
            print(f"\n✅ Article created: {doc_result['file_path']}")
        else:
            print(f"           ⚠️  No recent image to insert")
    
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": f"Created article '{request['title']}' with image"})
```

### Track Last Generated Image (Add after image generation)

```python
if result.get('success'):
    self.last_generated_image = result['path']  # Track for insertion
    print(f"\n✅ Image created successfully!")
```

## Testing Checklist

- [ ] "create image of X" generates image
- [ ] "insert that image in article titled Y" creates article with image
- [ ] System executes instead of chatting about it
- [ ] Progress shown for all steps
- [ ] Files created in correct locations
- [ ] Workspace displayed after generation

## Quick Fix for Current Issue

The IMMEDIATE fix needed is in `interactive_mode()`. Add this handler BEFORE the chat handler:

```python
elif request['action'] == 'insert_image_in_document':
    # EXECUTE the task, don't chat about it
    result = self.create_article_with_image(
        title=request['title'],
        image_path=self.last_generated_image
    )
```

This ensures the system DOES the work instead of talking about doing it.

## Installation Commands

```bash
# For OCR
pip install pytesseract Pillow
# Download Tesseract: https://github.com/tesseract-ocr/tesseract

# For web scraping
pip install playwright selenium
playwright install

# For streaming content
pip install openai --upgrade  # Streaming support
```

## Summary

The core systems are built and working. What's needed now is connecting the pieces - specifically making the system **execute** image insertion tasks instead of **chatting** about them, and adding the handler code shown above to `interactive_mode()`.

The fix is straightforward: detect `'insert_image_in_document'` action and route to execution, not chat.
