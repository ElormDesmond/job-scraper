import time
import random
import urllib.request
import json
import logging
from typing import List, Dict, Any

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "JobScraperBot/1.0 (+https://antigravity.ai/bot)"
]

class BaseScraper:
    def __init__(self, source_name: str, rate_limit_per_min: int = 10):
        self.source_name = source_name
        self.rate_limit_delay = 60.0 / max(rate_limit_per_min, 1)
        self.logger = logging.getLogger(source_name)

    def fetch_url(self, url: str) -> str:
        time.sleep(self.rate_limit_delay * random.uniform(0.8, 1.2))
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.warning(f"Fetch failed for {url}: {e}")
            return ""

    def scrape(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement scrape()")
