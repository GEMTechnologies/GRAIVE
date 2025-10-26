"""Lightweight browser automation fallback when Selenium is unavailable."""

from __future__ import annotations

import base64
import re
import time
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import request as urllib_request
from urllib.parse import unquote, urlparse

try:  # pragma: no cover - exercised when optional dependency exists
    import requests
except ImportError:  # pragma: no cover - fallback path covered in tests
    requests = None  # type: ignore[assignment]


if requests:
    RequestError = requests.RequestException  # type: ignore[attr-defined]
else:
    class RequestError(Exception):
        """Placeholder error used when requests is unavailable."""

        pass


@dataclass
class _LightweightResponse:
    """Simple container for navigation results."""

    url: str
    status_code: int
    headers: Dict[str, str]
    text: str


class HumanBehaviorSimulator:
    """Fallback human behaviour simulator used for parity with Selenium version."""

    @staticmethod
    def human_delay(min_delay: float = 0.05, max_delay: float = 0.2) -> None:
        """Introduce a deterministic short delay to mimic human interaction."""
        time.sleep((min_delay + max_delay) / 2)

    @staticmethod
    def human_type(element: Any, text: str, typing_speed: str = "normal") -> None:
        """No-op placeholder maintained for API compatibility."""
        del element, text, typing_speed

    @staticmethod
    def random_scroll(*_args: Any, **_kwargs: Any) -> None:
        """Scrolling is not applicable in the lightweight mode."""
        return None

    @staticmethod
    def random_mouse_movement(*_args: Any, **_kwargs: Any) -> None:
        """Mouse movement is not supported in the fallback implementation."""
        return None


class StealthBrowser:
    """Placeholder browser that keeps download folder semantics consistent."""

    def __init__(self, headless: bool = True, user_data_dir: Optional[str] = None) -> None:
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.downloads_folder = Path.home() / "Downloads" / "graive_downloads"
        self.downloads_folder.mkdir(parents=True, exist_ok=True)

    def start(self) -> None:
        """There is no real browser to return in lightweight mode."""
        return None

    def close(self) -> None:
        """Nothing to close in lightweight mode."""
        return None


class AdvancedBrowserAutomation:
    """HTTP-based fallback that supports basic navigation and scraping."""

    def __init__(
        self,
        headless: bool = True,
        user_data_dir: Optional[str] = None,
        storage_manager: Optional[Any] = None,
        request_timeout: int = 15,
    ) -> None:
        self.browser = StealthBrowser(headless=headless, user_data_dir=user_data_dir)
        self.session = requests.Session() if requests else None
        self.storage_manager = storage_manager
        self.request_timeout = request_timeout
        self.human_behavior = HumanBehaviorSimulator()

        self._started = False
        self._last_response: Optional[_LightweightResponse] = None
        self._history: List[str] = []

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    def start_browser(self) -> Dict[str, Any]:
        self._started = True
        self.browser.start()
        return {
            "success": True,
            "browser": "lightweight-http",
            "headless": self.browser.headless,
            "stealth": False,
        }

    def close(self) -> None:
        if self.session and requests:
            self.session.close()
        self.browser.close()
        self._started = False
        self._last_response = None

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def navigate(self, url: str) -> Dict[str, Any]:
        if not self._started:
            return {"success": False, "error": "Browser not started"}

        try:
            response = self._load_url(url)
        except (OSError, ValueError, RequestError) as exc:
            return {"success": False, "error": str(exc)}

        self._last_response = response
        self._history.append(response.url)

        if self.storage_manager and response.text:
            try:
                filename = f"page_capture_{len(self._history):04d}.html"
                self.storage_manager.write_file(
                    file_path=filename,
                    content=response.text,
                )
            except Exception:
                # Storage errors should not halt browser usage.
                pass

        return {
            "success": True,
            "url": response.url,
            "status_code": response.status_code,
            "content_length": len(response.text),
            "source": self._source_for_url(response.url),
        }

    def _load_url(self, url: str) -> _LightweightResponse:
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()

        if scheme == "file":
            path = self._resolve_file_url(parsed)
            text = path.read_text(encoding="utf-8")
            return _LightweightResponse(url=url, status_code=200, headers={}, text=text)

        if scheme == "data":
            header, _, data = url.partition(",")
            if ";base64" in header:
                payload = base64.b64decode(data)
                text = payload.decode("utf-8", errors="replace")
            else:
                text = unquote(data)
            return _LightweightResponse(url=url, status_code=200, headers={}, text=text)

        if scheme in {"http", "https"}:
            if self.session and requests:
                response = self.session.get(url, timeout=self.request_timeout)
                response.raise_for_status()
                headers = {k.lower(): v for k, v in response.headers.items()}
                return _LightweightResponse(
                    url=str(response.url),
                    status_code=response.status_code,
                    headers=headers,
                    text=response.text,
                )

            with urllib_request.urlopen(url, timeout=self.request_timeout) as response:  # type: ignore[call-arg]
                data = response.read().decode("utf-8", errors="replace")
                headers = {k.lower(): v for k, v in response.headers.items()}
                status_code = getattr(response, "status", 200)
                return _LightweightResponse(
                    url=url,
                    status_code=status_code,
                    headers=headers,
                    text=data,
                )

        if not scheme:
            # Treat bare paths as files.
            return self._load_url(Path(url).resolve().as_uri())

        raise ValueError(f"Unsupported URL scheme: {scheme}")

    @staticmethod
    def _resolve_file_url(parsed) -> Path:
        path = Path(unquote(parsed.path))
        if parsed.netloc and parsed.netloc != "":
            # Windows paths come through the netloc component.
            drive = unquote(parsed.netloc)
            path = Path(f"{drive}{parsed.path}")
        return path.resolve()

    @staticmethod
    def _source_for_url(url: str) -> str:
        parsed = urlparse(url)
        return parsed.scheme or "file"

    # ------------------------------------------------------------------
    # Extraction utilities
    # ------------------------------------------------------------------
    def take_screenshot(
        self,
        filename: Optional[str] = None,
        full_page: bool = False,
        highlight_elements: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        del filename, full_page, highlight_elements
        return {
            "success": False,
            "error": "Screenshots are unavailable in lightweight mode",
        }

    def extract_all_text(self) -> Dict[str, Any]:
        if not self._last_response:
            return {"success": False, "error": "No page loaded"}

        text, headings, links = self._extract_from_html(self._last_response.text)

        if self.storage_manager:
            try:
                filename = f"extracted_text_{len(self._history):04d}.txt"
                self.storage_manager.write_file(
                    file_path=filename,
                    content=text,
                )
            except Exception:
                pass

        return {
            "success": True,
            "text": text,
            "word_count": len(text.split()),
            "char_count": len(text),
            "headings_count": len(headings),
            "paragraphs_count": text.count("\n"),
            "links_count": len(links),
            "headings": headings[:10],
            "links": links[:20],
        }

    def _extract_from_html(self, html: str) -> Tuple[str, List[str], List[Dict[str, str]]]:
        cleaned = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", html)
        headings = [
            unescape(match.group(2)).strip()
            for match in re.finditer(r"<(h[1-6])[^>]*>(.*?)</\1>", cleaned, flags=re.IGNORECASE | re.DOTALL)
        ]
        links = [
            {"text": unescape(match.group(2)).strip(), "href": match.group(1)}
            for match in re.finditer(
                r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>",
                cleaned,
                flags=re.IGNORECASE | re.DOTALL,
            )
        ]
        text_only = re.sub(r"(?s)<[^>]+>", " ", cleaned)
        text_only = unescape(text_only)
        normalized = re.sub(r"[ \t\r\f\v]+", " ", text_only)
        normalized = re.sub(r"\n\s+", "\n", normalized)
        normalized = normalized.strip()
        return normalized, headings, links

    # ------------------------------------------------------------------
    # Downloads and filesystem helpers
    # ------------------------------------------------------------------
    def download_file(
        self,
        download_url: str,
        filename: Optional[str] = None,
        create_folder: Optional[str] = None,
        wait_timeout: int = 60,
    ) -> Dict[str, Any]:
        del wait_timeout  # Parameter retained for API compatibility.

        if not self._started:
            return {"success": False, "error": "Browser not started"}

        target_dir = self.browser.downloads_folder
        if create_folder:
            target_dir = target_dir / create_folder
            target_dir.mkdir(parents=True, exist_ok=True)

        try:
            path = self._download_to_path(download_url, target_dir, filename)
        except (OSError, ValueError, RequestError) as exc:
            return {"success": False, "error": str(exc)}

        return {
            "success": True,
            "file_path": str(path),
            "filename": path.name,
            "size_bytes": path.stat().st_size,
        }

    def _download_to_path(self, url: str, directory: Path, filename: Optional[str]) -> Path:
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()

        if scheme == "file":
            source_path = self._resolve_file_url(parsed)
            target_name = filename or source_path.name
            target_path = directory / target_name
            target_path.write_bytes(source_path.read_bytes())
            return target_path

        if scheme in {"http", "https"}:
            data: bytes
            if self.session and requests:
                response = self.session.get(url, timeout=self.request_timeout)
                response.raise_for_status()
                data = response.content
            else:
                with urllib_request.urlopen(url, timeout=self.request_timeout) as response:  # type: ignore[call-arg]
                    data = response.read()

            target_name = filename or Path(parsed.path).name or "download.bin"
            target_path = directory / target_name
            target_path.write_bytes(data)
            return target_path

        if not scheme:
            return self._download_to_path(Path(url).resolve().as_uri(), directory, filename)

        raise ValueError(f"Unsupported URL scheme: {scheme}")

    def create_folder(self, folder_name: str, parent_path: Optional[str] = None) -> Dict[str, Any]:
        base = self.browser.downloads_folder
        if parent_path:
            base = base / parent_path
        folder_path = base / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        return {"success": True, "folder_path": str(folder_path), "exists": True}

    # ------------------------------------------------------------------
    # Session utilities
    # ------------------------------------------------------------------
    def save_session(self) -> Dict[str, Any]:
        if not self._started:
            return {"success": False, "error": "Browser not started"}

        if self.session and requests:
            cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        else:
            cookie_dict = {}
        session_data = {
            "cookies": cookie_dict,
            "history": list(self._history),
            "timestamp": time.time(),
            "url": self._last_response.url if self._last_response else None,
        }
        return {"success": True, "cookies_count": len(cookie_dict), "session_data": session_data}

    def restore_session(self, session_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._started:
            return {"success": False, "error": "Browser not started"}

        if not session_data:
            return {"success": False, "error": "No session data provided"}

        if self.session and requests:
            jar = requests.utils.cookiejar_from_dict(session_data.get("cookies", {}))
            self.session.cookies = jar
        self._history = list(session_data.get("history", []))

        url = session_data.get("url")
        if url:
            self.navigate(url)

        return {
            "success": True,
            "restored_cookies": len(session_data.get("cookies", {})),
            "history_length": len(self._history),
        }

    def clear_cookies(self) -> Dict[str, Any]:
        if self.session and requests:
            self.session.cookies.clear()
        return {"success": True}

    def get_cookies(self) -> Dict[str, Any]:
        if self.session and requests:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        else:
            cookies = {}
        return {"success": True, "cookies": cookies, "cookies_count": len(cookies)}

