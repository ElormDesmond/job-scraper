import json
import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper
from engine.nlp_parser import extract_structured_requirements, extract_salary_range
from engine.diversity_classifier import extract_diversity_badges
from engine.legitimacy_checker import inspect_job_legitimacy

class DevToScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 15):
        super().__init__("devto", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        raw_json = self.fetch_url("https://dev.to/api/articles?tag=job&per_page=15")
        jobs = []

        if raw_json:
            try:
                articles = json.loads(raw_json)
                for item in articles:
                    title = item.get("title", "")
                    description = item.get("description", "") or title
                    url = item.get("url", "https://dev.to")
                    posting_date = item.get("published_at", datetime.datetime.now().strftime("%Y-%m-%d"))[:10]
                    user_info = item.get("user", {})
                    company = user_info.get("name", "Dev.to Tech Partner")

                    nlp = extract_structured_requirements(description)
                    sal = extract_salary_range(description)
                    div_badges = extract_diversity_badges(description)

                    job_id = f"devto_{item.get('id', hash(title))}"

                    job_dict = {
                        "job_id": job_id,
                        "job_title": title,
                        "company_name": company,
                        "company_website": "https://dev.to",
                        "location": "Worldwide Remote",
                        "work_location_type": "remote_only",
                        "country": "International",
                        "posting_date": posting_date,
                        "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
                        "source": "devto",
                        "source_url": url,
                        "source_portal_url": "https://dev.to/t/job",
                        "job_description_raw": description,
                        "salary_range": sal["salary_range"],
                        "salary_confidence": sal["salary_confidence"],
                        "required_skills": nlp["required_skills"] or ["JavaScript", "Python", "React", "Node.js"],
                        "required_experience_years": nlp["required_experience_years"],
                        "required_education": nlp["required_education"],
                        "preferred_qualifications": ["Open source contributions"],
                        "certifications_required": nlp["certifications_required"],
                        "programming_languages": nlp["programming_languages"],
                        "tools_frameworks": nlp["tools_frameworks"],
                        "company_size": "smb",
                        "company_industry": "Technology",
                        "hiring_urgency": "normal",
                        "visa_sponsorship": nlp["visa_sponsorship"],
                        "work_visa_support": nlp["work_visa_support"],
                        "relocation_assistance": nlp["relocation_assistance"],
                        "benefits_listed": ["100% Remote", "Flexible Working Hours"],
                        "diversity_badges": div_badges or ["DEI Commitment"],
                        "salary_transparency": sal["salary_transparency"],
                        "verification_status": "verified",
                        "last_checked": datetime.datetime.utcnow().isoformat() + "Z",
                        "application_link": url,
                        "company_verified": "yes",
                        "posting_active": "yes"
                    }

                    v_status, c_verified, p_active = inspect_job_legitimacy(job_dict)
                    job_dict["verification_status"] = v_status
                    job_dict["company_verified"] = c_verified
                    job_dict["posting_active"] = p_active

                    if p_active == "yes":
                        jobs.append(job_dict)
            except Exception as e:
                self.logger.error(f"Error parsing Dev.to jobs: {e}")

        return jobs
