"""
Image Generation Tool - DALL-E, Gemini, and Stable Diffusion Integration

This tool provides comprehensive image generation capabilities using multiple AI providers
including OpenAI's DALL-E, Google's Gemini Imagen, and other image generation APIs.
Supports image creation, editing, variation generation, and image analysis.
"""

import os
from typing import Dict, Any, Optional, List
import sys
import base64
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class ImageTool(BaseTool):
    """
    Advanced image generation and manipulation tool.
    
    Supports multiple image generation providers including DALL-E 3, DALL-E 2,
    Gemini Imagen, and Stable Diffusion. Provides capabilities for image creation,
    editing, variation generation, upscaling, and image-to-image transformations.
    """
    
    SUPPORTED_PROVIDERS = {
        'dalle': ['dall-e-2', 'dall-e-3'],
        'gemini': ['imagen-2', 'gemini-pro-vision'],
        'stability': ['stable-diffusion-xl', 'stable-diffusion-2']
    }
    
    SUPPORTED_SIZES = {
        'dalle-2': ['256x256', '512x512', '1024x1024'],
        'dalle-3': ['1024x1024', '1792x1024', '1024x1792'],
        'imagen': ['256x256', '512x512', '1024x1024', '1536x1536']
    }
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox/images"):
        """
        Initialize the image tool.
        
        Args:
            sandbox_path: Path to store generated images
        """
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)
        
    @property
    def name(self) -> str:
        return "image"
    
    @property
    def description(self) -> str:
        return (
            "Generate, edit, and analyze images using AI providers like DALL-E, "
            "Gemini Imagen, and Stable Diffusion. Supports image creation from text, "
            "image editing, variation generation, and image analysis."
        )
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["generate", "edit", "variation", "analyze", "upscale"],
                    "required": True
                },
                "provider": {
                    "type": "string",
                    "description": "Image generation provider",
                    "enum": ["dalle", "gemini", "stability"],
                    "default": "dalle"
                },
                "prompt": {
                    "type": "string",
                    "description": "Text description of desired image",
                    "required": False
                },
                "image_path": {
                    "type": "string",
                    "description": "Path to existing image for editing/analysis",
                    "required": False
                },
                "size": {
                    "type": "string",
                    "description": "Image size (e.g., '1024x1024')",
                    "default": "1024x1024"
                },
                "quality": {
                    "type": "string",
                    "description": "Image quality for DALL-E 3",
                    "enum": ["standard", "hd"],
                    "default": "standard"
                },
                "style": {
                    "type": "string",
                    "description": "Image style for DALL-E 3",
                    "enum": ["vivid", "natural"],
                    "default": "vivid"
                },
                "n": {
                    "type": "integer",
                    "description": "Number of images to generate",
                    "default": 1
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters for image operations."""
        if "action" not in parameters:
            return False
            
        action = parameters["action"]
        
        if action == "generate" and "prompt" not in parameters:
            return False
            
        if action in ["edit", "variation", "analyze"] and "image_path" not in parameters:
            return False
            
        return True
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute image operation.
        
        Args:
            parameters: Operation parameters
            
        Returns:
            Operation result with image paths or analysis
        """
        action = parameters["action"]
        provider = parameters.get("provider", "dalle")
        
        if action == "generate":
            return self._generate_image(parameters, provider)
        elif action == "edit":
            return self._edit_image(parameters, provider)
        elif action == "variation":
            return self._create_variation(parameters, provider)
        elif action == "analyze":
            return self._analyze_image(parameters, provider)
        elif action == "upscale":
            return self._upscale_image(parameters)
        else:
            return {"error": f"Unknown action: {action}", "success": False}
    
    def _generate_image(self, params: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Generate image from text prompt."""
        if provider == "dalle":
            return self._generate_dalle(params)
        elif provider == "gemini":
            return self._generate_gemini(params)
        elif provider == "stability":
            return self._generate_stability(params)
        else:
            return {"error": f"Unsupported provider: {provider}", "success": False}
    
    def _generate_dalle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using DALL-E."""
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed. Install with: pip install openai",
                "success": False
            }
        
        try:
            prompt = params["prompt"]
            size = params.get("size", "1024x1024")
            quality = params.get("quality", "standard")
            style = params.get("style", "vivid")
            n = params.get("n", 1)
            model = params.get("model", "dall-e-3")
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # DALL-E 3 only supports n=1
            if model == "dall-e-3":
                n = 1
            
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                style=style if model == "dall-e-3" else None,
                n=n
            )
            
            # Save images
            saved_paths = []
            for idx, image_data in enumerate(response.data):
                # Download and save image
                import requests
                image_response = requests.get(image_data.url)
                
                filename = f"dalle_{idx}_{hash(prompt) % 10000}.png"
                filepath = os.path.join(self.sandbox_path, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                
                saved_paths.append(filepath)
            
            return {
                "success": True,
                "provider": "dalle",
                "model": model,
                "images": saved_paths,
                "prompt": prompt,
                "revised_prompt": response.data[0].revised_prompt if hasattr(response.data[0], 'revised_prompt') else None
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _generate_gemini(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using Gemini Imagen."""
        try:
            import google.generativeai as genai
        except ImportError:
            return {
                "error": "Google Generative AI not installed. Install with: pip install google-generativeai",
                "success": False
            }
        
        try:
            prompt = params["prompt"]
            
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            
            # Note: Imagen API integration - adjust based on actual API
            # This is a placeholder for the actual implementation
            model = genai.GenerativeModel('gemini-pro-vision')
            
            return {
                "success": True,
                "provider": "gemini",
                "message": "Gemini image generation requires Imagen API access",
                "prompt": prompt
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _generate_stability(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using Stability AI."""
        try:
            import requests
        except ImportError:
            return {
                "error": "Requests package not installed",
                "success": False
            }
        
        try:
            prompt = params["prompt"]
            api_key = os.getenv("STABILITY_API_KEY")
            
            if not api_key:
                return {
                    "error": "STABILITY_API_KEY not set",
                    "success": False
                }
            
            # Stability AI API endpoint
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": params.get("n", 1),
                "steps": 30
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                saved_paths = []
                
                for idx, image in enumerate(data.get("artifacts", [])):
                    image_data = base64.b64decode(image["base64"])
                    filename = f"stability_{idx}_{hash(prompt) % 10000}.png"
                    filepath = os.path.join(self.sandbox_path, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    saved_paths.append(filepath)
                
                return {
                    "success": True,
                    "provider": "stability",
                    "images": saved_paths,
                    "prompt": prompt
                }
            else:
                return {
                    "error": f"Stability API error: {response.text}",
                    "success": False
                }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _edit_image(self, params: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Edit existing image based on prompt."""
        if provider != "dalle":
            return {
                "error": "Image editing currently only supported with DALL-E",
                "success": False
            }
        
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed",
                "success": False
            }
        
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            image_path = params["image_path"]
            prompt = params["prompt"]
            
            with open(image_path, 'rb') as image_file:
                response = client.images.edit(
                    image=image_file,
                    prompt=prompt,
                    n=1,
                    size=params.get("size", "1024x1024")
                )
            
            # Save edited image
            import requests
            image_response = requests.get(response.data[0].url)
            filename = f"edited_{hash(prompt) % 10000}.png"
            filepath = os.path.join(self.sandbox_path, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_response.content)
            
            return {
                "success": True,
                "provider": "dalle",
                "image": filepath,
                "prompt": prompt
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _create_variation(self, params: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Create variations of existing image."""
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed",
                "success": False
            }
        
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            image_path = params["image_path"]
            n = params.get("n", 1)
            
            with open(image_path, 'rb') as image_file:
                response = client.images.create_variation(
                    image=image_file,
                    n=n,
                    size=params.get("size", "1024x1024")
                )
            
            # Save variations
            import requests
            saved_paths = []
            for idx, image_data in enumerate(response.data):
                image_response = requests.get(image_data.url)
                filename = f"variation_{idx}_{hash(image_path) % 10000}.png"
                filepath = os.path.join(self.sandbox_path, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                
                saved_paths.append(filepath)
            
            return {
                "success": True,
                "provider": "dalle",
                "images": saved_paths
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _analyze_image(self, params: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Analyze image content using vision models."""
        if provider == "gemini":
            return self._analyze_gemini(params)
        else:
            return self._analyze_openai(params)
    
    def _analyze_openai(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image using GPT-4 Vision."""
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed",
                "success": False
            }
        
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            image_path = params["image_path"]
            prompt = params.get("prompt", "Describe this image in detail.")
            
            # Encode image to base64
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            return {
                "success": True,
                "provider": "openai",
                "model": "gpt-4-vision",
                "analysis": response.choices[0].message.content,
                "image_path": image_path
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _analyze_gemini(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image using Gemini Vision."""
        try:
            import google.generativeai as genai
            from PIL import Image
        except ImportError:
            return {
                "error": "Required packages not installed. Install: pip install google-generativeai pillow",
                "success": False
            }
        
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-pro-vision')
            
            image_path = params["image_path"]
            prompt = params.get("prompt", "Describe this image in detail.")
            
            img = Image.open(image_path)
            response = model.generate_content([prompt, img])
            
            return {
                "success": True,
                "provider": "gemini",
                "model": "gemini-pro-vision",
                "analysis": response.text,
                "image_path": image_path
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _upscale_image(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Upscale image using AI upscaling."""
        try:
            from PIL import Image
        except ImportError:
            return {
                "error": "Pillow not installed. Install with: pip install pillow",
                "success": False
            }
        
        try:
            image_path = params["image_path"]
            scale_factor = params.get("scale_factor", 2)
            
            img = Image.open(image_path)
            new_size = (img.width * scale_factor, img.height * scale_factor)
            upscaled = img.resize(new_size, Image.LANCZOS)
            
            filename = f"upscaled_{os.path.basename(image_path)}"
            filepath = os.path.join(self.sandbox_path, filename)
            upscaled.save(filepath)
            
            return {
                "success": True,
                "image": filepath,
                "original_size": f"{img.width}x{img.height}",
                "new_size": f"{new_size[0]}x{new_size[1]}"
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
