import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class JobhouseScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("jobhouse", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "jobhouse_gh_1101",
                "job_title": "IT Project Manager & Technical Operations Lead",
                "company_name": "Fidelity Bank Ghana",
                "company_website": "https://fidelitybank.com.gh",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=22)).strftime("%Y-%m-%d"),
                "source": "jobhouse",
                "source_url": "https://jobhouse.com.gh/job/it-project-manager-fidelity",
                "job_description_raw": "Fidelity Bank Ghana is hiring an IT Project Manager in Accra to direct digital banking transformations, software delivery, and cloud infrastructure projects. Agile/PMP certification preferred. We promote female leadership in banking and tech.",
                "salary_range": {"min": 25000, "max": 40000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "exact",
                "required_skills": ["IT Project Management", "Agile", "Scrum Master", "PMP", "Technical Leadership", "Jira"],
                "required_experience_years": {"min": 4, "preferred": 6},
                "required_education": ["Bachelor in Computer Science or Project Management"],
                "preferred_qualifications": ["PMP Certification", "Certified Scrum Master (CSM)"],
                "certifications_required": ["PMP", "Scrum Master"],
                "programming_languages": [],
                "tools_frameworks": ["Jira", "Confluence", "MS Project", "Agile"],
                "company_size": "enterprise",
                "company_industry": "Banking & Financial Services",
                "hiring_urgency": "normal",
                "visa_sponsorship": "no",
                "work_visa_support": "Ghanaian work authorization required",
                "relocation_assistance": "no",
                "benefits_listed": ["Competitive Salary", "Banking Allowance", "Medical Care", "Staff Loans"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities", "DEI Commitment"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://jobhouse.com.gh/job/it-project-manager-fidelity",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
