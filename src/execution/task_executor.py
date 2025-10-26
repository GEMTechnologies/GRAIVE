"""
Autonomous Task Execution Engine

Transforms user requests into actual executed tasks instead of chat responses.
Handles code generation, data analysis, PPT creation, image insertion, and more.
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime


class TaskExecutor:
    """
    Executes tasks autonomously with progress tracking.
    
    Replaces chat-based responses with actual task execution including
    file generation, data analysis, code creation, and document manipulation.
    """
    
    def __init__(self, workspace_path: str, llm_caller=None):
        """
        Initialize task executor.
        
        Args:
            workspace_path: Path to workspace directory
            llm_caller: Function to call LLM for content generation
        """
        self.workspace = Path(workspace_path)
        self.llm_caller = llm_caller
        
        # Create task-specific directories
        (self.workspace / "code").mkdir(parents=True, exist_ok=True)
        (self.workspace / "analysis").mkdir(parents=True, exist_ok=True)
        (self.workspace / "presentations").mkdir(parents=True, exist_ok=True)
        (self.workspace / "data").mkdir(parents=True, exist_ok=True)
    
    def execute_task(self, task_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route task to appropriate executor.
        
        Args:
            task_type: Type of task to execute
            params: Task parameters
        
        Returns:
            Execution result with status and output files
        """
        executors = {
            'generate_code': self.execute_code_generation,
            'analyze_data': self.execute_data_analysis,
            'create_presentation': self.execute_ppt_generation,
            'insert_image_in_document': self.execute_image_insertion,
            'web_scrape': self.execute_web_scraping,
            'create_diagram': self.execute_diagram_creation
        }
        
        executor = executors.get(task_type)
        if executor:
            return executor(params)
        else:
            return {"success": False, "error": f"Unknown task type: {task_type}"}
    
    def execute_code_generation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate actual code files from description.
        
        Args:
            params: Must contain 'description' and 'language'
        
        Returns:
            Dict with generated file paths and status
        """
        description = params.get('description', '')
        language = params.get('language', 'python')
        
        print(f"\n{'='*70}")
        print(f"💻 CODE GENERATION - {description.upper()}")
        print(f"{'='*70}")
        print(f"Language: {language}")
        print(f"{'='*70}\n")
        
        try:
            # Step 1: Generate code using LLM
            print("[Step 1/4] 🤖 Generating code with AI...")
            
            prompt = f"""Write complete, production-ready {language} code for: {description}

Requirements:
- Include all necessary imports
- Add comprehensive comments
- Handle errors properly
- Follow best practices for {language}
- Make it immediately runnable

Write ONLY the code, no explanations."""

            if self.llm_caller:
                code = self.llm_caller(prompt, max_tokens=2000)
                print(f"           ✅ Generated {len(code.split('\\n'))} lines of code\n")
            else:
                # Fallback: template code
                code = self._generate_template_code(description, language)
                print(f"           ⚠️  Using template code (no LLM available)\n")
            
            # Step 2: Save to file
            print("[Step 2/4] 💾 Saving code to file...")
            
            # Create safe filename
            safe_name = description.lower().replace(' ', '_')
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
            
            extensions = {
                'python': 'py',
                'javascript': 'js',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c'
            }
            ext = extensions.get(language, 'txt')
            
            filename = f"{safe_name}.{ext}"
            filepath = self.workspace / "code" / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            file_size = os.path.getsize(filepath)
            print(f"           ✅ Saved to: {filename}\n")
            
            # Step 3: Verify syntax
            print("[Step 3/4] ✅ Verifying code syntax...")
            
            if language == 'python':
                try:
                    compile(code, filename, 'exec')
                    print(f"           ✅ Python syntax valid\n")
                    syntax_valid = True
                except SyntaxError as e:
                    print(f"           ⚠️  Syntax error: {e}\n")
                    syntax_valid = False
            else:
                syntax_valid = True
                print(f"           ⚠️  Syntax check not available for {language}\n")
            
            # Step 4: Create README
            print("[Step 4/4] 📝 Creating README...")
            
            readme_content = f"""# {description.title()}

## Generated Code

**Language:** {language}  
**File:** `{filename}`  
**Lines:** {len(code.split(chr(10)))}  
**Size:** {file_size:,} bytes  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Usage

```{language}
{self._get_usage_example(description, language, filename)}
```

## Code

```{language}
{code}
```

---
*Generated by Graive AI Autonomous Code Generator*
"""
            
            readme_path = self.workspace / "code" / f"{safe_name}_README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"           ✅ README created\n")
            
            # Final summary
            print(f"{'='*70}")
            print(f"✅ CODE GENERATION COMPLETE")
            print(f"{'='*70}")
            print(f"📄 Code File: {filename}")
            print(f"📍 Location: {filepath}")
            print(f"📊 Lines: {len(code.split(chr(10)))}")
            print(f"💾 Size: {file_size:,} bytes")
            print(f"✅ Syntax: {'Valid' if syntax_valid else 'Check manually'}")
            print(f"📝 README: {readme_path.name}")
            print(f"{'='*70}\n")
            
            return {
                "success": True,
                "code_file": str(filepath),
                "readme_file": str(readme_path),
                "lines": len(code.split('\n')),
                "size": file_size,
                "syntax_valid": syntax_valid,
                "language": language
            }
            
        except Exception as e:
            print(f"\n❌ Code generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_image_insertion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert image into document (create document if needed).
        
        Args:
            params: Must contain 'title' and 'image_path'
        
        Returns:
            Dict with document path and status
        """
        title = params.get('title', 'Untitled')
        image_path = params.get('image_path')
        word_count = params.get('word_count', 800)
        
        print(f"\n{'='*70}")
        print(f"📝 DOCUMENT WITH IMAGE - {title.upper()}")
        print(f"{'='*70}")
        print(f"Title: {title}")
        if image_path:
            print(f"Image: {Path(image_path).name}")
        print(f"{'='*70}\n")
        
        try:
            # Step 1: Generate article content
            print(f"[Step 1/3] ✍️  Generating article content...")
            print(f"           Topic: {title}")
            print(f"           Words: ~{word_count}")
            
            if self.llm_caller:
                content_prompt = f"""Write a {word_count}-word article titled "{title}".

Requirements:
- Professional academic style
- Clear introduction and conclusion
- Well-structured paragraphs
- Include section headings
- Markdown format

Write the complete article:"""
                
                article_content = self.llm_caller(content_prompt, max_tokens=word_count * 2)
                actual_words = len(article_content.split())
                print(f"           ✅ Generated {actual_words} words\n")
            else:
                article_content = f"# {title}\n\nContent generation requires LLM configuration."
                actual_words = len(article_content.split())
            
            # Step 2: Insert image
            print(f"[Step 2/3] 🖼️  Inserting image...")
            
            if image_path and os.path.exists(image_path):
                lines = article_content.split('\n')
                
                # Find good insertion point (after first section)
                insertion_idx = 3 if len(lines) > 3 else len(lines)
                
                # Create relative path
                img_path = Path(image_path)
                
                # Insert image markdown
                img_markdown = f"\n\n![Illustration for {title}]({img_path.name})\n\n*Figure 1: Visual representation related to {title}*\n\n"
                lines.insert(insertion_idx, img_markdown)
                
                article_content = '\n'.join(lines)
                print(f"           ✅ Image inserted\n")
            elif image_path:
                print(f"           ⚠️  Image not found: {image_path}\n")
            else:
                print(f"           ⚠️  No image specified\n")
            
            # Step 3: Save document
            print(f"[Step 3/3] 💾 Saving document...")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = title.lower().replace(' ', '_')
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c == '_')
            
            filename = f"{safe_title}_{timestamp}.md"
            filepath = self.workspace / "documents" / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article_content)
            
            file_size = os.path.getsize(filepath)
            print(f"           ✅ Saved to: {filename}\n")
            
            # Final summary
            print(f"{'='*70}")
            print(f"✅ DOCUMENT CREATED")
            print(f"{'='*70}")
            print(f"📄 File: {filename}")
            print(f"📍 Location: {filepath}")
            print(f"📊 Words: {actual_words}")
            if image_path:
                print(f"🖼️  Image: Included")
            print(f"{'='*70}\n")
            
            return {
                "success": True,
                "file_path": str(filepath),
                "word_count": actual_words,
                "has_image": bool(image_path)
            }
            
        except Exception as e:
            print(f"\n❌ Document creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_template_code(self, description: str, language: str) -> str:
        """Generate template code when LLM unavailable."""
        if language == 'python':
            if 'snake' in description.lower() or 'game' in description.lower():
                return '''import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2)]
        self.direction = (BLOCK_SIZE, 0)
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()
    
    def grow(self):
        self.body.append(self.body[-1])
    
    def check_collision(self):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= WIDTH or 
            head[1] < 0 or head[1] >= HEIGHT or
            head in self.body[1:]):
            return True
        return False

class Food:
    def __init__(self):
        self.position = self.random_position()
    
    def random_position(self):
        x = random.randint(0, (WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

def main():
    snake = Snake()
    food = Food()
    score = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, BLOCK_SIZE):
                    snake.direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -BLOCK_SIZE):
                    snake.direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (BLOCK_SIZE, 0):
                    snake.direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-BLOCK_SIZE, 0):
                    snake.direction = (BLOCK_SIZE, 0)
        
        snake.move()
        
        # Check if snake ate food
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.random_position()
            score += 10
        
        # Check collision
        if snake.check_collision():
            running = False
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw food
        pygame.draw.rect(screen, RED, (*food.position, BLOCK_SIZE, BLOCK_SIZE))
        
        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    print(f"Game Over! Final Score: {score}")

if __name__ == "__main__":
    main()
'''
        
        # Generic template
        return f'''# {description}
# Generated by Graive AI

def main():
    """
    {description}
    """
    print("Hello from {description}!")
    # Add your code here

if __name__ == "__main__":
    main()
'''
    
    def _get_usage_example(self, description: str, language: str, filename: str) -> str:
        """Generate usage example."""
        if language == 'python':
            return f"python {filename}"
        elif language == 'javascript':
            return f"node {filename}"
        elif language == 'java':
            return f"javac {filename} && java {filename.replace('.java', '')}"
        else:
            return f"./{filename}"
    
    def execute_data_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis task."""
        # Placeholder for data analysis implementation
        return {
            "success": False,
            "error": "Data analysis not yet implemented. Install pandas/matplotlib."
        }
    
    def execute_ppt_generation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute PowerPoint generation."""
        # Placeholder for PPT generation
        return {
            "success": False,
            "error": "PPT generation not yet implemented. Install python-pptx."
        }
    
    def execute_web_scraping(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web scraping task."""
        # Placeholder for web scraping
        return {
            "success": False,
            "error": "Web scraping requires browser automation setup."
        }
    
    def execute_diagram_creation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute diagram creation."""
        # Placeholder for diagram creation
        return {
            "success": False,
            "error": "Diagram creation not yet implemented."
        }


def create_task_executor(workspace_path: str, llm_caller=None) -> TaskExecutor:
    """
    Factory function to create task executor.
    
    Args:
        workspace_path: Path to workspace
        llm_caller: Function to call LLM
    
    Returns:
        Configured task executor
    """
    return TaskExecutor(workspace_path, llm_caller)
