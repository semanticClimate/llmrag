"""
Web Downloader Component

Downloads IPCC chapters from URLs using headless browsers.
Supports Selenium for JavaScript-heavy sites.
"""

import logging
import time
from typing import Dict, Any
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class WebDownloader:
    """
    Downloads web content using various methods (Selenium, requests).
    
    Supports headless browsers for JavaScript-heavy sites like IPCC.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def download(self, url: str) -> str:
        """
        Download content from a URL.
        
        Args:
            url: The URL to download from
            
        Returns:
            HTML content as string
        """
        method = self.config.get('method', 'selenium_headless')
        
        if method == 'selenium_headless':
            return self._download_with_selenium(url)
        elif method == 'requests':
            return self._download_with_requests(url)
        else:
            raise ValueError(f"Unknown download method: {method}")
    
    def _download_with_selenium(self, url: str) -> str:
        """Download using Selenium headless browser."""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not available. Install with: pip install selenium")
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=options)
        
        try:
            self.logger.info(f"Downloading with Selenium: {url}")
            driver.get(url)
            
            # Wait for page to load
            wait_time = self.config.get('wait_time', 5)
            time.sleep(wait_time)
            
            # Wait for main content to be present
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except Exception as e:
                self.logger.warning(f"Timeout waiting for page load: {e}")
            
            # Get the page source
            html_content = driver.page_source
            
            return html_content
            
        finally:
            driver.quit()
    
    def _download_with_requests(self, url: str) -> str:
        """Download using requests library."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests not available. Install with: pip install requests")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.text 