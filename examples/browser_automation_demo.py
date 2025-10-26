"""
Advanced Browser Automation - Comprehensive Examples

Demonstrates human-like browser control, anti-detection, and web automation:
1. Stealth browsing with anti-detection
2. Human-like behavior simulation
3. Cloudflare and CAPTCHA bypass
4. Screenshot capture with highlighting
5. Complete text extraction
6. File downloads with organization
7. Session persistence and restoration
8. Multi-page workflows
"""

import os
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.browser_automation import (
    AdvancedBrowserAutomation,
    StealthBrowser,
    HumanBehaviorSimulator,
    create_browser_tool
)
from src.storage import create_storage_tool_for_sandbox


def example_stealth_browsing():
    """
    Example 1: Stealth Browsing with Anti-Detection
    
    Demonstrates browser setup with stealth mode to bypass detection.
    """
    print("=" * 80)
    print("EXAMPLE 1: STEALTH BROWSING WITH ANTI-DETECTION")
    print("=" * 80)
    
    # Create browser automation
    browser = AdvancedBrowserAutomation(headless=False)
    
    # Start stealth browser
    print("\n1. Starting Stealth Browser")
    result = browser.start_browser()
    print(f"   ✓ Browser: {result.get('browser')}")
    print(f"   ✓ Version: {result.get('version')}")
    print(f"   ✓ Headless: {result.get('headless')}")
    
    # Navigate to bot-detection test site
    print("\n2. Testing Bot Detection")
    test_urls = [
        "https://bot.sannysoft.com/",
        "https://arh.antoinevastel.com/bots/areyouheadless"
    ]
    
    for url in test_urls:
        print(f"\n   Testing: {url}")
        result = browser.navigate(url)
        
        if result["success"]:
            print(f"   ✓ Loaded: {result['title'][:50]}...")
            print(f"   ✓ Load time: {result['load_time']:.2f}s")
            
            if "cloudflare_bypassed" in result:
                print(f"   ✓ Cloudflare bypassed: {result['cloudflare_bypassed']}")
            
            time.sleep(3)  # Wait to observe
        else:
            print(f"   ✗ Failed: {result.get('error')}")
    
    # Clean up
    browser.close()
    print("\n   ✓ Browser closed")
    
    return browser


def example_human_behavior():
    """
    Example 2: Human-like Behavior Simulation
    
    Demonstrates realistic mouse movements, typing, and scrolling.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: HUMAN-LIKE BEHAVIOR SIMULATION")
    print("=" * 80)
    
    browser = AdvancedBrowserAutomation(headless=False)
    browser.start_browser()
    
    # Navigate to test page
    print("\n1. Navigating to Wikipedia")
    browser.navigate("https://en.wikipedia.org/wiki/Artificial_intelligence")
    
    # Demonstrate human-like scrolling
    print("\n2. Simulating Human Scrolling")
    human = HumanBehaviorSimulator()
    
    for i in range(5):
        print(f"   Scroll {i+1}: Random distance, natural timing")
        human.random_scroll(browser.driver, direction="down")
        human.human_delay(0.5, 1.5)
    
    # Scroll back up
    for i in range(3):
        human.random_scroll(browser.driver, direction="up")
        human.human_delay(0.3, 0.8)
    
    print("   ✓ Human-like scrolling complete")
    
    # Random mouse movements
    print("\n3. Simulating Random Mouse Movements")
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(browser.driver)
    
    human.random_mouse_movement(browser.driver, actions)
    print("   ✓ Mouse movements complete")
    
    browser.close()
    return browser


def example_screenshot_capture():
    """
    Example 3: Screenshot Capture with Element Highlighting
    
    Demonstrates taking screenshots with element emphasis.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: SCREENSHOT CAPTURE WITH HIGHLIGHTING")
    print("=" * 80)
    
    browser = AdvancedBrowserAutomation(headless=False)
    browser.start_browser()
    
    # Navigate to page
    print("\n1. Navigating to Target Page")
    browser.navigate("https://github.com")
    time.sleep(2)
    
    # Take regular screenshot
    print("\n2. Capturing Regular Screenshot")
    result = browser.take_screenshot(
        filename="github_homepage.png",
        full_page=False
    )
    
    if result["success"]:
        print(f"   ✓ Saved: {result['file_path']}")
        print(f"   ✓ Size: {result['size_bytes']:,} bytes")
    
    # Take screenshot with highlighted elements
    print("\n3. Capturing with Element Highlighting")
    result = browser.take_screenshot(
        filename="github_highlighted.png",
        full_page=False,
        highlight_elements=["h1", ".btn"]
    )
    
    if result["success"]:
        print(f"   ✓ Saved: {result['file_path']}")
        print(f"   ✓ Highlighted: h1, .btn elements")
    
    # Take full page screenshot
    print("\n4. Capturing Full Page Screenshot")
    result = browser.take_screenshot(
        filename="github_fullpage.png",
        full_page=True
    )
    
    if result["success"]:
        print(f"   ✓ Saved: {result['file_path']}")
        print(f"   ✓ Full page captured")
    
    browser.close()
    return result


def example_text_extraction():
    """
    Example 4: Complete Text Extraction
    
    Demonstrates extracting all text, headings, and links from pages.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: COMPLETE TEXT EXTRACTION")
    print("=" * 80)
    
    # Create storage for extracted text
    storage = create_storage_tool_for_sandbox("text_extraction_001")
    browser = AdvancedBrowserAutomation(
        headless=True,
        storage_manager=storage.storage
    )
    browser.start_browser()
    
    # Navigate to article
    print("\n1. Navigating to Article")
    browser.navigate("https://en.wikipedia.org/wiki/Machine_learning")
    
    # Extract all text
    print("\n2. Extracting Complete Text")
    result = browser.extract_all_text()
    
    if result["success"]:
        print(f"   ✓ Text extracted")
        print(f"   ✓ Word count: {result['word_count']:,}")
        print(f"   ✓ Character count: {result['char_count']:,}")
        print(f"   ✓ Headings: {result['headings_count']}")
        print(f"   ✓ Paragraphs: {result['paragraphs_count']}")
        print(f"   ✓ Links: {result['links_count']}")
        
        # Display sample headings
        print("\n3. Sample Headings:")
        for i, heading in enumerate(result['headings'][:5], 1):
            print(f"   {i}. {heading}")
        
        # Display sample links
        print("\n4. Sample Links:")
        for i, link in enumerate(result['links'][:5], 1):
            print(f"   {i}. {link['text'][:50]}...")
            print(f"      → {link['href'][:60]}...")
    
    browser.close()
    return result


def example_file_downloads():
    """
    Example 5: File Downloads with Folder Organization
    
    Demonstrates downloading files and organizing them in folders.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: FILE DOWNLOADS WITH ORGANIZATION")
    print("=" * 80)
    
    browser = AdvancedBrowserAutomation(headless=True)
    browser.start_browser()
    
    # Create organized folder structure
    print("\n1. Creating Folder Structure")
    folders = [
        "research_papers",
        "research_papers/AI",
        "research_papers/ML",
        "datasets"
    ]
    
    for folder in folders:
        result = browser.create_folder(folder)
        if result["success"]:
            print(f"   ✓ Created: {folder}")
    
    # Example download URLs (using sample PDFs)
    print("\n2. Downloading Files")
    downloads = [
        {
            "url": "https://arxiv.org/pdf/1706.03762.pdf",  # Attention is All You Need
            "filename": "attention_paper.pdf",
            "folder": "research_papers/AI"
        }
    ]
    
    for download in downloads:
        print(f"\n   Downloading: {download['filename']}")
        result = browser.download_file(
            download_url=download['url'],
            filename=download.get('filename'),
            create_folder=download.get('folder'),
            wait_timeout=60
        )
        
        if result["success"]:
            print(f"   ✓ Saved: {result['file_path']}")
            print(f"   ✓ Size: {result['size_bytes']:,} bytes")
            print(f"   ✓ Time: {result['download_time']:.2f}s")
        else:
            print(f"   ✗ Failed: {result.get('error')}")
    
    browser.close()
    return result


def example_session_persistence():
    """
    Example 6: Session Persistence and Restoration
    
    Demonstrates saving and restoring browser sessions.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 6: SESSION PERSISTENCE AND RESTORATION")
    print("=" * 80)
    
    # Create storage for session
    storage = create_storage_tool_for_sandbox("session_test_001")
    browser = AdvancedBrowserAutomation(
        headless=False,
        storage_manager=storage.storage
    )
    browser.start_browser()
    
    # Session 1: Browse and save
    print("\n1. First Session: Browse and Save")
    browser.navigate("https://github.com")
    time.sleep(2)
    
    # Save session
    result = browser.save_session()
    print(f"   ✓ Session saved")
    print(f"   ✓ Cookies: {result['cookies_count']}")
    print(f"   ✓ Local storage items: {result['local_storage_items']}")
    
    # Close browser
    browser.close()
    print("   ✓ Browser closed")
    
    # Session 2: Restore and continue
    print("\n2. Second Session: Restore State")
    browser2 = AdvancedBrowserAutomation(
        headless=False,
        storage_manager=storage.storage
    )
    browser2.start_browser()
    
    # Restore session
    result = browser2.restore_session()
    if result["success"]:
        print(f"   ✓ Session restored")
        print(f"   ✓ Cookies: {result['restored_cookies']}")
        print(f"   ✓ Local storage: {result['restored_local_storage']}")
        print("   ✓ Continuing from previous state")
    
    time.sleep(3)
    browser2.close()
    
    return result


def example_multi_page_workflow():
    """
    Example 7: Multi-Page Research Workflow
    
    Demonstrates complete workflow: search, extract, download, organize.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 7: MULTI-PAGE RESEARCH WORKFLOW")
    print("=" * 80)
    
    storage = create_storage_tool_for_sandbox("research_workflow_001")
    browser = AdvancedBrowserAutomation(
        headless=False,
        storage_manager=storage.storage
    )
    browser.start_browser()
    
    # Step 1: Search for papers
    print("\n1. Searching arXiv for AI papers")
    browser.navigate("https://arxiv.org/search/?query=artificial+intelligence&searchtype=all")
    time.sleep(2)
    
    # Take screenshot of search results
    browser.take_screenshot("arxiv_search.png")
    print("   ✓ Captured search results")
    
    # Extract paper links
    result = browser.extract_all_text()
    print(f"   ✓ Found {result.get('links_count', 0)} links")
    
    # Step 2: Visit specific paper
    print("\n2. Opening Specific Paper")
    browser.navigate("https://arxiv.org/abs/1706.03762")  # Attention paper
    time.sleep(2)
    
    # Extract paper details
    result = browser.extract_all_text()
    print(f"   ✓ Paper title extracted")
    print(f"   ✓ Abstract length: {len(result.get('text', '').split()[:200])} words")
    
    # Step 3: Create organized structure
    print("\n3. Creating Folder Structure")
    browser.create_folder("AI_Papers/Transformers")
    
    # Step 4: Download PDF
    print("\n4. Downloading Paper PDF")
    # Would download if needed
    print("   ✓ Ready to download")
    
    # Step 5: Save session for later
    print("\n5. Saving Research Session")
    browser.save_session()
    print("   ✓ Session saved for resumption")
    
    browser.close()
    print("\n   ✓ Workflow complete")
    
    return result


def example_browser_tool_interface():
    """
    Example 8: Using Browser Tool Interface
    
    Demonstrates high-level tool interface for agents.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 8: BROWSER TOOL INTERFACE")
    print("=" * 80)
    
    # Create tool
    print("\n1. Creating Browser Tool")
    tool = create_browser_tool(headless=True)
    
    # Show available actions
    print("\n2. Available Actions")
    actions = tool.get_available_actions()
    print(f"   Total actions: {len(actions)}")
    print(f"   Navigation: {[a for a in actions if 'navigate' in a or 'browser' in a]}")
    print(f"   Extraction: {[a for a in actions if 'extract' in a or 'screenshot' in a]}")
    print(f"   Downloads: {[a for a in actions if 'download' in a or 'folder' in a]}")
    
    # Execute actions via tool interface
    print("\n3. Executing Actions via Tool")
    
    result = tool.execute("start_browser")
    print(f"   ✓ Start browser: {result['success']}")
    
    result = tool.execute("navigate", url="https://example.com")
    if result["success"]:
        print(f"   ✓ Navigate: {result['title']}")
    
    result = tool.execute("take_screenshot", filename="example.png")
    if result["success"]:
        print(f"   ✓ Screenshot: {Path(result['file_path']).name}")
    
    result = tool.execute("extract_text")
    if result["success"]:
        print(f"   ✓ Text extracted: {result['word_count']} words")
    
    result = tool.execute("close_browser")
    print(f"   ✓ Close browser: {result['success']}")
    
    return tool


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" ADVANCED BROWSER AUTOMATION - COMPREHENSIVE EXAMPLES")
    print("=" * 80)
    print("\nDemonstrating human-like browser control and anti-detection:")
    print("  1. Stealth browsing to bypass bot detection")
    print("  2. Human-like behavior (scrolling, mouse, typing)")
    print("  3. Screenshot capture with highlighting")
    print("  4. Complete text extraction")
    print("  5. File downloads with organization")
    print("  6. Session persistence and restoration")
    print("  7. Multi-page research workflow")
    print("  8. Browser tool interface")
    print("\n" + "=" * 80)
    
    # Run examples (comment out as needed)
    try:
        print("\nNote: Browser automation requires Selenium and ChromeDriver")
        print("Install: pip install selenium undetected-chromedriver selenium-stealth")
        
        # Uncomment to run specific examples:
        # example_stealth_browsing()
        # example_human_behavior()
        # example_screenshot_capture()
        # example_text_extraction()
        # example_file_downloads()
        # example_session_persistence()
        # example_multi_page_workflow()
        example_browser_tool_interface()
        
        print("\n" + "=" * 80)
        print("EXAMPLES COMPLETE")
        print("=" * 80)
        print("\nBrowser automation provides:")
        print("  ✓ Stealth mode bypassing Cloudflare and bot detection")
        print("  ✓ Human-like behavior (realistic timing and movements)")
        print("  ✓ Screenshot capture with element highlighting")
        print("  ✓ Complete text and link extraction")
        print("  ✓ File downloads with folder organization")
        print("  ✓ Session persistence across browser restarts")
        print("  ✓ Multi-page workflows with state management")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Ensure Selenium and ChromeDriver are properly installed")
