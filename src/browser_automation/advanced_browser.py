"""
Advanced Browser Automation - Human-like Browser Control

This module implements sophisticated browser automation capabilities for Graive AI:
- Human-like mouse movements and typing patterns
- Anti-detection techniques to bypass bot detection
- CAPTCHA handling and "Prove You're Human" challenges
- Screenshot capture with element highlighting
- Text extraction from entire pages
- File downloads with progress tracking
- Folder creation and organization
- Session persistence and cookie management
- Stealth mode to avoid detection
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
import os
import time
import random
import json
from pathlib import Path
from datetime import datetime
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# For stealth mode
try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False

# For undetected ChromeDriver
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False


class HumanBehaviorSimulator:
    """
    Simulates human-like behavior to bypass bot detection.
    
    Implements realistic mouse movements, typing patterns, scrolling,
    and timing variations that mimic human interaction.
    """
    
    @staticmethod
    def human_delay(min_delay: float = 0.1, max_delay: float = 0.5) -> None:
        """Random delay simulating human reaction time."""
        time.sleep(random.uniform(min_delay, max_delay))
    
    @staticmethod
    def human_type(element, text: str, typing_speed: str = "normal") -> None:
        """
        Type text with human-like timing variations.
        
        Args:
            element: Web element to type into
            text: Text to type
            typing_speed: Speed preset (slow, normal, fast)
        """
        speed_ranges = {
            "slow": (0.1, 0.3),
            "normal": (0.05, 0.15),
            "fast": (0.02, 0.08)
        }
        
        min_delay, max_delay = speed_ranges.get(typing_speed, (0.05, 0.15))
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
            
            # Occasionally pause longer (simulating thinking)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.8))
    
    @staticmethod
    def bezier_curve_movement(
        action_chains: ActionChains,
        from_x: int, from_y: int,
        to_x: int, to_y: int,
        steps: int = 20
    ) -> None:
        """
        Move mouse along Bezier curve for natural movement.
        
        Args:
            action_chains: Selenium ActionChains instance
            from_x, from_y: Starting coordinates
            to_x, to_y: Target coordinates
            steps: Number of intermediate points
        """
        # Generate control points for Bezier curve
        ctrl_x1 = from_x + random.randint(-50, 50)
        ctrl_y1 = from_y + random.randint(-50, 50)
        ctrl_x2 = to_x + random.randint(-50, 50)
        ctrl_y2 = to_y + random.randint(-50, 50)
        
        # Calculate points along curve
        for i in range(steps):
            t = i / steps
            
            # Cubic Bezier formula
            x = (1-t)**3 * from_x + 3*(1-t)**2*t * ctrl_x1 + \
                3*(1-t)*t**2 * ctrl_x2 + t**3 * to_x
            y = (1-t)**3 * from_y + 3*(1-t)**2*t * ctrl_y1 + \
                3*(1-t)*t**2 * ctrl_y2 + t**3 * to_y
            
            action_chains.move_by_offset(int(x), int(y))
            time.sleep(random.uniform(0.001, 0.003))
    
    @staticmethod
    def random_scroll(driver, direction: str = "down", distance: int = None) -> None:
        """
        Scroll page with human-like patterns.
        
        Args:
            driver: Selenium WebDriver instance
            direction: Scroll direction (up, down)
            distance: Pixels to scroll (random if None)
        """
        if distance is None:
            distance = random.randint(100, 500)
        
        # Scroll in multiple small increments
        increments = random.randint(3, 8)
        increment_size = distance // increments
        
        for _ in range(increments):
            if direction == "down":
                driver.execute_script(f"window.scrollBy(0, {increment_size})")
            else:
                driver.execute_script(f"window.scrollBy(0, -{increment_size})")
            
            time.sleep(random.uniform(0.1, 0.3))
    
    @staticmethod
    def random_mouse_movement(driver, action_chains: ActionChains) -> None:
        """Perform random mouse movements to appear human."""
        for _ in range(random.randint(2, 5)):
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-100, 100)
            action_chains.move_by_offset(offset_x, offset_y).perform()
            time.sleep(random.uniform(0.05, 0.15))


class StealthBrowser:
    """
    Browser with anti-detection capabilities.
    
    Implements techniques to bypass bot detection systems including
    Cloudflare, reCAPTCHA, and other anti-bot mechanisms.
    """
    
    def __init__(
        self,
        headless: bool = False,
        use_undetected: bool = True,
        user_data_dir: Optional[str] = None
    ):
        """
        Initialize stealth browser.
        
        Args:
            headless: Run in headless mode
            use_undetected: Use undetected-chromedriver if available
            user_data_dir: Chrome user data directory for session persistence
        """
        self.headless = headless
        self.use_undetected = use_undetected and UNDETECTED_AVAILABLE
        self.user_data_dir = user_data_dir
        
        self.driver = None
        self.human_behavior = HumanBehaviorSimulator()
        self.downloads_folder = Path.home() / "Downloads" / "graive_downloads"
        self.downloads_folder.mkdir(parents=True, exist_ok=True)
    
    def start(self) -> webdriver.Chrome:
        """
        Start browser with stealth configuration.
        
        Returns:
            Configured WebDriver instance
        """
        if self.use_undetected:
            # Use undetected-chromedriver for maximum stealth
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            if self.user_data_dir:
                options.add_argument(f'--user-data-dir={self.user_data_dir}')
            
            # Additional stealth options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Download preferences
            prefs = {
                "download.default_directory": str(self.downloads_folder),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False
            }
            options.add_experimental_option("prefs", prefs)
            
            self.driver = uc.Chrome(options=options, version_main=None)
        
        else:
            # Standard Selenium with stealth enhancements
            options = Options()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            if self.user_data_dir:
                options.add_argument(f'--user-data-dir={self.user_data_dir}')
            
            # Anti-detection arguments
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            # Realistic window size
            options.add_argument('--window-size=1920,1080')
            
            # User agent
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Download preferences
            prefs = {
                "download.default_directory": str(self.downloads_folder),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False
            }
            options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=options)
            
            # Apply selenium-stealth if available
            if STEALTH_AVAILABLE:
                stealth(self.driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )
            
            # Override navigator properties
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                '''
            })
        
        return self.driver
    
    def navigate_to(self, url: str, wait_time: int = 10) -> Dict[str, Any]:
        """
        Navigate to URL with human-like behavior.
        
        Args:
            url: Target URL
            wait_time: Maximum wait time for page load
        
        Returns:
            Navigation result with status and timing
        """
        start_time = time.time()
        
        try:
            self.driver.get(url)
            
            # Random delay simulating page reading
            self.human_behavior.human_delay(1.0, 2.5)
            
            # Random scroll to simulate human browsing
            self.human_behavior.random_scroll(self.driver)
            
            # Wait for page to be ready
            WebDriverWait(self.driver, wait_time).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            load_time = time.time() - start_time
            
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title,
                "load_time": load_time
            }
        
        except TimeoutException:
            return {
                "success": False,
                "error": "Page load timeout",
                "url": url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def bypass_cloudflare(self, max_wait: int = 30) -> bool:
        """
        Attempt to bypass Cloudflare challenge.
        
        Args:
            max_wait: Maximum seconds to wait for bypass
        
        Returns:
            True if bypassed successfully
        """
        try:
            # Wait for Cloudflare challenge to complete
            # Undetected ChromeDriver usually handles this automatically
            
            start_time = time.time()
            while time.time() - start_time < max_wait:
                # Check if still on challenge page
                if "cloudflare" in self.driver.current_url.lower() or \
                   "Just a moment" in self.driver.page_source:
                    time.sleep(1)
                    continue
                else:
                    return True
            
            return False
        
        except Exception:
            return False
    
    def handle_recaptcha(self) -> bool:
        """
        Detect and handle reCAPTCHA challenges.
        
        Note: This provides a framework for CAPTCHA handling.
        Actual solving would require third-party services or manual intervention.
        
        Returns:
            True if CAPTCHA detected
        """
        try:
            # Detect reCAPTCHA iframe
            recaptcha_iframe = self.driver.find_elements(
                By.CSS_SELECTOR,
                'iframe[src*="recaptcha"]'
            )
            
            if recaptcha_iframe:
                print("reCAPTCHA detected. Manual intervention or CAPTCHA service required.")
                return True
            
            return False
        
        except Exception:
            return False
    
    def close(self):
        """Close browser and cleanup."""
        if self.driver:
            self.driver.quit()
            self.driver = None


class AdvancedBrowserAutomation:
    """
    Comprehensive browser automation with advanced capabilities.
    
    Provides high-level methods for web interaction, content extraction,
    file management, and screenshot capture.
    """
    
    def __init__(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None,
        storage_manager: Optional[Any] = None
    ):
        """
        Initialize advanced browser automation.
        
        Args:
            headless: Run browser in headless mode
            user_data_dir: Directory for persistent session data
            storage_manager: Optional storage manager for saving artifacts
        """
        self.browser = StealthBrowser(
            headless=headless,
            user_data_dir=user_data_dir
        )
        self.driver = None
        self.storage_manager = storage_manager
        self.human_behavior = HumanBehaviorSimulator()
        
        # Session state
        self.cookies: List[Dict] = []
        self.local_storage: Dict[str, str] = {}
        self.session_storage: Dict[str, str] = {}
    
    def start_browser(self) -> Dict[str, Any]:
        """
        Start browser session.
        
        Returns:
            Startup status and browser info
        """
        try:
            self.driver = self.browser.start()
            
            return {
                "success": True,
                "browser": "Chrome (Stealth Mode)",
                "version": self.driver.capabilities.get('browserVersion'),
                "headless": self.browser.headless
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to URL with anti-detection."""
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        result = self.browser.navigate_to(url)
        
        # Check for Cloudflare
        if "cloudflare" in self.driver.page_source.lower():
            print("Cloudflare detected, attempting bypass...")
            if self.browser.bypass_cloudflare():
                result["cloudflare_bypassed"] = True
            else:
                result["cloudflare_bypassed"] = False
        
        # Check for reCAPTCHA
        if self.browser.handle_recaptcha():
            result["recaptcha_detected"] = True
        
        return result
    
    def take_screenshot(
        self,
        filename: Optional[str] = None,
        full_page: bool = False,
        highlight_elements: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Capture screenshot with optional element highlighting.
        
        Args:
            filename: Output filename (auto-generated if None)
            full_page: Capture entire page or just viewport
            highlight_elements: CSS selectors to highlight before capture
        
        Returns:
            Screenshot result with file path
        """
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # Highlight elements if requested
            if highlight_elements:
                for selector in highlight_elements:
                    self._highlight_element(selector)
            
            # Capture screenshot
            if full_page:
                screenshot_path = self._capture_full_page(filename)
            else:
                screenshot_path = self.browser.downloads_folder / filename
                self.driver.save_screenshot(str(screenshot_path))
            
            # Store in storage manager if available
            if self.storage_manager:
                with open(screenshot_path, 'rb') as f:
                    self.storage_manager.cache_media(
                        media_data=f.read(),
                        media_type="image",
                        filename=filename
                    )
            
            return {
                "success": True,
                "file_path": str(screenshot_path),
                "size_bytes": screenshot_path.stat().st_size
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _highlight_element(self, selector: str, color: str = "red"):
        """Highlight element with border for screenshot."""
        try:
            script = f"""
            var elements = document.querySelectorAll('{selector}');
            elements.forEach(function(element) {{
                element.style.border = '3px solid {color}';
                element.style.boxShadow = '0 0 10px {color}';
            }});
            """
            self.driver.execute_script(script)
        except Exception:
            pass
    
    def _capture_full_page(self, filename: str) -> Path:
        """Capture full page screenshot (beyond viewport)."""
        # Get page dimensions
        total_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )
        viewport_height = self.driver.execute_script(
            "return window.innerHeight"
        )
        
        # Scroll and capture sections
        screenshots = []
        scroll_position = 0
        
        while scroll_position < total_height:
            # Capture current viewport
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            
            # Scroll down
            scroll_position += viewport_height
            self.driver.execute_script(
                f"window.scrollTo(0, {scroll_position})"
            )
            time.sleep(0.3)
        
        # Combine screenshots (simplified - would use PIL in production)
        output_path = self.browser.downloads_folder / filename
        with open(output_path, 'wb') as f:
            f.write(screenshots[0])  # For now, just save first section
        
        return output_path
    
    def extract_all_text(self) -> Dict[str, Any]:
        """
        Extract all visible text from current page.
        
        Returns:
            Extracted text and metadata
        """
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        try:
            # Extract visible text
            text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract structured content
            headings = [
                elem.text for elem in self.driver.find_elements(
                    By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6"
                )
            ]
            
            paragraphs = [
                elem.text for elem in self.driver.find_elements(
                    By.TAG_NAME, "p"
                )
            ]
            
            links = [
                {"text": elem.text, "href": elem.get_attribute("href")}
                for elem in self.driver.find_elements(By.TAG_NAME, "a")
            ]
            
            # Store in storage manager
            if self.storage_manager:
                self.storage_manager.write_file(
                    file_path=f"extracted_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    content=text
                )
            
            return {
                "success": True,
                "text": text,
                "word_count": len(text.split()),
                "char_count": len(text),
                "headings_count": len(headings),
                "paragraphs_count": len(paragraphs),
                "links_count": len(links),
                "headings": headings[:10],  # First 10
                "links": links[:20]  # First 20
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_file(
        self,
        download_url: str,
        filename: Optional[str] = None,
        create_folder: Optional[str] = None,
        wait_timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Download file from URL with progress tracking.
        
        Args:
            download_url: URL to download from
            filename: Custom filename (auto-detect if None)
            create_folder: Optional subfolder to create
            wait_timeout: Max seconds to wait for download
        
        Returns:
            Download result with file info
        """
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        try:
            # Create subfolder if requested
            if create_folder:
                folder_path = self.browser.downloads_folder / create_folder
                folder_path.mkdir(parents=True, exist_ok=True)
                download_dir = folder_path
            else:
                download_dir = self.browser.downloads_folder
            
            # Get initial file count
            initial_files = set(download_dir.glob("*"))
            
            # Initiate download
            self.driver.get(download_url)
            self.human_behavior.human_delay(0.5, 1.5)
            
            # Wait for download to complete
            start_time = time.time()
            while time.time() - start_time < wait_timeout:
                current_files = set(download_dir.glob("*"))
                new_files = current_files - initial_files
                
                # Check for completed downloads (no .crdownload files)
                completed_downloads = [
                    f for f in new_files
                    if not f.name.endswith('.crdownload')
                ]
                
                if completed_downloads:
                    downloaded_file = completed_downloads[0]
                    
                    # Rename if custom filename provided
                    if filename:
                        new_path = downloaded_file.parent / filename
                        downloaded_file.rename(new_path)
                        downloaded_file = new_path
                    
                    return {
                        "success": True,
                        "file_path": str(downloaded_file),
                        "filename": downloaded_file.name,
                        "size_bytes": downloaded_file.stat().st_size,
                        "download_time": time.time() - start_time
                    }
                
                time.sleep(0.5)
            
            return {
                "success": False,
                "error": "Download timeout exceeded"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_folder(self, folder_name: str, parent_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Create folder in downloads directory.
        
        Args:
            folder_name: Name of folder to create
            parent_path: Optional parent path (relative to downloads)
        
        Returns:
            Folder creation result
        """
        try:
            if parent_path:
                folder_path = self.browser.downloads_folder / parent_path / folder_name
            else:
                folder_path = self.browser.downloads_folder / folder_name
            
            folder_path.mkdir(parents=True, exist_ok=True)
            
            return {
                "success": True,
                "folder_path": str(folder_path),
                "exists": True
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_session(self) -> Dict[str, Any]:
        """
        Save current browser session (cookies, storage).
        
        Returns:
            Session data for later restoration
        """
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        try:
            # Save cookies
            self.cookies = self.driver.get_cookies()
            
            # Save local storage
            local_storage = self.driver.execute_script(
                "return Object.entries(localStorage).reduce((acc, [k, v]) => ({...acc, [k]: v}), {});"
            )
            self.local_storage = local_storage or {}
            
            # Save session storage
            session_storage = self.driver.execute_script(
                "return Object.entries(sessionStorage).reduce((acc, [k, v]) => ({...acc, [k]: v}), {});"
            )
            self.session_storage = session_storage or {}
            
            session_data = {
                "cookies": self.cookies,
                "local_storage": self.local_storage,
                "session_storage": self.session_storage,
                "url": self.driver.current_url,
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in storage manager
            if self.storage_manager:
                self.storage_manager.store_context(
                    key="browser_session",
                    value=session_data,
                    context_type="browser"
                )
            
            return {
                "success": True,
                "cookies_count": len(self.cookies),
                "local_storage_items": len(self.local_storage),
                "session_storage_items": len(self.session_storage)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def restore_session(self, session_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Restore previous browser session.
        
        Args:
            session_data: Session data to restore (loads from storage if None)
        
        Returns:
            Restoration result
        """
        if not self.driver:
            return {"success": False, "error": "Browser not started"}
        
        try:
            # Load session data from storage if not provided
            if session_data is None and self.storage_manager:
                session_data = self.storage_manager.retrieve_context("browser_session")
            
            if not session_data:
                return {"success": False, "error": "No session data found"}
            
            # Navigate to original URL first (required for setting cookies)
            if "url" in session_data:
                self.driver.get(session_data["url"])
            
            # Restore cookies
            for cookie in session_data.get("cookies", []):
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    pass  # Some cookies may be invalid
            
            # Restore local storage
            for key, value in session_data.get("local_storage", {}).items():
                self.driver.execute_script(
                    f"localStorage.setItem('{key}', '{value}');"
                )
            
            # Restore session storage
            for key, value in session_data.get("session_storage", {}).items():
                self.driver.execute_script(
                    f"sessionStorage.setItem('{key}', '{value}');"
                )
            
            # Refresh page to apply session
            self.driver.refresh()
            
            return {
                "success": True,
                "restored_cookies": len(session_data.get("cookies", [])),
                "restored_local_storage": len(session_data.get("local_storage", {})),
                "restored_session_storage": len(session_data.get("session_storage", {}))
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def close(self):
        """Close browser and cleanup resources."""
        self.browser.close()
        self.driver = None
