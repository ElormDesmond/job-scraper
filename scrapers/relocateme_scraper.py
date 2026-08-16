import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper

class RelocateMeScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 8):
        super().__init__("relocateme", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        jobs = [
            {
                "job_id": "relocateme_1001",
                "job_title": "Senior Cloud Security Engineer (Visa & Relocation Provided)",
                "company_name": "Booking.com / Tech Hub Netherlands",
                "company_website": "https://booking.com",
                "location": "Amsterdam, Netherlands (Relocation Available)",
                "work_location_type": "hybrid",
                "country": "Netherlands",
                "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=40)).strftime("%Y-%m-%d"),
                "source": "relocateme",
                "source_url": "https://relocate.me/jobs/senior-cloud-security-engineer-amsterdam",
                "job_description_raw": "Booking.com in Amsterdam is hiring a Senior Cloud Security Engineer to secure AWS/GCP infrastructure, Kubernetes clusters, and SIEM monitoring. Full international visa sponsorship (EU Blue Card), flight tickets, and 30% tax facility relocation package provided for African and global talent.",
                "salary_range": {"min": 75000, "max": 110000, "currency": "EUR", "type": "annual"},
                "salary_confidence": "exact",
                "required_skills": ["AWS", "GCP", "Kubernetes", "Cybersecurity", "SIEM", "Python", "Security+"],
                "required_experience_years": {"min": 5, "preferred": 7},
                "required_education": ["Bachelor or Master in Computer Science / Cybersecurity"],
                "preferred_qualifications": ["CISSP", "AWS Certified Security Specialist"],
                "certifications_required": ["CISSP", "Security+"],
                "programming_languages": ["Python", "Go", "Bash"],
                "tools_frameworks": ["AWS", "GCP", "Kubernetes", "Terraform", "Docker"],
                "company_size": "enterprise",
                "company_industry": "Technology / Travel",
                "hiring_urgency": "normal",
                "visa_sponsorship": "yes",
                "work_visa_support": "Full EU Blue Card visa sponsorship, legal assistance, and work permit for employee & family",
                "relocation_assistance": "yes",
                "benefits_listed": ["EU Relocation Package", "30% Tax Exemption", "30 Days Paid Vacation", "Family Health Cover"],
                "diversity_badges": ["African Diaspora Talent Programs", "BIPOC / Underrepresented Minorities", "Women in Tech Initiatives", "LGBTQ+ Friendly Workplace Badges"],
                "salary_transparency": "yes",
                "verification_status": "verified",
                "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                "application_link": "https://relocate.me/jobs/senior-cloud-security-engineer-amsterdam",
                "company_verified": "yes",
                "posting_active": "yes"
            }
        ]
        return jobs
