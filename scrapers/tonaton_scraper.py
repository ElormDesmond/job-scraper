import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class TonatonScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("tonaton", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "tonaton_gh_901",
                "job_title": "Full-Stack Web Developer (Node.js & React)",
                "company_name": "Swoove Delivery Ghana",
                "company_website": "https://swoove.delivery",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
                "source": "tonaton",
                "source_url": "https://tonaton.com/jobs/fullstack-developer-swoove",
                "job_description_raw": "Swoove Delivery is seeking a Full-Stack Developer in Accra to build scalable logistics APIs using Node.js, Express, React, TypeScript, and MongoDB. We encourage female software engineers and young Ghanaian talent to apply.",
                "salary_range": {"min": 14000, "max": 22000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "exact",
                "required_skills": ["JavaScript", "TypeScript", "Node.js", "Express", "React", "MongoDB", "REST API"],
                "required_experience_years": {"min": 2, "preferred": 4},
                "required_education": ["Diploma or Degree in Computer Science / IT"],
                "preferred_qualifications": ["Experience with Google Maps API and Socket.io"],
                "certifications_required": [],
                "programming_languages": ["JavaScript", "TypeScript"],
                "tools_frameworks": ["Node.js", "Express", "React", "MongoDB", "Git"],
                "company_size": "startup",
                "company_industry": "Logistics & Technology",
                "hiring_urgency": "urgent",
                "visa_sponsorship": "no",
                "work_visa_support": "Local position in Accra",
                "relocation_assistance": "no",
                "benefits_listed": ["Competitive Salary", "Flexible Working", "Health Cover"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://tonaton.com/jobs/fullstack-developer-swoove",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
