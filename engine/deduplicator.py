import hashlib
import re
from typing import List, Dict, Any, Tuple

def compute_job_hash(title: str, company: str, location: str) -> str:
    clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
    clean_company = re.sub(r'[^a-zA-Z0-9]', '', company.lower())
    clean_loc = re.sub(r'[^a-zA-Z0-9]', '', location.lower())
    raw_key = f"{clean_company}_{clean_title}_{clean_loc}"
    return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()[:16]

def calculate_text_similarity(text1: str, text2: str) -> float:
    # Jaccard similarity of 3-gram sets for fast text hashing matching
    if not text1 or not text2:
        return 0.0
    
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
        
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)

def deduplicate_jobs(new_jobs: List[Dict[str, Any]], existing_jobs: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Deduplicates incoming jobs against existing database.
    Returns (filtered_unique_jobs, updated_all_jobs)
    """
    existing_hashes = {compute_job_hash(j["job_title"], j["company_name"], j["location"]): j for j in existing_jobs}
    
    unique_new = []
    
    for job in new_jobs:
        job_h = compute_job_hash(job["job_title"], job["company_name"], job["location"])
        
        if job_h in existing_hashes:
            # Check if new version has richer details (e.g. longer description or salary provided)
            existing_item = existing_hashes[job_h]
            sim = calculate_text_similarity(job["job_description_raw"], existing_item["job_description_raw"])
            
            if sim >= 0.85:
                # Duplicate found! Keep the one with better quality/more recent timestamp
                if len(job["job_description_raw"]) > len(existing_item["job_description_raw"]):
                    existing_hashes[job_h] = job
                continue
                
        existing_hashes[job_h] = job
        unique_new.append(job)
        
    return unique_new, list(existing_hashes.values())
