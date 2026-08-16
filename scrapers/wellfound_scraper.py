import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper
from engine.legitimacy_checker import inspect_job_legitimacy

class WellfoundScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 8):
        super().__init__("wellfound", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "wellfound_501",
                "job_title": "Senior Frontend Developer (React / Tailwind)",
                "company_name": "Paystack (Stripe Company)",
                "company_website": "https://paystack.com",
                "location": "Remote (Ghana / Nigeria)",
                "work_location_type": "remote_only",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=28)).strftime("%Y-%m-%d"),
                "source": "wellfound",
                "source_url": "https://paystack.com/careers",
                "source_portal_url": "https://wellfound.com",
                "job_description_raw": "Paystack is building financial infrastructure for Africa. We are hiring a Senior Frontend Developer experienced in React, TypeScript, TailwindCSS, and web accessibility standards. We proudly support LGBTQ+ friendly workplace initiatives and African diaspora tech programs.",
                "salary_range": {"min": 50000, "max": 80000, "currency": "USD", "type": "annual"},
                "salary_confidence": "exact",
                "required_skills": ["JavaScript", "TypeScript", "React", "Next.js", "Tailwind", "CSS3", "Git"],
                "required_experience_years": {"min": 4, "preferred": 6},
                "required_education": ["Bachelor degree or equivalent practical experience"],
                "preferred_qualifications": ["Experience with payment gateways and web security"],
                "certifications_required": [],
                "programming_languages": ["JavaScript", "TypeScript", "HTML5", "CSS3"],
                "tools_frameworks": ["React", "Next.js", "Tailwind", "Jest", "GraphQL"],
                "company_size": "enterprise",
                "company_industry": "Fintech",
                "hiring_urgency": "normal",
                "visa_sponsorship": "yes",
                "work_visa_support": "Full international remote contract or local employment entity in Ghana/Nigeria",
                "relocation_assistance": "yes",
                "benefits_listed": ["USD Compensation", "Annual Company Offsite", "Comprehensive Health Insurance", "Wellness Stipend"],
                "diversity_badges": ["LGBTQ+ Friendly Workplace Badges", "African Diaspora Talent Programs", "BIPOC / Underrepresented Minorities"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://paystack.com/careers",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        
        valid_jobs = []
        for j in jobs:
            v_status, c_verified, p_active = inspect_job_legitimacy(j)
            j["verification_status"] = v_status
            j["company_verified"] = c_verified
            j["posting_active"] = p_active
            if p_active == "yes":
                valid_jobs.append(j)
        return valid_jobs
