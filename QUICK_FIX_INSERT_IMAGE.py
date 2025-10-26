"""
QUICK FIX: Add this code to graive.py to enable image insertion

Location: In interactive_mode() method, add this BEFORE the 'else' clause that handles chat

This makes the system EXECUTE image insertion instead of chatting about it.
"""

# ADD THIS CODE BLOCK in interactive_mode() at line ~1247
# Right after the 'generate_image' action handler and BEFORE 'generate_document'

elif request['action'] == 'insert_image_in_document':
    # User wants image inserted into a document!
    print(f"\nManus AI: I'll create an article titled '{request['title']}' with your image.\n")
    
    print(f"{'='*70}")
    print(f"📝 CREATING ARTICLE WITH IMAGE")
    print(f"{'='*70}")
    print(f"Title: {request['title']}")
    if self.last_generated_image:
        print(f"Image: {Path(self.last_generated_image).name}")
    print(f"{'='*70}\n")
    
    # Step 1: Generate article content
    print("[Step 1/3] ✍️  Generating article content...")
    print(f"           Topic: {request['title']}")
    print(f"           Words: ~800")
    
    doc_result = self.generate_document(
        topic=request['title'],
        word_count=800,
        include_images=False,  # We'll add image manually
        include_tables=False,
        enable_phd_review=False  # Skip review for quick articles
    )
    
    if not doc_result.get('success'):
        print(f"\n❌ Failed to generate article")
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": f"Failed to create article: {doc_result.get('error')}"})
        continue
    
    print(f"           ✅ Article content generated\n")
    
    # Step 2: Insert image into document
    print("[Step 2/3] 🖼️  Inserting image into article...")
    
    if self.last_generated_image:
        try:
            # Read the generated document
            with open(doc_result['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find a good insertion point (after title and first section)
            lines = content.split('\n')
            insertion_idx = 5  # After frontmatter and first heading
            
            # Get relative path to image
            img_path = Path(self.last_generated_image)
            doc_path = Path(doc_result['file_path'])
            
            try:
                # Try to get relative path
                rel_path = os.path.relpath(img_path, doc_path.parent)
            except:
                # Fallback to absolute
                rel_path = str(img_path)
            
            # Create image markdown
            img_markdown = f"\n\n![Illustration for {request['title']}]({rel_path})\n\n*Figure 1: Visual representation related to {request['title']}*\n\n"
            
            # Insert image
            if insertion_idx < len(lines):
                lines.insert(insertion_idx, img_markdown)
            else:
                lines.append(img_markdown)
            
            # Write updated content
            updated_content = '\n'.join(lines)
            with open(doc_result['file_path'], 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"           ✅ Image inserted at line {insertion_idx}")
            print(f"           📍 Image: {img_path.name}\n")
            
        except Exception as e:
            print(f"           ⚠️  Could not insert image: {e}\n")
    else:
        print(f"           ⚠️  No recent image found to insert\n")
    
    # Step 3: Final summary
    print("[Step 3/3] ✅ Finalizing document...")
    
    print(f"\n{'='*70}")
    print(f"✅ ARTICLE WITH IMAGE CREATED")
    print(f"{'='*70}")
    print(f"📄 File: {Path(doc_result['file_path']).name}")
    print(f"📍 Location: {doc_result['file_path']}")
    print(f"📊 Words: {doc_result.get('word_count', 'N/A')}")
    if self.last_generated_image:
        print(f"🖼️  Image: Included")
    print(f"{'='*70}\n")
    
    # Show workspace
    self._show_workspace_contents()
    
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": f"Created article '{request['title']}' with image. Saved to {doc_result['file_path']}"})


# ALSO ADD THIS: Track last generated image
# In the 'generate_image' action handler (around line 1217), ADD after success check:

if result.get('success'):
    self.last_generated_image = result['path']  # ← ADD THIS LINE
    print(f"\n✅ Image created successfully!")
    # ... rest of code
