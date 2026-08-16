import json
import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper
from engine.nlp_parser import extract_structured_requirements, extract_salary_range
from engine.diversity_classifier import extract_diversity_badges
from engine.legitimacy_checker import inspect_job_legitimacy

class RemotiveScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 15):
        super().__init__("remotive", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        raw_json = self.fetch_url("https://remotive.com/api/remote-jobs?category=software-dev&limit=15")
        jobs = []
        
        if raw_json:
            try:
                data = json.loads(raw_json)
                job_list = data.get("jobs", [])
                for item in job_list[:15]:
                    title = item.get("title", "")
                    company = item.get("company_name", "")
                    description = item.get("description", "") or f"{title} at {company}."
                    url = item.get("url", "https://remotive.com")
                    posting_date = item.get("publication_date", datetime.datetime.now().strftime("%Y-%m-%d"))[:10]
                    location = item.get("candidate_required_location", "Worldwide Remote")
                    
                    nlp = extract_structured_requirements(description)
                    sal = extract_salary_range(description)
                    div_badges = extract_diversity_badges(description)
                    
                    job_id = f"remotive_{item.get('id', hash(title))}"
                    company_clean = company.lower().replace(' ', '').replace('.', '').replace(',', '')
                    
                    job_dict = {
                        "job_id": job_id,
                        "job_title": title,
                        "company_name": company,
                        "company_website": f"https://{company_clean}.com",
                        "location": location,
                        "work_location_type": "remote_only",
                        "country": "International",
                        "posting_date": posting_date,
                        "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
                        "source": "remotive",
                        "source_url": url,
                        "source_portal_url": "https://remotive.com",
                        "job_description_raw": description,
                        "salary_range": sal["salary_range"],
                        "salary_confidence": sal["salary_confidence"],
                        "required_skills": nlp["required_skills"],
                        "required_experience_years": nlp["required_experience_years"],
                        "required_education": nlp["required_education"],
                        "preferred_qualifications": ["Strong remote communication skills", "Self-starter attitude"],
                        "certifications_required": nlp["certifications_required"],
                        "programming_languages": nlp["programming_languages"],
                        "tools_frameworks": nlp["tools_frameworks"],
                        "company_size": "smb",
                        "company_industry": "Technology",
                        "hiring_urgency": "normal",
                        "visa_sponsorship": nlp["visa_sponsorship"],
                        "work_visa_support": nlp["work_visa_support"],
                        "relocation_assistance": nlp["relocation_assistance"],
                        "benefits_listed": ["100% Remote", "Flexible Working Hours", "Competitive Salary"],
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
                self.logger.error(f"Error parsing Remotive jobs: {e}")

        return jobs
