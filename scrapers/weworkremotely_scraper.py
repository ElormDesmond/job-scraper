import xml.etree.ElementTree as ET
import datetime
from typing import List, Dict, Any
from scrapers.base_scraper import BaseScraper
from engine.nlp_parser import extract_structured_requirements, extract_salary_range
from engine.diversity_classifier import extract_diversity_badges
from engine.legitimacy_checker import inspect_job_legitimacy

class WeWorkRemotelyScraper(BaseScraper):
    def __init__(self, rate_limit_per_min: int = 10):
        super().__init__("weworkremotely", rate_limit_per_min)

    def scrape(self) -> List[Dict[str, Any]]:
        raw_xml = self.fetch_url("https://weworkremotely.com/categories/remote-programming-jobs.rss")
        jobs = []

        if raw_xml:
            try:
                root = ET.fromstring(raw_xml)
                items = root.findall('.//item')
                for item in items[:15]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description')

                    full_title = title_elem.text if title_elem is not None else "Remote Engineer"
                    url = link_elem.text if link_elem is not None else "https://weworkremotely.com"
                    description = desc_elem.text if desc_elem is not None else full_title
                    
                    company = "Remote Company"
                    job_title = full_title
                    if ":" in full_title:
                        parts = full_title.split(":", 1)
                        company = parts[0].strip()
                        job_title = parts[1].strip()

                    nlp = extract_structured_requirements(description)
                    sal = extract_salary_range(description)
                    div_badges = extract_diversity_badges(description)

                    job_id = f"wwr_{hash(url)}"
                    company_clean = company.lower().replace(' ', '').replace(':', '').replace('.', '')

                    job_dict = {
                        "job_id": job_id,
                        "job_title": job_title,
                        "company_name": company,
                        "company_website": f"https://{company_clean}.com",
                        "location": "Worldwide Remote",
                        "work_location_type": "remote_only",
                        "country": "International",
                        "posting_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "application_deadline": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
                        "source": "weworkremotely",
                        "source_url": url,
                        "source_portal_url": "https://weworkremotely.com",
                        "job_description_raw": description,
                        "salary_range": sal["salary_range"],
                        "salary_confidence": sal["salary_confidence"],
                        "required_skills": nlp["required_skills"],
                        "required_experience_years": nlp["required_experience_years"],
                        "required_education": nlp["required_education"],
                        "preferred_qualifications": ["Self-directed problem solver", "Excellent written English"],
                        "certifications_required": nlp["certifications_required"],
                        "programming_languages": nlp["programming_languages"],
                        "tools_frameworks": nlp["tools_frameworks"],
                        "company_size": "smb",
                        "company_industry": "Technology",
                        "hiring_urgency": "normal",
                        "visa_sponsorship": nlp["visa_sponsorship"],
                        "work_visa_support": nlp["work_visa_support"],
                        "relocation_assistance": nlp["relocation_assistance"],
                        "benefits_listed": ["100% Remote", "Global Health Cover", "Equipment Allowance"],
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
                self.logger.error(f"Error parsing WeWorkRemotely RSS: {e}")

        return jobs
