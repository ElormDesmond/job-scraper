import csv
import json
import datetime
import os
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IS_VERCEL = os.environ.get("VERCEL", "0") == "1" or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

def get_writable_dir() -> str:
    if IS_VERCEL:
        return "/tmp"
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

class DataExporter:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or get_writable_dir()
        os.makedirs(self.output_dir, exist_ok=True)

    def export_csv(self, jobs: List[Dict[str, Any]]) -> str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.output_dir, f"ghana_it_jobs_{date_str}.csv")
        
        fieldnames = [
            "job_id", "job_title", "company_name", "company_website", "source_portal_url", "application_link",
            "location", "work_location_type", "country", "posting_date", "application_deadline", 
            "source", "salary_currency", "salary_min", "salary_max", "visa_sponsorship",
            "diversity_badges", "required_skills", "verification_status", "posting_active"
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for j in jobs:
                sal = j.get("salary_range", {})
                writer.writerow({
                    "job_id": j.get("job_id"),
                    "job_title": j.get("job_title"),
                    "company_name": j.get("company_name"),
                    "company_website": j.get("company_website"),
                    "source_portal_url": j.get("source_portal_url"),
                    "application_link": j.get("application_link") or j.get("source_url"),
                    "location": j.get("location"),
                    "work_location_type": j.get("work_location_type"),
                    "country": j.get("country"),
                    "posting_date": j.get("posting_date"),
                    "application_deadline": j.get("application_deadline"),
                    "source": j.get("source"),
                    "salary_currency": sal.get("currency", "USD"),
                    "salary_min": sal.get("min", 0),
                    "salary_max": sal.get("max", 0),
                    "visa_sponsorship": j.get("visa_sponsorship"),
                    "diversity_badges": "; ".join(j.get("diversity_badges", [])),
                    "required_skills": "; ".join(j.get("required_skills", [])),
                    "verification_status": j.get("verification_status"),
                    "posting_active": j.get("posting_active")
                })
        return filepath

    def export_markdown_report(self, jobs: List[Dict[str, Any]]) -> str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.output_dir, f"job_report_{date_str}.md")
        
        ghana_jobs = [j for j in jobs if "Ghana" in j.get("country", "") or "Ghana" in j.get("location", "")]
        remote_jobs = [j for j in jobs if j.get("work_location_type") == "remote_only"]
        visa_jobs = [j for j in jobs if j.get("visa_sponsorship") in ["yes", "case_by_case"]]
        diversity_jobs = [j for j in jobs if len(j.get("diversity_badges", [])) > 0]
        
        md_content = f"""# 🚀 Verified IT Job Opportunities Report ({date_str})

## 📊 Market Overview & Verified Metrics
- **Active Verified Opportunities**: {len(jobs)}
- **Ghana & Regional Africa Roles**: {len(ghana_jobs)}
- **Fully Remote Roles**: {len(remote_jobs)}
- **Visa Sponsorship Supported**: {len(visa_jobs)}
- **DEI & Inclusion Verified Roles**: {len(diversity_jobs)}

---

## 🌟 Curated Verified Opportunities (With Direct Links)

"""
        for j in jobs:
            sal = j.get("salary_range", {})
            sal_str = f"{sal.get('currency', 'USD')} {sal.get('min', 0):,}" if sal.get('min', 0) else "Not Specified"
            if sal.get('max', 0) and sal.get('max') != sal.get('min'):
                sal_str += f" - {sal.get('max'):,}"
            
            badges_str = " | ".join([f"`{b}`" for b in j.get("diversity_badges", [])])
            skills_str = ", ".join(j.get("required_skills", []))
            apply_link = j.get("application_link") or j.get("source_url")
            company_url = j.get("company_website") or "#"
            portal_url = j.get("source_portal_url") or "#"
            
            md_content += f"""### [{j.get('job_title')}]({apply_link})
- **Company**: **[{j.get('company_name')}]({company_url})** ({j.get('company_size', 'N/A').upper()})
- **Source Portal**: **[{j.get('source').upper()}]({portal_url})** | **Posted**: {j.get('posting_date')} | **Deadline**: {j.get('application_deadline')}
- **Location**: {j.get('location')} ({j.get('work_location_type')})
- **Salary**: **{sal_str}** ({j.get('salary_confidence')})
- **Visa Sponsorship**: `{j.get('visa_sponsorship').upper()}`
- **Diversity Badges**: {badges_str if badges_str else 'N/A'}
- **Key Skills**: `{skills_str}`
- **Verification**: `STATUS: {j.get('verification_status').upper()}` | `COMPANY VERIFIED: {j.get('company_verified').upper()}`

> **Description Summary**:  
> {j.get('job_description_raw')[:300]}...

- 🚀 [Direct Application Link]({apply_link})
- 🏢 [Company Official Website]({company_url})
- 🌐 [Job Board Portal Homepage]({portal_url})

---
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return filepath
