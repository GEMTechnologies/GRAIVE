"""
Browser Automation Module - Advanced Web Control

Provides sophisticated browser automation with human-like behavior and anti-detection:
- Stealth mode to bypass bot detection (Cloudflare, reCAPTCHA)
- Human-like mouse movements and typing patterns
- Screenshot capture with element highlighting
- Complete text extraction from pages
- File downloads with folder organization
- Session persistence and restoration
"""

from src.browser_automation.advanced_browser import (
    AdvancedBrowserAutomation,
    StealthBrowser,
    HumanBehaviorSimulator
)

from src.browser_automation.browser_tool import (
    BrowserAutomationTool,
    create_browser_tool
)

__all__ = [
    "AdvancedBrowserAutomation",
    "StealthBrowser",
    "HumanBehaviorSimulator",
    "BrowserAutomationTool",
    "create_browser_tool"
]
