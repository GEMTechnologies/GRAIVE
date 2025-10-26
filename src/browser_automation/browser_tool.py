"""Browser Automation Tool - Integration with Graive AI."""

from typing import Any, Dict, List, Optional

try:
    from .advanced_browser import (
        AdvancedBrowserAutomation as _AdvancedBrowserAutomation,
        StealthBrowser as _StealthBrowser,
        HumanBehaviorSimulator as _HumanBehaviorSimulator,
    )
    ADVANCED_BROWSER_AVAILABLE = True
    BROWSER_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - exercised in fallback unit tests
    from .fallback_browser import (
        AdvancedBrowserAutomation as _AdvancedBrowserAutomation,
        StealthBrowser as _StealthBrowser,
        HumanBehaviorSimulator as _HumanBehaviorSimulator,
    )
    ADVANCED_BROWSER_AVAILABLE = False
    BROWSER_IMPORT_ERROR = exc

AdvancedBrowserAutomation = _AdvancedBrowserAutomation
StealthBrowser = _StealthBrowser
HumanBehaviorSimulator = _HumanBehaviorSimulator


class BrowserAutomationTool:
    """
    Unified tool for browser automation in Graive AI.
    
    Provides high-level interface for web interaction, content extraction,
    file downloads, and session management.
    """
    
    def __init__(
        self,
        headless: bool = False,
        storage_manager: Optional[Any] = None
    ):
        """
        Initialize browser automation tool.
        
        Args:
            headless: Run browser in headless mode
            storage_manager: Optional storage manager for artifacts
        """
        self.automation = AdvancedBrowserAutomation(
            headless=headless,
            storage_manager=storage_manager
        )
        self.name = "browser_automation_tool"
        self.description = "Advanced browser automation with anti-detection and human-like behavior"
    
    def get_available_actions(self) -> List[str]:
        """Get list of available browser actions."""
        return [
            # Navigation
            "start_browser",
            "navigate",
            "close_browser",
            
            # Content Extraction
            "take_screenshot",
            "extract_text",
            "extract_links",
            "extract_images",
            
            # Downloads
            "download_file",
            "create_folder",
            
            # Session Management
            "save_session",
            "restore_session",
            "get_cookies",
            "clear_cookies",
            
            # Interaction
            "click_element",
            "fill_form",
            "scroll_page",
            "wait_for_element"
        ]
    
    def execute(self, action: str, **params) -> Dict[str, Any]:
        """
        Execute browser automation action.
        
        Args:
            action: Action name
            **params: Action-specific parameters
        
        Returns:
            Action result dictionary
        """
        # Navigation actions
        if action == "start_browser":
            return self.automation.start_browser()
        
        elif action == "navigate":
            return self.automation.navigate(
                url=params["url"]
            )
        
        elif action == "close_browser":
            self.automation.close()
            return {"success": True, "message": "Browser closed"}
        
        # Content extraction actions
        elif action == "take_screenshot":
            return self.automation.take_screenshot(
                filename=params.get("filename"),
                full_page=params.get("full_page", False),
                highlight_elements=params.get("highlight_elements")
            )
        
        elif action == "extract_text":
            return self.automation.extract_all_text()
        
        # Download actions
        elif action == "download_file":
            return self.automation.download_file(
                download_url=params["url"],
                filename=params.get("filename"),
                create_folder=params.get("folder"),
                wait_timeout=params.get("timeout", 60)
            )
        
        elif action == "create_folder":
            return self.automation.create_folder(
                folder_name=params["name"],
                parent_path=params.get("parent")
            )
        
        # Session management actions
        elif action == "save_session":
            return self.automation.save_session()
        
        elif action == "restore_session":
            return self.automation.restore_session(
                session_data=params.get("session_data")
            )
        
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }


def create_browser_tool(
    headless: bool = False,
    storage_manager: Optional[Any] = None
) -> BrowserAutomationTool:
    """
    Create browser automation tool instance.
    
    Args:
        headless: Run in headless mode
        storage_manager: Optional storage manager
    
    Returns:
        Configured BrowserAutomationTool
    """
    return BrowserAutomationTool(
        headless=headless,
        storage_manager=storage_manager
    )
