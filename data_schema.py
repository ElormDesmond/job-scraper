from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class JobListing:
    # Required Fields
    job_id: str
    job_title: str
    company_name: str
    company_website: str
    location: str
    work_location_type: str  # remote_only | hybrid | on_site
    country: str
    posting_date: str  # YYYY-MM-DD
    application_deadline: str
    source: str  # linkedin | glassdoor | wellfound | remotive | weworkremotely | devto | jobberman | myjobmag | tonaton | relocateme | jobhouse | company_careers
    source_url: str
    source_portal_url: str  # Official job board portal homepage/search URL
    job_description_raw: str
    salary_range: Dict[str, Any]  # {min, max, currency, type: annual|monthly|hourly}
    salary_confidence: str  # exact | estimated | not_provided

    # Structured Requirements
    required_skills: List[str]
    required_experience_years: Dict[str, Any]  # {min: int, preferred: int}
    required_education: List[str]
    preferred_qualifications: List[str]
    certifications_required: List[str]
    programming_languages: List[str]
    tools_frameworks: List[str]

    # Company & Benefits
    company_size: str  # startup | smb | enterprise
    company_industry: str
    hiring_urgency: str  # urgent | normal | no_timeline
    visa_sponsorship: str  # yes | no | case_by_case | not_mentioned
    work_visa_support: str
    relocation_assistance: str  # yes | partial | no
    benefits_listed: List[str]
    diversity_badges: List[str]
    salary_transparency: str  # yes | no

    # Metadata
    verification_status: str  # verified | pending | failed | expired
    last_checked: str  # ISO 8601
    application_link: str
    company_verified: str  # yes | no
    posting_active: str  # yes | no

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "job_title": self.job_title,
            "company_name": self.company_name,
            "company_website": self.company_website,
            "location": self.location,
            "work_location_type": self.work_location_type,
            "country": self.country,
            "posting_date": self.posting_date,
            "application_deadline": self.application_deadline,
            "source": self.source,
            "source_url": self.source_url,
            "source_portal_url": self.source_portal_url,
            "job_description_raw": self.job_description_raw,
            "salary_range": self.salary_range,
            "salary_confidence": self.salary_confidence,
            "required_skills": self.required_skills,
            "required_experience_years": self.required_experience_years,
            "required_education": self.required_education,
            "preferred_qualifications": self.preferred_qualifications,
            "certifications_required": self.certifications_required,
            "programming_languages": self.programming_languages,
            "tools_frameworks": self.tools_frameworks,
            "company_size": self.company_size,
            "company_industry": self.company_industry,
            "hiring_urgency": self.hiring_urgency,
            "visa_sponsorship": self.visa_sponsorship,
            "work_visa_support": self.work_visa_support,
            "relocation_assistance": self.relocation_assistance,
            "benefits_listed": self.benefits_listed,
            "diversity_badges": self.diversity_badges,
            "salary_transparency": self.salary_transparency,
            "verification_status": self.verification_status,
            "last_checked": self.last_checked,
            "application_link": self.application_link,
            "company_verified": self.company_verified,
            "posting_active": self.posting_active
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobListing":
        return cls(**data)
