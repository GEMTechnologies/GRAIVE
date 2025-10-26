# Graive AI - Image Generation System

## Overview

Graive AI now includes a comprehensive image generation system that can create, download, or generate images on demand. The system automatically routes image requests to the appropriate generation method based on the description.

## Capabilities

The image generation system supports three methods of creating images, automatically selecting the best approach based on the request.

### Programmatic Generation

For simple, well-defined images such as flags, logos, and basic graphics, the system generates images programmatically using PIL/Pillow. This method is fast, free, and produces high-quality results for geometric patterns and standard designs.

The system currently includes built-in generators for national flags (Japan, USA, and more), simple charts and diagrams, and geometric shapes and patterns. These are created instantly without requiring external APIs.

### Web Download

For photographs, stock images, and common visual content, the system can download images from free sources such as Wikimedia Commons, Unsplash, and Pexels. This provides access to millions of high-quality professional images.

### AI Generation

For complex, creative, or custom images, the system can use AI generation APIs including OpenAI DALL-E 3, Stable Diffusion, and other image generation models. This allows creation of completely original images from textual descriptions.

## Usage Examples

### Natural Language Requests

The system understands natural language image requests and automatically creates the requested images.

**Example 1: Flag Generation**
```
You: give me flag of japan image now

Graive AI: I'll generate an image of 'flag of japan' for you.
          This will take just a moment...

======================================================================
🖼️  IMAGE GENERATION
======================================================================
Description: flag of japan
Method: auto
Size: 1024x1024
======================================================================

[Auto-detect] Using method: programmatic

[Step 1/3] 🎨 Generating image programmatically...
           Detected: Flag of Japan
           Creating: White background with red circle

[Step 2/3] 💾 Saving image...
           ✅ Saved to: flag_of_japan_20251026_164522.png
           Size: 45,678 bytes

[Step 3/3] ✅ Image generation complete!

======================================================================
✅ IMAGE GENERATED SUCCESSFULLY
======================================================================
📄 File: flag_of_japan_20251026_164522.png
📍 Location: C:\Users\...\workspace\images\flag_of_japan_20251026_164522.png
📐 Dimensions: 1024x1024
💾 Size: 45,678 bytes
======================================================================

✅ Image created successfully!
   📁 Saved to: flag_of_japan_20251026_164522.png
   📍 Full path: C:\Users\...\workspace\images\flag_of_japan_20251026_164522.png
```

**Example 2: AI-Generated Image**
```
You: create an image of a futuristic city at sunset

Graive AI: I'll generate an image of 'futuristic city at sunset' for you.

[Using DALL-E 3 for complex image generation]
Generating... (20-30 seconds)
✅ Image created successfully!
```

**Example 3: Web Download**
```
You: get me a picture of the Eiffel Tower

Graive AI: I'll find and download 'picture of eiffel tower' for you.

[Searching Wikimedia Commons...]
✅ Image downloaded successfully!
```

## Automatic Method Selection

The system automatically detects the best generation method based on keywords in your request.

**Programmatic Generation Triggers:**
- "flag" → Generates flags programmatically
- "chart" → Creates charts/graphs  
- "simple" → Uses geometric generation

**Web Download Triggers:**
- "photo" → Downloads from image libraries
- "picture" → Searches free stock photos
- "landscape" → Finds photography

**AI Generation Triggers:**
- Complex descriptions → Uses DALL-E
- Creative concepts → AI generation
- Custom designs → AI-generated

## Installation Requirements

### Basic Image Generation (Programmatic)

For basic image generation including flags and simple graphics, install Pillow:

```bash
pip install Pillow
```

This enables instant creation of flags, charts, and geometric images without requiring API keys.

### AI Image Generation (DALL-E)

For AI-powered image generation, ensure you have an OpenAI API key configured in the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

DALL-E 3 generates high-quality, creative images from text descriptions but incurs API costs (approximately $0.04 per image for standard quality).

### Web Image Download

For downloading images from the web, no additional configuration is required. The system automatically uses free sources like Wikimedia Commons.

## Supported Image Types

### Flags
- All national flags
- State/regional flags  
- Historical flags
- Custom flag designs

### Charts and Diagrams
- Bar charts
- Pie charts
- Line graphs
- Flowcharts

### AI-Generated Content
- Landscapes and scenery
- Abstract art
- Character designs
- Product visualizations
- Architectural concepts
- Scientific illustrations

### Downloaded Images
- Photographs
- Stock images
- Historical images
- Public domain art

## File Organization

All generated images are automatically saved to the workspace images directory with descriptive filenames and timestamps.

```
workspace/
└── images/
    ├── flag_of_japan_20251026_164522.png
    ├── ai_generated_futuristic_city_20251026_165834.png
    ├── chart_sales_data_20251026_170142.png
    └── downloaded_eiffel_tower_20251026_171255.png
```

Each filename includes the image type, description, and timestamp for easy identification and organization.

## Image Metadata

Every generated image includes metadata in the return result including the full file path, filename, dimensions (width x height), file size in bytes, generation method used, and original description.

This metadata is automatically logged and can be accessed for documentation or tracking purposes.

## Integration with Document Generation

Images generated through the image system can be automatically included in documents. When generating a document with images, the system creates the images first and then embeds them properly in the document with captions and numbering.

**Example:**
```
You: write an essay about Japan with images

[System generates essay content]
[System generates flag of Japan image]
[System generates cultural images]
[System embeds images in document with proper formatting]

Result: Complete document with professionally embedded images
```

## Cost Considerations

**Programmatic Generation:** Free (uses local computation only)

**Web Download:** Free (uses public domain/creative commons images)

**AI Generation (DALL-E 3):**
- Standard quality (1024x1024): $0.040 per image
- HD quality (1024x1792): $0.080 per image

The system automatically selects the free programmatic or download methods when possible, only using AI generation for complex creative requests.

## Error Handling

If image generation fails for any reason, the system provides graceful fallback behavior.

### PIL/Pillow Not Installed

When Pillow is not installed, the system creates a text placeholder file with the image description and instructions for installing Pillow.

### API Key Missing

When requesting AI generation without an API key, the system automatically falls back to programmatic generation or downloads, ensuring you always get some result.

### Download Failures

If web downloads fail due to network issues, the system attempts alternative sources or falls back to programmatic generation.

## Advanced Usage

### Specify Generation Method

```python
# Force programmatic generation
result = graive.image_generator.generate_image(
    description="flag of usa",
    method="programmatic",
    size="1024x1024"
)

# Force AI generation
result = graive.image_generator.generate_image(
    description="cyberpunk cityscape",
    method="ai",
    size="1024x1024"
)

# Force web download
result = graive.image_generator.generate_image(
    description="mountain landscape",
    method="web",
    size="1920x1080"
)
```

### Custom Image Sizes

```python
# Square images
size="1024x1024"  # Standard
size="512x512"    # Smaller

# Landscape
size="1792x1024"  # Wide
size="1920x1080"  # HD

# Portrait  
size="1024x1792"  # Tall
```

## Real-Time Progress Tracking

The image generation system provides complete progress visibility showing the detection of image type, generation method selected, step-by-step progress through creation, file saving confirmation, and final summary with full path.

This ensures you always know exactly what's happening during image generation, maintaining the same transparency as document generation.

## Summary

Graive AI's image generation system provides a comprehensive solution for creating images on demand, supporting programmatic generation for simple images, web downloads for stock imagery, and AI generation for creative content. The system automatically selects the best method, provides complete progress tracking, and integrates seamlessly with document generation.

Whether you need a simple flag, a professional photograph, or a completely original AI-generated image, the system handles your request intelligently and efficiently.
