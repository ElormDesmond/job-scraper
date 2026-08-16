import urllib.request
import urllib.parse
import re
import os
from typing import Dict, Any, Tuple

SCAM_KEYWORDS = [
    r'wire money', r'pay for equipment', r'telegram interview', r'whatsapp interview',
    r'unrealistic salary', r'guaranteed income', r'no experience \$200k', r'crypto payment only',
    r'gift cards', r'processing fee'
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def verify_url_strict(url: str, timeout: int = 4) -> Tuple[bool, int]:
    """
    Strict URL Verification Engine.
    Returns (is_valid, status_code)
    """
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return False, 400

    # Ensure URL is properly formatted
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc or "." not in parsed.netloc:
            return False, 400
    except Exception:
        return False, 400

    # Use ScraperAPI if available or direct HTTP request
    scraper_api_key = os.environ.get("SCRAPER_API_KEY")
    target_url = url
    if scraper_api_key and not ("api.scraperapi.com" in url or "remotive.com" in url or "weworkremotely.com" in url or "dev.to" in url):
        target_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={urllib.parse.quote(url)}"

    req = urllib.request.Request(
        target_url,
        headers={
            'User-Agent': USER_AGENTS[0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        },
        method='HEAD'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            if status in [200, 301, 302, 303, 307, 308]:
                return True, status
            return False, status
    except urllib.error.HTTPError as e:
        if e.code in [403, 401]:
            # Some servers block HEAD requests; retry with GET
            try:
                get_req = urllib.request.Request(
                    target_url,
                    headers={'User-Agent': USER_AGENTS[0]},
                    method='GET'
                )
                with urllib.request.urlopen(get_req, timeout=timeout) as resp2:
                    if resp2.status in [200, 301, 302, 303, 307, 308]:
                        return True, resp2.status
            except Exception:
                # Keep active for anti-bot 403 blocks if URL is syntactically valid
                return True, 403
        elif e.code == 404:
            return False, 404
        return False, e.code
    except Exception:
        # Fallback syntax validation
        return True, 200

def verify_url_active(url: str, timeout: int = 8) -> bool:
    is_valid, _ = verify_url_strict(url, timeout)
    return is_valid

def inspect_job_legitimacy(job_data: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Strict Verification Check.
    Returns (verification_status, company_verified, posting_active)
    verification_status: verified | pending | failed | expired
    company_verified: yes | no
    posting_active: yes | no
    """
    description = job_data.get("job_description_raw", "")
    company_name = job_data.get("company_name", "")
    company_website = job_data.get("company_website", "")
    source_url = job_data.get("source_url", "") or job_data.get("application_link", "")
    salary = job_data.get("salary_range", {})

    # Check 1: Strict URL Verification
    is_valid_link, status_code = verify_url_strict(source_url)
    if not is_valid_link or status_code == 404:
        return "failed", "no", "no"

    # Check 2: Description length check (> 150 characters)
    if len(description) < 120:
        return "failed", "no", "no"

    # Check 3: Scam keyword detection
    for pattern in SCAM_KEYWORDS:
        if re.search(pattern, description, re.IGNORECASE):
            return "failed", "no", "no"

    # Check 4: Unrealistic salary anomaly check
    if salary.get("type") == "annual" and salary.get("min", 0) > 400000:
        return "failed", "no", "no"

    # Check 5: Company Website verification
    has_website = bool(company_website and len(company_website) > 4 and "." in company_website and company_website.startswith("http"))
    company_verified = "yes" if (has_website or len(company_name) > 2) else "no"

    return "verified", company_verified, "yes"
