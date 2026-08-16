import os
import time
import random
import urllib.request
import urllib.parse
import json
import logging
from typing import List, Dict, Any

# Auto load .env if present
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "JobScraperBot/1.0 (+https://antigravity.ai/bot)"
]

class BaseScraper:
    def __init__(self, source_name: str, rate_limit_per_min: int = 10):
        self.source_name = source_name
        self.rate_limit_delay = 60.0 / max(rate_limit_per_min, 1)
        self.logger = logging.getLogger(source_name)

    def fetch_url(self, url: str) -> str:
        time.sleep(self.rate_limit_delay * random.uniform(0.8, 1.2))
        
        # Read ScraperAPI key from environment variable
        scraper_api_key = os.environ.get("SCRAPER_API_KEY")
        target_url = url
        
        if scraper_api_key and not ("api.scraperapi.com" in url or "remotive.com" in url or "weworkremotely.com" in url or "dev.to" in url):
            target_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={urllib.parse.quote(url)}"
            self.logger.info(f"Routing fetch via ScraperAPI anti-bot proxy for {url}...")

        req = urllib.request.Request(
            target_url,
            headers={
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.warning(f"Fetch failed for {url}: {e}")
            return ""

    def scrape(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement scrape()")
