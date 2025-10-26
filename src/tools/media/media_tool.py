"""
Audio and Video Tool

This tool provides comprehensive audio and video processing capabilities including
text-to-speech, speech-to-text, audio generation, video creation, video editing,
and multimedia manipulation using various AI services and libraries.
"""

import os
from typing import Dict, Any, Optional, List
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class MediaTool(BaseTool):
    """
    Advanced audio and video processing tool.
    
    Provides capabilities for text-to-speech, speech recognition, audio generation,
    video creation, video editing, and multimedia manipulation. Supports OpenAI TTS,
    Whisper, ElevenLabs, and various video processing libraries.
    """
    
    AUDIO_FORMATS = ['mp3', 'wav', 'ogg', 'flac', 'm4a']
    VIDEO_FORMATS = ['mp4', 'avi', 'mov', 'webm', 'mkv']
    TTS_VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox/media"):
        """
        Initialize the media tool.
        
        Args:
            sandbox_path: Path to store media files
        """
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "audio"), exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "video"), exist_ok=True)
        
    @property
    def name(self) -> str:
        return "media"
    
    @property
    def description(self) -> str:
        return (
            "Process audio and video files. Generate speech from text (TTS), "
            "transcribe audio to text (STT), create videos, edit multimedia, "
            "and manipulate audio/video files using AI services and libraries."
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
                    "enum": [
                        "text_to_speech", "speech_to_text", "generate_audio",
                        "create_video", "edit_video", "extract_audio",
                        "add_subtitles", "merge_videos", "convert_format"
                    ],
                    "required": True
                },
                "text": {
                    "type": "string",
                    "description": "Text for TTS or subtitles",
                    "required": False
                },
                "audio_path": {
                    "type": "string",
                    "description": "Path to audio file",
                    "required": False
                },
                "video_path": {
                    "type": "string",
                    "description": "Path to video file",
                    "required": False
                },
                "voice": {
                    "type": "string",
                    "description": "Voice for TTS",
                    "enum": TTS_VOICES,
                    "default": "alloy"
                },
                "language": {
                    "type": "string",
                    "description": "Language code (e.g., 'en', 'es')",
                    "default": "en"
                },
                "format": {
                    "type": "string",
                    "description": "Output format",
                    "required": False
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters for media operations."""
        return "action" in parameters
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute media operation.
        
        Args:
            parameters: Operation parameters
            
        Returns:
            Operation result with file paths or transcription
        """
        action = parameters["action"]
        
        action_map = {
            "text_to_speech": self._text_to_speech,
            "speech_to_text": self._speech_to_text,
            "generate_audio": self._generate_audio,
            "create_video": self._create_video,
            "edit_video": self._edit_video,
            "extract_audio": self._extract_audio,
            "add_subtitles": self._add_subtitles,
            "merge_videos": self._merge_videos,
            "convert_format": self._convert_format
        }
        
        handler = action_map.get(action)
        if handler:
            return handler(parameters)
        else:
            return {"error": f"Unknown action: {action}", "success": False}
    
    def _text_to_speech(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert text to speech using OpenAI TTS."""
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed. Install: pip install openai",
                "success": False
            }
        
        try:
            text = params["text"]
            voice = params.get("voice", "alloy")
            model = params.get("model", "tts-1")
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            
            # Save audio file
            filename = f"tts_{hash(text) % 100000}.mp3"
            filepath = os.path.join(self.sandbox_path, "audio", filename)
            
            response.stream_to_file(filepath)
            
            return {
                "success": True,
                "audio_path": filepath,
                "voice": voice,
                "text_length": len(text)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _speech_to_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Transcribe speech to text using OpenAI Whisper."""
        try:
            import openai
        except ImportError:
            return {
                "error": "OpenAI package not installed",
                "success": False
            }
        
        try:
            audio_path = params["audio_path"]
            model = params.get("model", "whisper-1")
            language = params.get("language")
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            with open(audio_path, 'rb') as audio_file:
                if language:
                    transcript = client.audio.transcriptions.create(
                        model=model,
                        file=audio_file,
                        language=language
                    )
                else:
                    transcript = client.audio.transcriptions.create(
                        model=model,
                        file=audio_file
                    )
            
            return {
                "success": True,
                "transcription": transcript.text,
                "audio_path": audio_path,
                "word_count": len(transcript.text.split())
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _generate_audio(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate audio using AI (placeholder for services like ElevenLabs)."""
        # This would integrate with services like ElevenLabs
        return {
            "success": False,
            "message": "Audio generation requires third-party service integration (e.g., ElevenLabs)",
            "alternative": "Use text_to_speech action for OpenAI TTS"
        }
    
    def _create_video(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create video from images and audio."""
        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        except ImportError:
            return {
                "error": "MoviePy not installed. Install: pip install moviepy",
                "success": False
            }
        
        try:
            images = params.get("images", [])
            audio_path = params.get("audio_path")
            duration_per_image = params.get("duration_per_image", 3)
            fps = params.get("fps", 24)
            
            if not images:
                return {"error": "No images provided", "success": False}
            
            # Create video clips from images
            clips = []
            for img_path in images:
                clip = ImageClip(img_path, duration=duration_per_image)
                clips.append(clip)
            
            # Concatenate clips
            video = concatenate_videoclips(clips, method="compose")
            
            # Add audio if provided
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video = video.set_audio(audio)
            
            # Save video
            filename = f"video_{hash(str(images)) % 100000}.mp4"
            filepath = os.path.join(self.sandbox_path, "video", filename)
            
            video.write_videofile(filepath, fps=fps, codec='libx264', audio_codec='aac')
            
            return {
                "success": True,
                "video_path": filepath,
                "num_images": len(images),
                "duration": len(images) * duration_per_image
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _edit_video(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Edit video file (trim, crop, etc.)."""
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            return {
                "error": "MoviePy not installed",
                "success": False
            }
        
        try:
            video_path = params["video_path"]
            operation = params.get("operation", "trim")
            
            video = VideoFileClip(video_path)
            
            if operation == "trim":
                start_time = params.get("start_time", 0)
                end_time = params.get("end_time", video.duration)
                video = video.subclip(start_time, end_time)
            
            elif operation == "resize":
                width = params.get("width")
                height = params.get("height")
                if width and height:
                    video = video.resize((width, height))
            
            elif operation == "speed":
                speed_factor = params.get("speed_factor", 1.0)
                video = video.speedx(speed_factor)
            
            # Save edited video
            filename = f"edited_{os.path.basename(video_path)}"
            filepath = os.path.join(self.sandbox_path, "video", filename)
            
            video.write_videofile(filepath, codec='libx264', audio_codec='aac')
            
            return {
                "success": True,
                "video_path": filepath,
                "operation": operation
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _extract_audio(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract audio from video file."""
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            return {
                "error": "MoviePy not installed",
                "success": False
            }
        
        try:
            video_path = params["video_path"]
            
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                return {"error": "Video has no audio track", "success": False}
            
            # Save audio
            filename = f"extracted_audio_{os.path.basename(video_path)}.mp3"
            filepath = os.path.join(self.sandbox_path, "audio", filename)
            
            audio.write_audiofile(filepath)
            
            return {
                "success": True,
                "audio_path": filepath,
                "duration": audio.duration
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _add_subtitles(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add subtitles to video."""
        try:
            from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        except ImportError:
            return {
                "error": "MoviePy not installed",
                "success": False
            }
        
        try:
            video_path = params["video_path"]
            subtitles = params.get("subtitles", [])
            
            video = VideoFileClip(video_path)
            
            subtitle_clips = []
            for subtitle in subtitles:
                text = subtitle.get("text", "")
                start = subtitle.get("start", 0)
                end = subtitle.get("end", 5)
                
                txt_clip = TextClip(
                    text,
                    fontsize=24,
                    color='white',
                    bg_color='black',
                    size=video.size
                ).set_position(('center', 'bottom')).set_start(start).set_end(end)
                
                subtitle_clips.append(txt_clip)
            
            # Composite video with subtitles
            final_video = CompositeVideoClip([video] + subtitle_clips)
            
            # Save video with subtitles
            filename = f"subtitled_{os.path.basename(video_path)}"
            filepath = os.path.join(self.sandbox_path, "video", filename)
            
            final_video.write_videofile(filepath, codec='libx264', audio_codec='aac')
            
            return {
                "success": True,
                "video_path": filepath,
                "num_subtitles": len(subtitles)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _merge_videos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple video files."""
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
        except ImportError:
            return {
                "error": "MoviePy not installed",
                "success": False
            }
        
        try:
            video_paths = params.get("video_paths", [])
            
            if len(video_paths) < 2:
                return {"error": "Need at least 2 videos to merge", "success": False}
            
            clips = [VideoFileClip(path) for path in video_paths]
            
            # Concatenate videos
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Save merged video
            filename = f"merged_{hash(str(video_paths)) % 100000}.mp4"
            filepath = os.path.join(self.sandbox_path, "video", filename)
            
            final_video.write_videofile(filepath, codec='libx264', audio_codec='aac')
            
            return {
                "success": True,
                "video_path": filepath,
                "num_videos_merged": len(video_paths),
                "total_duration": final_video.duration
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _convert_format(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert audio/video file format."""
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
        except ImportError:
            return {
                "error": "MoviePy not installed",
                "success": False
            }
        
        try:
            input_path = params.get("input_path")
            output_format = params.get("output_format")
            media_type = params.get("media_type", "video")
            
            if media_type == "video":
                clip = VideoFileClip(input_path)
                output_dir = os.path.join(self.sandbox_path, "video")
            else:
                clip = AudioFileClip(input_path)
                output_dir = os.path.join(self.sandbox_path, "audio")
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            filename = f"{base_name}_converted.{output_format}"
            filepath = os.path.join(output_dir, filename)
            
            # Convert
            if media_type == "video":
                clip.write_videofile(filepath, codec='libx264', audio_codec='aac')
            else:
                clip.write_audiofile(filepath)
            
            return {
                "success": True,
                "output_path": filepath,
                "original_format": os.path.splitext(input_path)[1],
                "new_format": output_format
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
