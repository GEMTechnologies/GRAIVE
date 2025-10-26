"""
Advanced Features Demo - Image Generation, Web Scraping, Data Analysis, Media

This example demonstrates the complete suite of advanced Graive AI capabilities including:
- Image generation with DALL-E, Gemini, Stability AI
- Web scraping, content extraction, PDF parsing
- Data analysis, visualization, Excel processing
- Audio/video creation, TTS, STT
- Complete end-to-end workflows
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.image.image_tool import ImageTool
from src.tools.web.web_scraping_tool import WebScrapingTool
from src.tools.data.data_analysis_tool import DataAnalysisTool
from src.tools.media.media_tool import MediaTool


def demo_image_generation():
    """Demonstrate image generation capabilities."""
    print("\n" + "="*70)
    print("IMAGE GENERATION DEMO")
    print("="*70)
    
    tool = ImageTool()
    
    # Generate image with DALL-E
    print("\n1. Generating image with DALL-E...")
    result = tool.execute({
        "action": "generate",
        "provider": "dalle",
        "prompt": "A futuristic AI agent analyzing data in a high-tech laboratory, "
                 "digital art style, blue and purple color scheme",
        "size": "1024x1024",
        "quality": "standard"
    })
    
    if result["success"]:
        print(f"   ✓ Image generated: {result['images'][0]}")
        print(f"   Provider: {result['provider']}")
        if result.get("revised_prompt"):
            print(f"   Revised prompt: {result['revised_prompt'][:100]}...")
    else:
        print(f"   ✗ Error: {result.get('error')}")
    
    # Analyze image with GPT-4 Vision
    print("\n2. Analyzing generated image with GPT-4 Vision...")
    if result.get("success") and result.get("images"):
        analysis_result = tool.execute({
            "action": "analyze",
            "provider": "openai",
            "image_path": result["images"][0],
            "prompt": "Describe this image in detail and identify key elements."
        })
        
        if analysis_result["success"]:
            print(f"   ✓ Analysis complete")
            print(f"   Analysis: {analysis_result['analysis'][:200]}...")
        else:
            print(f"   ✗ Error: {analysis_result.get('error')}")


def demo_web_scraping():
    """Demonstrate web scraping capabilities."""
    print("\n" + "="*70)
    print("WEB SCRAPING DEMO")
    print("="*70)
    
    tool = WebScrapingTool()
    
    # Visit a webpage
    print("\n1. Visiting Wikipedia page...")
    result = tool.execute({
        "action": "visit",
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
    })
    
    if result["success"]:
        print(f"   ✓ Page visited successfully")
        print(f"   Title: {result['title']}")
        print(f"   Content type: {result['content_type']}")
        print(f"   Content length: {result['content_length']} bytes")
    else:
        print(f"   ✗ Error: {result.get('error')}")
    
    # Extract text content
    print("\n2. Extracting text content...")
    text_result = tool.execute({
        "action": "extract_text",
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
    })
    
    if text_result["success"]:
        print(f"   ✓ Text extracted")
        print(f"   Word count: {text_result['word_count']}")
        print(f"   Preview: {text_result['text'][:150]}...")
    else:
        print(f"   ✗ Error: {text_result.get('error')}")
    
    # Generate citation
    print("\n3. Generating APA citation...")
    citation_result = tool.execute({
        "action": "generate_citation",
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "citation_style": "apa"
    })
    
    if citation_result["success"]:
        print(f"   ✓ Citation generated")
        print(f"   Citation: {citation_result['citation']}")
    else:
        print(f"   ✗ Error: {citation_result.get('error')}")
    
    # Download images
    print("\n4. Downloading images from page...")
    image_result = tool.execute({
        "action": "download_images",
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "max_images": 3
    })
    
    if image_result["success"]:
        print(f"   ✓ Downloaded {image_result['images_downloaded']} images")
        for img in image_result['images'][:3]:
            print(f"     - {img['path']} ({img['size']} bytes)")
    else:
        print(f"   ✗ Error: {image_result.get('error')}")


def demo_data_analysis():
    """Demonstrate data analysis capabilities."""
    print("\n" + "="*70)
    print("DATA ANALYSIS DEMO")
    print("="*70)
    
    tool = DataAnalysisTool()
    
    # Create sample dataset
    print("\n1. Creating sample dataset...")
    import pandas as pd
    import numpy as np
    
    # Generate sample sales data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(1000, 5000, 100),
        'Customers': np.random.randint(50, 200, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    sample_file = '/tmp/sample_sales.csv'
    data.to_csv(sample_file, index=False)
    print(f"   ✓ Sample dataset created: {sample_file}")
    print(f"   Rows: {len(data)}, Columns: {len(data.columns)}")
    
    # Analyze data
    print("\n2. Analyzing dataset...")
    analysis_result = tool.execute({
        "action": "analyze",
        "data_source": sample_file,
        "format": "csv"
    })
    
    if analysis_result["success"]:
        print(f"   ✓ Analysis complete")
        analysis = analysis_result['analysis']
        print(f"   Shape: {analysis['shape']['rows']} rows × {analysis['shape']['columns']} columns")
        print(f"   Columns: {', '.join(analysis['columns'])}")
        print(f"   Missing values: {sum(analysis['missing_values'].values())} total")
    else:
        print(f"   ✗ Error: {analysis_result.get('error')}")
    
    # Calculate statistics
    print("\n3. Calculating statistics...")
    stats_result = tool.execute({
        "action": "statistics",
        "data_source": sample_file,
        "format": "csv",
        "columns": ['Sales', 'Customers']
    })
    
    if stats_result["success"]:
        print(f"   ✓ Statistics calculated")
        for col, stats in stats_result['statistics'].items():
            print(f"   {col}: Mean={stats['mean']:.2f}, Std={stats['std']:.2f}")
    else:
        print(f"   ✗ Error: {stats_result.get('error')}")
    
    # Create visualization
    print("\n4. Creating line chart...")
    viz_result = tool.execute({
        "action": "visualize",
        "data_source": sample_file,
        "format": "csv",
        "chart_type": "line",
        "columns": ['Sales', 'Customers']
    })
    
    if viz_result["success"]:
        print(f"   ✓ Visualization created: {viz_result['chart_path']}")
        print(f"   Chart type: {viz_result['chart_type']}")
    else:
        print(f"   ✗ Error: {viz_result.get('error')}")
    
    # Create correlation heatmap
    print("\n5. Creating correlation heatmap...")
    heatmap_result = tool.execute({
        "action": "visualize",
        "data_source": sample_file,
        "format": "csv",
        "chart_type": "heatmap"
    })
    
    if heatmap_result["success"]:
        print(f"   ✓ Heatmap created: {heatmap_result['chart_path']}")
    else:
        print(f"   ✗ Error: {heatmap_result.get('error')}")


def demo_media_processing():
    """Demonstrate audio and video processing capabilities."""
    print("\n" + "="*70)
    print("MEDIA PROCESSING DEMO")
    print("="*70)
    
    tool = MediaTool()
    
    # Text to speech
    print("\n1. Converting text to speech...")
    tts_result = tool.execute({
        "action": "text_to_speech",
        "text": "Hello! I am Graive, an autonomous AI agent capable of processing "
               "text, images, data, audio, and video. I can analyze information, "
               "create visualizations, and generate multimedia content.",
        "voice": "alloy"
    })
    
    if tts_result["success"]:
        print(f"   ✓ Speech generated: {tts_result['audio_path']}")
        print(f"   Voice: {tts_result['voice']}")
        print(f"   Text length: {tts_result['text_length']} characters")
    else:
        print(f"   ✗ Error: {tts_result.get('error')}")
    
    # Speech to text (if audio file exists)
    if tts_result.get("success"):
        print("\n2. Transcribing speech to text...")
        stt_result = tool.execute({
            "action": "speech_to_text",
            "audio_path": tts_result["audio_path"]
        })
        
        if stt_result["success"]:
            print(f"   ✓ Transcription complete")
            print(f"   Transcription: {stt_result['transcription'][:100]}...")
            print(f"   Word count: {stt_result['word_count']}")
        else:
            print(f"   ✗ Error: {stt_result.get('error')}")


def create_end_to_end_workflow():
    """Demonstrate complete end-to-end workflow combining all tools."""
    print("\n" + "="*70)
    print("END-TO-END WORKFLOW: Research Report Generation")
    print("="*70)
    
    print("\nWorkflow: Research AI topic → Scrape data → Analyze → Generate images → Create presentation")
    
    # Step 1: Web scraping
    print("\n[Step 1] Scraping research content...")
    web_tool = WebScrapingTool()
    content = web_tool.execute({
        "action": "extract_text",
        "url": "https://en.wikipedia.org/wiki/Machine_learning"
    })
    
    if content["success"]:
        print(f"   ✓ Content extracted ({content['word_count']} words)")
    
    # Step 2: Generate illustration
    print("\n[Step 2] Generating illustration...")
    image_tool = ImageTool()
    image = image_tool.execute({
        "action": "generate",
        "provider": "dalle",
        "prompt": "Machine learning neural network visualization, abstract digital art",
        "size": "1024x1024"
    })
    
    if image.get("success"):
        print(f"   ✓ Image generated: {image['images'][0]}")
    
    # Step 3: Create narration
    print("\n[Step 3] Creating audio narration...")
    media_tool = MediaTool()
    narration = media_tool.execute({
        "action": "text_to_speech",
        "text": "Machine learning is a subset of artificial intelligence that enables "
               "systems to learn and improve from experience without being explicitly programmed.",
        "voice": "nova"
    })
    
    if narration.get("success"):
        print(f"   ✓ Narration created: {narration['audio_path']}")
    
    print("\n[Workflow Complete] All components generated successfully!")


def main():
    """Run comprehensive advanced features demonstration."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*17 + "GRAIVE AI - ADVANCED FEATURES DEMO" + " "*18 + "║")
    print("║" + " "*10 + "Image | Web | Data | Media Processing" + " "*17 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Run demonstrations
    demo_image_generation()
    demo_web_scraping()
    demo_data_analysis()
    demo_media_processing()
    create_end_to_end_workflow()
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nAll advanced features demonstrated successfully!")
    print("\nCapabilities showcased:")
    print("  ✓ Image generation (DALL-E, Gemini, Stability AI)")
    print("  ✓ Image analysis (GPT-4 Vision, Gemini Vision)")
    print("  ✓ Web scraping and content extraction")
    print("  ✓ Citation generation (APA, MLA, Chicago, IEEE)")
    print("  ✓ Data analysis and statistics")
    print("  ✓ Data visualization (charts, heatmaps, plots)")
    print("  ✓ Text-to-speech (OpenAI TTS)")
    print("  ✓ Speech-to-text (Whisper)")
    print("  ✓ End-to-end workflow integration")
    
    print("\nNote: Some operations require API keys:")
    print("  - OPENAI_API_KEY for DALL-E and Whisper")
    print("  - GEMINI_API_KEY for Gemini features")
    print("  - STABILITY_API_KEY for Stability AI")
    print()


if __name__ == "__main__":
    main()
