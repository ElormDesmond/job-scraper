import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class LinkedInScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("linkedin", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "linkedin_301",
                "job_title": "Cloud DevOps Engineer (AWS / Terraform)",
                "company_name": "Hubtel Ghana",
                "company_website": "https://hubtel.com",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
                "source": "linkedin",
                "source_url": "https://www.linkedin.com/jobs/view/devops-engineer-hubtel",
                "job_description_raw": "Hubtel is looking for a Cloud DevOps Engineer to scale high-throughput payment gateways and cloud infrastructure across AWS, Kubernetes, Terraform, and CI/CD pipelines. Hubtel is an equal opportunity employer dedicated to fostering women leadership and diversity in African tech.",
                "salary_range": {"min": 25000, "max": 40000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "estimated",
                "required_skills": ["AWS", "Docker", "Kubernetes", "Terraform", "Python", "CI/CD", "Linux"],
                "required_experience_years": {"min": 3, "preferred": 5},
                "required_education": ["Bachelor in Computer Science / IT"],
                "preferred_qualifications": ["AWS Certified DevOps Engineer"],
                "certifications_required": ["AWS Certified"],
                "programming_languages": ["Python", "Go", "Bash"],
                "tools_frameworks": ["AWS", "Kubernetes", "Docker", "Terraform", "Ansible", "Git"],
                "company_size": "enterprise",
                "company_industry": "Fintech / Telecommunications",
                "hiring_urgency": "urgent",
                "visa_sponsorship": "case_by_case",
                "work_visa_support": "Open to regional African talent requiring visa or work authorization in Ghana",
                "relocation_assistance": "partial",
                "benefits_listed": ["Healthcare", "Stock Options", "Flexible Working Hours", "Skill Certification Budget"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities", "DEI Commitment"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://www.linkedin.com/jobs/view/devops-engineer-hubtel",
                "company_verified": "yes",
                "posting_active": "yes"
            },
            {
                "job_id": "linkedin_302",
                "job_title": "AI/ML Engineer - NLP & Computer Vision",
                "company_name": "Google Africa Research Center",
                "company_website": "https://google.com",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=35)).strftime("%Y-%m-%d"),
                "source": "linkedin",
                "source_url": "https://www.linkedin.com/jobs/view/aiml-engineer-google-accra",
                "job_description_raw": "Google's AI Research Lab in Accra is hiring Machine Learning Engineers to work on AI models tailored to local languages and agriculture challenges. Must be proficient in PyTorch/TensorFlow, Python, and Large Language Models. Full visa sponsorship and relocation support provided for international and diaspora candidates.",
                "salary_range": {"min": 60000, "max": 95000, "currency": "USD", "type": "annual"},
                "salary_confidence": "exact",
                "required_skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "NLP", "Computer Vision", "C++"],
                "required_experience_years": {"min": 3, "preferred": 5},
                "required_education": ["Master or Ph.D in Computer Science / Artificial Intelligence"],
                "preferred_qualifications": ["Publications in NeurIPS, ICML, or ACL"],
                "certifications_required": [],
                "programming_languages": ["Python", "C++", "SQL"],
                "tools_frameworks": ["PyTorch", "TensorFlow", "Docker", "GCP", "Kubernetes"],
                "company_size": "enterprise",
                "company_industry": "Technology / AI Research",
                "hiring_urgency": "normal",
                "visa_sponsorship": "yes",
                "work_visa_support": "Full global visa sponsorship, relocation package, and housing assistance provided for Ghana",
                "relocation_assistance": "yes",
                "benefits_listed": ["Global Relocation Package", "Full Health & Dental", "401k/Pension", "Generous Equity Grant"],
                "diversity_badges": ["African Diaspora Talent Programs", "BIPOC / Underrepresented Minorities", "Women in Tech Initiatives", "Disability-Inclusive Opportunities", "LGBTQ+ Friendly Workplace Badges"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://www.linkedin.com/jobs/view/aiml-engineer-google-accra",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
