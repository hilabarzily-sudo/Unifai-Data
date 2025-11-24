"""
Civitai Web Scraper
Method 2: HTML scraping with Selenium
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from typing import Dict, List, Optional
import time
from tqdm import tqdm
import json
import os
import re
from config import SCRAPING_CONFIG, COMMON_CONFIG, USER_AGENT


class CivitaiWebScraper:
    """Scraper using HTML parsing"""

    def __init__(self):
        self.base_url = "https://civitai.com"
        self.use_selenium = SCRAPING_CONFIG["use_selenium"]
        self.driver = None

        if self.use_selenium:
            self._setup_selenium()

    def _setup_selenium(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={USER_AGENT}')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Selenium initialized")
        except Exception as e:
            print(f"⚠ Selenium failed: {e}")
            self.use_selenium = False

    def get_html(self, url: str) -> str:
        """Fetch HTML content"""
        if self.use_selenium and self.driver:
            try:
                self.driver.get(url)
                time.sleep(3)
                return self.driver.page_source
            except Exception as e:
                print(f"Error loading {url}: {e}")
                return ""
        else:
            try:
                response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return ""

    def parse_model_card(self, card) -> Optional[Dict]:
        """Parse model card from listing"""
        try:
            data = {}

            # Find link
            link = card.find('a', href=re.compile(r'/models/\d+'))
            if link:
                href = link.get('href')
                data['model_url'] = f"{self.base_url}{href}"
                match = re.search(r'/models/(\d+)', href)
                if match:
                    data['model_id'] = match.group(1)

            # Model name
            title = card.find(['h2', 'h3'])
            if title:
                data['model_name'] = title.get_text(strip=True)

            # Stats
            stats = card.find_all(['span', 'div'])
            for stat in stats:
                text = stat.get_text().lower()
                if 'download' in text:
                    data['downloads'] = self._extract_number(text)
                elif 'favorite' in text or 'like' in text:
                    data['favorites'] = self._extract_number(text)

            # Image
            img = card.find('img')
            if img:
                data['preview_image'] = img.get('src') or img.get('data-src')

            return data if 'model_url' in data else None

        except Exception as e:
            return None

    def scrape_listing_page(self, page: int) -> List[Dict]:
        """Scrape models from listing page"""
        url = f"{self.base_url}/models?page={page}&sort={COMMON_CONFIG['sort']}&period={COMMON_CONFIG['period']}"

        html = self.get_html(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all(['div', 'article'], class_=re.compile(r'card|item', re.I))

        models = []
        for card in cards:
            model = self.parse_model_card(card)
            if model:
                models.append(model)

        return models

    def scrape_model_details(self, url: str) -> Dict:
        """Scrape detailed model page"""
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        details = {'url': url}

        try:
            # Title
            title = soup.find(['h1', 'h2'])
            if title:
                details['title'] = title.get_text(strip=True)

            # Description
            desc = soup.find(['div', 'p'], class_=re.compile(r'description', re.I))
            if desc:
                details['description'] = desc.get_text(strip=True)[:1000]

            # Tags
            tags = soup.find_all(['span', 'a'], class_=re.compile(r'tag', re.I))
            details['tags'] = ', '.join([t.get_text(strip=True) for t in tags[:15]])

            # Base model
            base = soup.find(string=re.compile(r'SD 1\.5|SDXL|SD 2', re.I))
            if base:
                details['base_model'] = base.strip()

        except Exception as e:
            print(f"Error parsing {url}: {e}")

        return details

    def scrape(self, max_pages: Optional[int] = None) -> pd.DataFrame:
        """Main scraping method"""
        max_pages = max_pages or SCRAPING_CONFIG["max_pages"]
        all_models = []

        print(f"\n{'='*60}")
        print("CIVITAI WEB SCRAPER")
        print(f"{'='*60}")
        print(f"Max pages: {max_pages}")
        print(f"Fetch details: {SCRAPING_CONFIG['fetch_details']}")
        print(f"{'='*60}\n")

        # Scrape listing pages
        for page in tqdm(range(1, max_pages + 1), desc="Scraping pages"):
            models = self.scrape_listing_page(page)
            if not models:
                break
            all_models.extend(models)
            time.sleep(SCRAPING_CONFIG["rate_limit_delay"])

        print(f"\n✓ Found {len(all_models)} models from listings")

        # Fetch details if enabled
        if SCRAPING_CONFIG["fetch_details"]:
            print("\nFetching model details...")
            for model in tqdm(all_models, desc="Details"):
                if 'model_url' in model:
                    details = self.scrape_model_details(model['model_url'])
                    model.update(details)
                    time.sleep(1.5)

        df = pd.DataFrame(all_models)
        return df

    def _extract_number(self, text: str) -> Optional[int]:
        """Extract number from text"""
        match = re.search(r'([\d.]+)\s*([KkMm])?', text)
        if match:
            num = float(match.group(1))
            suffix = match.group(2)
            if suffix:
                if suffix.lower() == 'k':
                    num *= 1000
                elif suffix.lower() == 'm':
                    num *= 1000000
            return int(num)
        return None

    def close(self):
        """Clean up"""
        if self.driver:
            self.driver.quit()
