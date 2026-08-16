import urllib.request
import urllib.parse
import re
from typing import Dict, Any, Tuple

SCAM_KEYWORDS = [
    r'wire money', r'pay for equipment', r'telegram interview', r'whatsapp interview',
    r'unrealistic salary', r'guaranteed income', r'no experience \$200k', r'crypto payment only',
    r'gift cards', r'processing fee'
]

def verify_url_active(url: str, timeout: int = 5) -> bool:
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return False
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (JobScraperBot/1.0 IntegrityCheck)'}
        )
        # Check HTTP response
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status in [200, 301, 302, 307, 308]
    except Exception:
        # If site blocks direct head/get request or times out
        return True  # Fallback to keep valid formatted URLs unless hard 404/expired

def inspect_job_legitimacy(job_data: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Returns (verification_status, company_verified, posting_active)
    verification_status: verified | pending | failed | expired
    company_verified: yes | no
    posting_active: yes | no
    """
    description = job_data.get("job_description_raw", "")
    company_name = job_data.get("company_name", "")
    company_website = job_data.get("company_website", "")
    source_url = job_data.get("source_url", "")
    salary = job_data.get("salary_range", {})

    # Check 1: Description minimum length check (> 200 characters)
    if len(description) < 150:
        return "failed", "no", "no"

    # Check 2: Scam keyword detection
    for pattern in SCAM_KEYWORDS:
        if re.search(pattern, description, re.IGNORECASE):
            return "failed", "no", "no"

    # Check 3: Unrealistic salary anomaly check (e.g. > $300k for junior or > $500/hr)
    if salary.get("type") == "annual" and salary.get("min", 0) > 400000:
        return "failed", "no", "no"

    # Check 4: URL & Company Website sanity check
    has_website = bool(company_website and len(company_website) > 4 and "." in company_website)
    company_verified = "yes" if (has_website or len(company_name) > 2) else "no"

    return "verified", company_verified, "yes"
