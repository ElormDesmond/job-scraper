import re
from typing import Dict, List, Any

# Technical skills and keyword patterns
LANGUAGES_PATTERNS = [
    "Python", "JavaScript", "TypeScript", "Java", "C\\+\\+", "C#", "Go", "Golang", "Rust", 
    "PHP", "Ruby", "Kotlin", "Swift", "SQL", "R", "Dart", "Bash", "HTML5?", "CSS3?"
]

TOOLS_FRAMEWORKS_PATTERNS = [
    "React", "React Native", "Next\\.js", "Vue", "Angular", "Node\\.js", "Express", "Django", 
    "Flask", "FastAPI", "Spring Boot", "Laravel", "Flutter", "Docker", "Kubernetes", 
    "Terraform", "Ansible", "AWS", "Azure", "GCP", "Google Cloud", "PostgreSQL", "MySQL", 
    "MongoDB", "Redis", "Elasticsearch", "Kafka", "GraphQL", "REST API", "Tailwind", "Git"
]

CERTIFICATIONS_PATTERNS = [
    "Security\\+", "Network\\+", "A\\+", "OSCP", "CEH", "CISSP", "CISM", "CISA", 
    "AWS Certified", "Azure Certified", "GCP Certified", "CCNA", "CCNP", "PMP", 
    "Scrum Master", "CKA", "CKAD", "TOGAF"
]

EDUCATION_PATTERNS = [
    "Bachelor", "B\\.S\\.", "B\\.Sc", "Master", "M\\.S\\.", "M\\.Sc", "Ph\\.D", 
    "Computer Science", "Software Engineering", "Information Technology", "Cybersecurity", "Diploma"
]

def extract_structured_requirements(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    
    # Extract programming languages
    found_languages = []
    for lang in LANGUAGES_PATTERNS:
        if re.search(r'\b' + lang + r'\b', text, re.IGNORECASE):
            # Clean display name
            display_name = lang.replace('\\+', '+').replace('\\.', '.')
            if display_name not in found_languages:
                found_languages.append(display_name)

    # Extract tools & frameworks
    found_tools = []
    for tool in TOOLS_FRAMEWORKS_PATTERNS:
        if re.search(r'\b' + tool + r'\b', text, re.IGNORECASE):
            display_name = tool.replace('\\.', '.').replace('\\+', '+')
            if display_name not in found_tools:
                found_tools.append(display_name)

    # Extract certifications
    found_certs = []
    for cert in CERTIFICATIONS_PATTERNS:
        if re.search(r'\b' + cert + r'\b', text, re.IGNORECASE):
            display_name = cert.replace('\\+', '+')
            if display_name not in found_certs:
                found_certs.append(display_name)

    # Extract education
    found_edu = []
    for edu in EDUCATION_PATTERNS:
        if re.search(r'\b' + edu + r'\b', text, re.IGNORECASE):
            display_name = edu.replace('\\.', '.')
            if display_name not in found_edu:
                found_edu.append(display_name)

    # Required experience years extraction
    exp_min = 0
    exp_pref = 0
    exp_matches = re.findall(r'(\d+)\+?\s*(?:-\s*(\d+))?\s*(?:years?|yrs?)\b', text, re.IGNORECASE)
    if exp_matches:
        try:
            years = [int(m[0]) for m in exp_matches if m[0]]
            if years:
                exp_min = min(years)
                exp_pref = max(years)
        except Exception:
            exp_min = 2
            exp_pref = 5
    else:
        if "senior" in text_lower or "lead" in text_lower:
            exp_min, exp_pref = 5, 8
        elif "mid" in text_lower:
            exp_min, exp_pref = 2, 4
        elif "junior" in text_lower or "entry" in text_lower or "intern" in text_lower:
            exp_min, exp_pref = 0, 2
        else:
            exp_min, exp_pref = 1, 3

    # All required skills combined
    required_skills = list(set(found_languages + found_tools))

    # Visa sponsorship search
    visa_sponsorship = "not_mentioned"
    work_visa_support = "Not specified in posting description"
    if re.search(r'(visa sponsorship|work permit|sponsorship available|relocation support|h1b)', text, re.IGNORECASE):
        visa_sponsorship = "yes"
        work_visa_support = "Visa sponsorship or work permit assistance explicitly provided"
    elif re.search(r'(no visa sponsorship|must be authorized|no sponsorship)', text, re.IGNORECASE):
        visa_sponsorship = "no"
        work_visa_support = "Must already possess work authorization"

    # Relocation assistance search
    relocation = "no"
    if re.search(r'(relocation assistance|relocation package|relocation stipend)', text, re.IGNORECASE):
        relocation = "yes"

    return {
        "programming_languages": found_languages,
        "tools_frameworks": found_tools,
        "certifications_required": found_certs,
        "required_education": found_edu,
        "required_skills": required_skills,
        "required_experience_years": {"min": exp_min, "preferred": exp_pref},
        "visa_sponsorship": visa_sponsorship,
        "work_visa_support": work_visa_support,
        "relocation_assistance": relocation
    }

def extract_salary_range(text: str) -> Dict[str, Any]:
    # Look for salary patterns e.g. $80,000 - $120,000 or GH₵ 10,000 - GH₵ 20,000 or $50/hr
    usd_match = re.search(r'\$\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(?:-\s*\$\s*(\d{1,3}(?:,\d{3})+|\d+))?\s*(per year|yr|annually|/yr|/hr|hour)?', text, re.IGNORECASE)
    ghs_match = re.search(r'(?:GHS|GH₵|GH¢)\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(?:-\s*(?:GHS|GH₵|GH¢)?\s*(\d{1,3}(?:,\d{3})+|\d+))?', text, re.IGNORECASE)
    
    if usd_match:
        val1 = int(usd_match.group(1).replace(',', ''))
        val2 = int(usd_match.group(2).replace(',', '')) if usd_match.group(2) else val1
        rate_type = "hourly" if (usd_match.group(3) and "hr" in usd_match.group(3)) else "annual"
        return {
            "salary_range": {"min": val1, "max": val2, "currency": "USD", "type": rate_type},
            "salary_confidence": "exact",
            "salary_transparency": "yes"
        }
    elif ghs_match:
        val1 = int(ghs_match.group(1).replace(',', ''))
        val2 = int(ghs_match.group(2).replace(',', '')) if ghs_match.group(2) else val1
        return {
            "salary_range": {"min": val1, "max": val2, "currency": "GHS", "type": "monthly"},
            "salary_confidence": "exact",
            "salary_transparency": "yes"
        }

    return {
        "salary_range": {"min": 0, "max": 0, "currency": "USD", "type": "annual"},
        "salary_confidence": "not_provided",
        "salary_transparency": "no"
    }
