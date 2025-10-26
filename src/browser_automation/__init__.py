"""Browser Automation Module - Advanced Web Control."""

from .browser_tool import (
    AdvancedBrowserAutomation,
    BrowserAutomationTool,
    HumanBehaviorSimulator,
    StealthBrowser,
    create_browser_tool,
    ADVANCED_BROWSER_AVAILABLE,
    BROWSER_IMPORT_ERROR,
)

__all__ = [
    "AdvancedBrowserAutomation",
    "StealthBrowser",
    "HumanBehaviorSimulator",
    "BrowserAutomationTool",
    "create_browser_tool",
    "ADVANCED_BROWSER_AVAILABLE",
    "BROWSER_IMPORT_ERROR",
]
