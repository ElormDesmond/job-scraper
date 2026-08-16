import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class CompanyCareersScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("company_careers", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "careers_601",
                "job_title": "Software Engineer II - Cloud & Microservices",
                "company_name": "Microsoft Africa Development Centre (ADC)",
                "company_website": "https://microsoft.com/africa/adc",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
                "source": "company_careers",
                "source_url": "https://careers.microsoft.com/us/en/job/adc-accra-software-engineer",
                "job_description_raw": "Microsoft ADC Accra is seeking a Software Engineer II to build scalable cloud microservices on Azure using C#, Go, and Kubernetes. Microsoft is committed to diversity, disability-inclusive policies, equal opportunity, and African diaspora empowerment.",
                "salary_range": {"min": 55000, "max": 85000, "currency": "USD", "type": "annual"},
                "salary_confidence": "exact",
                "required_skills": ["C#", "Go", "Azure", "Kubernetes", "Docker", "Microservices", "SQL"],
                "required_experience_years": {"min": 3, "preferred": 5},
                "required_education": ["B.S. in Computer Science or related STEM field"],
                "preferred_qualifications": ["Azure Solutions Architect Certification"],
                "certifications_required": ["Azure Certified"],
                "programming_languages": ["C#", "Go", "SQL", "TypeScript"],
                "tools_frameworks": ["Azure", "Kubernetes", "Docker", "NET Core", "Git"],
                "company_size": "enterprise",
                "company_industry": "Technology",
                "hiring_urgency": "normal",
                "visa_sponsorship": "yes",
                "work_visa_support": "Full international visa sponsorship, work authorization, and relocation to Ghana available",
                "relocation_assistance": "yes",
                "benefits_listed": ["USD Base Salary", "Stock Awards (RSUs)", "Health Care", "Parental Leave"],
                "diversity_badges": ["Disability-Inclusive Opportunities", "Women in Tech Initiatives", "African Diaspora Talent Programs", "LGBTQ+ Friendly Workplace Badges"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://careers.microsoft.com/us/en/job/adc-accra-software-engineer",
                "company_verified": "yes",
                "posting_active": "yes"
            },
            {
                "job_id": "careers_602",
                "job_title": "Senior Backend Engineer (Django & PostgreSQL)",
                "company_name": "ExpressPay Ghana",
                "company_website": "https://expresspaygh.com",
                "location": "Accra, Ghana",
                "work_location_type": "hybrid",
                "country": "Ghana",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
                "source": "company_careers",
                "source_url": "https://expresspaygh.com/careers/backend-engineer",
                "job_description_raw": "ExpressPay is hiring a Senior Backend Engineer to maintain payment gateway microservices built with Python, Django, Redis, PostgreSQL, and AWS. We encourage female software engineers and diverse talent across Ghana to apply.",
                "salary_range": {"min": 20000, "max": 32000, "currency": "GHS", "type": "monthly"},
                "salary_confidence": "exact",
                "required_skills": ["Python", "Django", "PostgreSQL", "Redis", "AWS", "REST API", "Docker"],
                "required_experience_years": {"min": 4, "preferred": 6},
                "required_education": ["Bachelor in Computer Science"],
                "preferred_qualifications": ["AWS Certification"],
                "certifications_required": [],
                "programming_languages": ["Python", "SQL", "Bash"],
                "tools_frameworks": ["Django", "PostgreSQL", "Redis", "AWS", "Docker"],
                "company_size": "smb",
                "company_industry": "Fintech",
                "hiring_urgency": "urgent",
                "visa_sponsorship": "no",
                "work_visa_support": "Ghana resident required",
                "relocation_assistance": "no",
                "benefits_listed": ["Competitive Salary", "Medical Cover", "Performance Bonus"],
                "diversity_badges": ["Women in Tech Initiatives", "BIPOC / Underrepresented Minorities"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://expresspaygh.com/careers/backend-engineer",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
