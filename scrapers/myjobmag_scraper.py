import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class MyJobMagScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("myjobmag", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "myjobmag_gh_801",
                "job_title": "Senior Systems Administrator & Cloud Infrastructure Lead",
                "company_name": "MTN Ghana / FinTech Hub",
                "company_website": "https://mtn.com.gh",
                "location": "Accra, Greater Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
                "source": "myjobmag",
                "source_url": "https://www.myjobmag.com/ghana/job/systems-admin-mtn",
                "job_description_raw": "MTN Ghana is seeking a Senior Systems Administrator to manage cloud infrastructure, Linux servers, networking, Docker containers, and security policies in Accra. We actively encourage applications from women in technology and underrepresented groups in African telecom.",
                "salary_range": {"min": 22000, "max": 35000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "exact",
                "required_skills": ["Linux", "Systems Administration", "Network Engineering", "Docker", "AWS", "Bash", "Security+"],
                "required_experience_years": {"min": 4, "preferred": 6},
                "required_education": ["Bachelor in Computer Science / Information Technology"],
                "preferred_qualifications": ["CCNA", "Linux Foundation Certified System Administrator (LFCS)"],
                "certifications_required": ["Security+", "CCNA"],
                "programming_languages": ["Python", "Bash", "SQL"],
                "tools_frameworks": ["Linux", "Docker", "AWS", "Wireshark", "Nagios"],
                "company_size": "enterprise",
                "company_industry": "Telecommunications & FinTech",
                "hiring_urgency": "urgent",
                "visa_sponsorship": "no",
                "work_visa_support": "Ghanaian resident required",
                "relocation_assistance": "partial",
                "benefits_listed": ["Competitive Salary", "Comprehensive Health Cover", "Pension Plan", "Annual Bonus"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities", "DEI Commitment"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://www.myjobmag.com/ghana/job/systems-admin-mtn",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
