import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper
from engine.legitimacy_checker import inspect_job_legitimacy

class GlassdoorScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 5):
        super().__init__("glassdoor", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "glassdoor_401",
                "job_title": "Lead Software Engineer - MERN / React Native",
                "company_name": "mPharma",
                "company_website": "https://mpharma.com",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=21)).strftime("%Y-%m-%d"),
                "source": "glassdoor",
                "source_url": "https://mpharma.com/careers",
                "source_portal_url": "https://www.glassdoor.com",
                "job_description_raw": "mPharma is hiring a Lead Software Engineer in Accra to oversee healthcare inventory distribution platforms. Stack: React, React Native, Node.js, Express, MongoDB, and PostgreSQL. We promote equal opportunity, gender equality, and supportive maternity/paternity policies.",
                "salary_range": {"min": 30000, "max": 48000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "exact",
                "required_skills": ["JavaScript", "TypeScript", "React", "React Native", "Node.js", "Express", "MongoDB", "PostgreSQL"],
                "required_experience_years": {"min": 5, "preferred": 7},
                "required_education": ["Bachelor in Computer Science / Software Engineering"],
                "preferred_qualifications": ["AWS Certification", "Experience with healthcare compliance"],
                "certifications_required": [],
                "programming_languages": ["JavaScript", "TypeScript", "SQL"],
                "tools_frameworks": ["React", "React Native", "Node.js", "Express", "MongoDB", "PostgreSQL"],
                "company_size": "enterprise",
                "company_industry": "Healthcare / Technology",
                "hiring_urgency": "urgent",
                "visa_sponsorship": "yes",
                "work_visa_support": "Assistance for West African talent relocating to Ghana",
                "relocation_assistance": "partial",
                "benefits_listed": ["Health Insurance", "Paternity & Maternity Leave", "Gym Membership", "Equity"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities", "DEI Commitment"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://mpharma.com/careers",
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
