"""
Web Scraping and Browsing Tool

This tool provides comprehensive web scraping, browsing, and data extraction capabilities.
Supports HTML parsing, JavaScript rendering, PDF extraction, image downloading, citation
generation, and intelligent content extraction from web pages and documents.
"""

import os
from typing import Dict, Any, Optional, List
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class WebScrapingTool(BaseTool):
    """
    Advanced web scraping and browsing tool.
    
    Provides capabilities for visiting websites, extracting content, downloading files,
    parsing HTML/PDF, handling JavaScript-rendered pages, and generating citations.
    Supports academic journals, research papers, and general web content.
    """
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox/web"):
        """
        Initialize the web scraping tool.
        
        Args:
            sandbox_path: Path to store downloaded content
        """
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "images"), exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "pdfs"), exist_ok=True)
        
    @property
    def name(self) -> str:
        return "web_scraping"
    
    @property
    def description(self) -> str:
        return (
            "Scrape websites, extract content, download files (images, PDFs), "
            "parse HTML/PDF documents, handle JavaScript pages, extract data, "
            "generate citations, and visit academic journals and research papers."
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
                        "visit", "extract_text", "extract_data", "download_images",
                        "download_pdf", "parse_pdf", "generate_citation", 
                        "search_page", "get_links", "screenshot"
                    ],
                    "required": True
                },
                "url": {
                    "type": "string",
                    "description": "URL to visit or scrape",
                    "required": True
                },
                "selectors": {
                    "type": "object",
                    "description": "CSS selectors for targeted extraction",
                    "required": False
                },
                "wait_for_js": {
                    "type": "boolean",
                    "description": "Wait for JavaScript to render",
                    "default": False
                },
                "citation_style": {
                    "type": "string",
                    "description": "Citation format",
                    "enum": ["apa", "mla", "chicago", "ieee"],
                    "default": "apa"
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters for web operations."""
        return "action" in parameters and "url" in parameters
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute web scraping operation.
        
        Args:
            parameters: Operation parameters
            
        Returns:
            Operation result with extracted content or file paths
        """
        action = parameters["action"]
        url = parameters["url"]
        
        action_map = {
            "visit": self._visit_page,
            "extract_text": self._extract_text,
            "extract_data": self._extract_data,
            "download_images": self._download_images,
            "download_pdf": self._download_pdf,
            "parse_pdf": self._parse_pdf,
            "generate_citation": self._generate_citation,
            "search_page": self._search_page,
            "get_links": self._get_links,
            "screenshot": self._take_screenshot
        }
        
        handler = action_map.get(action)
        if handler:
            return handler(parameters)
        else:
            return {"error": f"Unknown action: {action}", "success": False}
    
    def _visit_page(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Visit a web page and return basic information."""
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "error": "Required packages not installed. Install: pip install requests beautifulsoup4",
                "success": False
            }
        
        try:
            url = params["url"]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic metadata
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content', '') if meta_description else ''
            
            return {
                "success": True,
                "url": url,
                "title": title_text,
                "description": description,
                "status_code": response.status_code,
                "content_type": response.headers.get('Content-Type', ''),
                "content_length": len(response.content)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _extract_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract clean text content from a web page."""
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            wait_for_js = params.get("wait_for_js", False)
            
            if wait_for_js:
                return self._extract_text_selenium(params)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = '\n'.join(lines)
            
            return {
                "success": True,
                "url": url,
                "text": clean_text,
                "word_count": len(clean_text.split()),
                "char_count": len(clean_text)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _extract_text_selenium(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text from JavaScript-rendered pages using Selenium."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "error": "Selenium not installed. Install: pip install selenium",
                "success": False
            }
        
        try:
            url = params["url"]
            
            # Setup headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Get page source
            page_source = driver.page_source
            driver.quit()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = '\n'.join(lines)
            
            return {
                "success": True,
                "url": url,
                "text": clean_text,
                "rendered_with_js": True,
                "word_count": len(clean_text.split())
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _extract_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data using CSS selectors."""
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            selectors = params.get("selectors", {})
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            extracted_data = {}
            
            for key, selector in selectors.items():
                elements = soup.select(selector)
                if len(elements) == 1:
                    extracted_data[key] = elements[0].get_text(strip=True)
                else:
                    extracted_data[key] = [el.get_text(strip=True) for el in elements]
            
            return {
                "success": True,
                "url": url,
                "data": extracted_data
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _download_images(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Download all images from a web page."""
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin, urlparse
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            max_images = params.get("max_images", 10)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = soup.find_all('img')
            
            downloaded = []
            for idx, img in enumerate(images[:max_images]):
                img_url = img.get('src') or img.get('data-src')
                if not img_url:
                    continue
                
                # Make absolute URL
                img_url = urljoin(url, img_url)
                
                try:
                    img_response = requests.get(img_url, headers=headers, timeout=10)
                    img_response.raise_for_status()
                    
                    # Generate filename
                    filename = f"image_{idx}_{urlparse(img_url).path.split('/')[-1]}"
                    if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        filename += '.jpg'
                    
                    filepath = os.path.join(self.sandbox_path, "images", filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    downloaded.append({
                        "url": img_url,
                        "path": filepath,
                        "alt": img.get('alt', ''),
                        "size": len(img_response.content)
                    })
                    
                except Exception as e:
                    continue
            
            return {
                "success": True,
                "url": url,
                "images_downloaded": len(downloaded),
                "images": downloaded
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _download_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Download PDF file from URL."""
        try:
            import requests
        except ImportError:
            return {
                "error": "Requests not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            
            # Verify it's a PDF
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' not in content_type.lower() and not url.lower().endswith('.pdf'):
                return {
                    "error": "URL does not appear to be a PDF",
                    "success": False
                }
            
            filename = f"document_{hash(url) % 100000}.pdf"
            filepath = os.path.join(self.sandbox_path, "pdfs", filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {
                "success": True,
                "url": url,
                "pdf_path": filepath,
                "size": len(response.content)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _parse_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parse PDF from URL and extract text."""
        # First download the PDF
        download_result = self._download_pdf(params)
        
        if not download_result.get("success"):
            return download_result
        
        try:
            import PyPDF2
        except ImportError:
            return {
                "error": "PyPDF2 not installed. Install: pip install PyPDF2",
                "success": False
            }
        
        try:
            pdf_path = download_result["pdf_path"]
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                num_pages = len(reader.pages)
                text_content = []
                
                for page in reader.pages:
                    text_content.append(page.extract_text())
                
                full_text = '\n\n'.join(text_content)
            
            return {
                "success": True,
                "url": params["url"],
                "pdf_path": pdf_path,
                "num_pages": num_pages,
                "text": full_text,
                "word_count": len(full_text.split())
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _generate_citation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate citation for a web page or article."""
        # First visit the page to get metadata
        visit_result = self._visit_page(params)
        
        if not visit_result.get("success"):
            return visit_result
        
        try:
            import requests
            from bs4 import BeautifulSoup
            from datetime import datetime
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            style = params.get("citation_style", "apa")
            
            # Get additional metadata
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = visit_result.get("title", "Untitled")
            
            # Try to find author
            author_meta = soup.find('meta', attrs={'name': 'author'})
            author = author_meta.get('content', 'Unknown') if author_meta else 'Unknown'
            
            # Try to find publication date
            date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
            pub_date = date_meta.get('content', '') if date_meta else ''
            
            if not pub_date:
                pub_date = datetime.now().strftime("%Y, %B %d")
            
            access_date = datetime.now().strftime("%B %d, %Y")
            
            # Generate citation based on style
            if style == "apa":
                citation = f"{author}. ({pub_date}). {title}. Retrieved {access_date}, from {url}"
            elif style == "mla":
                citation = f'{author}. "{title}." Web. {access_date}. <{url}>.'
            elif style == "chicago":
                citation = f'{author}. "{title}." Accessed {access_date}. {url}.'
            elif style == "ieee":
                citation = f'{author}, "{title}," [Online]. Available: {url}. [Accessed: {access_date}].'
            else:
                citation = f"{author}. {title}. {url} (accessed {access_date})"
            
            return {
                "success": True,
                "url": url,
                "citation": citation,
                "style": style,
                "metadata": {
                    "title": title,
                    "author": author,
                    "publication_date": pub_date,
                    "access_date": access_date
                }
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _search_page(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for specific text within a page."""
        text_result = self._extract_text(params)
        
        if not text_result.get("success"):
            return text_result
        
        try:
            search_term = params.get("search_term", "")
            text = text_result["text"]
            
            # Find all occurrences
            occurrences = []
            lines = text.split('\n')
            
            for idx, line in enumerate(lines):
                if search_term.lower() in line.lower():
                    occurrences.append({
                        "line_number": idx + 1,
                        "content": line,
                        "context": '\n'.join(lines[max(0, idx-1):min(len(lines), idx+2)])
                    })
            
            return {
                "success": True,
                "url": params["url"],
                "search_term": search_term,
                "occurrences": len(occurrences),
                "matches": occurrences
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _get_links(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all links from a page."""
        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            url = params["url"]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                
                links.append({
                    "url": absolute_url,
                    "text": link.get_text(strip=True),
                    "title": link.get('title', '')
                })
            
            return {
                "success": True,
                "url": url,
                "link_count": len(links),
                "links": links
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _take_screenshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Take screenshot of a web page."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except ImportError:
            return {
                "error": "Selenium not installed. Install: pip install selenium",
                "success": False
            }
        
        try:
            url = params["url"]
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Wait for page load
            driver.implicitly_wait(5)
            
            filename = f"screenshot_{hash(url) % 100000}.png"
            filepath = os.path.join(self.sandbox_path, "images", filename)
            
            driver.save_screenshot(filepath)
            driver.quit()
            
            return {
                "success": True,
                "url": url,
                "screenshot_path": filepath
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
