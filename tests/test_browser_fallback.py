"""Tests for the lightweight browser fallback implementation."""

from pathlib import Path

import pytest

from src.browser_automation import AdvancedBrowserAutomation, ADVANCED_BROWSER_AVAILABLE


@pytest.mark.skipif(ADVANCED_BROWSER_AVAILABLE, reason="Fallback is only exercised when Selenium is unavailable")
def test_fallback_navigates_local_file(tmp_path: Path) -> None:
    browser = AdvancedBrowserAutomation(headless=True)
    start_result = browser.start_browser()
    assert start_result["success"] is True

    html_file = tmp_path / "example.html"
    html_file.write_text("<html><body><h1>Hello</h1><p>World!</p></body></html>", encoding="utf-8")

    result = browser.navigate(html_file.resolve().as_uri())
    assert result["success"] is True
    assert result["source"] == "file"

    text_result = browser.extract_all_text()
    assert text_result["success"] is True
    assert "Hello" in text_result["text"]
    assert text_result["headings_count"] == 1
    assert text_result["links_count"] == 0

    browser.close()
