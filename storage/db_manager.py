import sqlite3
import json
import os
import datetime
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IS_VERCEL = os.environ.get("VERCEL", "0") == "1" or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

def get_writable_dir() -> str:
    if IS_VERCEL:
        return "/tmp"
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

class DatabaseManager:
    def __init__(self, db_path: str = None, json_path: str = None):
        target_dir = get_writable_dir()
        self.db_path = db_path or os.path.join(target_dir, "jobs.db")
        self.json_path = json_path or os.path.join(target_dir, "jobs_database.json")
        self.seed_json_path = os.path.join(BASE_DIR, "data", "jobs_database.json")
        
        self._init_sqlite()
        self._seed_if_empty()

    def _init_sqlite(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_title TEXT,
                    company_name TEXT,
                    company_website TEXT,
                    location TEXT,
                    work_location_type TEXT,
                    country TEXT,
                    posting_date TEXT,
                    source TEXT,
                    source_url TEXT,
                    source_portal_url TEXT,
                    salary_min REAL,
                    salary_max REAL,
                    currency TEXT,
                    verification_status TEXT,
                    company_verified TEXT,
                    posting_active TEXT,
                    last_checked TEXT,
                    raw_data TEXT
                )
            ''')
            # Migration check for existing DB
            cursor.execute("PRAGMA table_info(jobs)")
            cols = [c[1] for c in cursor.fetchall()]
            if "company_website" not in cols:
                cursor.execute("ALTER TABLE jobs ADD COLUMN company_website TEXT")
            if "source_portal_url" not in cols:
                cursor.execute("ALTER TABLE jobs ADD COLUMN source_portal_url TEXT")
            conn.commit()

    def _seed_if_empty(self):
        all_jobs = self.get_all_jobs()
        if not all_jobs and os.path.exists(self.seed_json_path):
            try:
                with open(self.seed_json_path, 'r', encoding='utf-8') as f:
                    seed_data = json.load(f)
                    if isinstance(seed_data, list) and len(seed_data) > 0:
                        self.save_jobs(seed_data)
            except Exception as e:
                print(f"Error seeding initial database: {e}")

    def save_jobs(self, jobs: List[Dict[str, Any]]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for j in jobs:
                sal = j.get("salary_range", {})
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs 
                    (job_id, job_title, company_name, company_website, location, work_location_type, country, posting_date, source, source_url, source_portal_url, salary_min, salary_max, currency, verification_status, company_verified, posting_active, last_checked, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    j.get("job_id"),
                    j.get("job_title"),
                    j.get("company_name"),
                    j.get("company_website"),
                    j.get("location"),
                    j.get("work_location_type"),
                    j.get("country"),
                    j.get("posting_date"),
                    j.get("source"),
                    j.get("source_url"),
                    j.get("source_portal_url", "https://remotive.com"),
                    sal.get("min", 0),
                    sal.get("max", 0),
                    sal.get("currency", "USD"),
                    j.get("verification_status", "verified"),
                    j.get("company_verified", "yes"),
                    j.get("posting_active", "yes"),
                    j.get("last_checked", datetime.datetime.utcnow().isoformat() + "Z"),
                    json.dumps(j)
                ))
            conn.commit()

        all_jobs = self.get_all_jobs()
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(all_jobs, f, indent=2)
        except Exception:
            pass

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT raw_data FROM jobs WHERE posting_active = "yes" ORDER BY posting_date DESC')
                rows = cursor.fetchall()
                if rows:
                    return [json.loads(r[0]) for r in rows]
        except Exception as e:
            print(f"Database fetch error: {e}")

        if os.path.exists(self.seed_json_path):
            try:
                with open(self.seed_json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def get_active_verified_jobs(self) -> List[Dict[str, Any]]:
        jobs = self.get_all_jobs()
        return [j for j in jobs if j.get("posting_active") == "yes" and j.get("verification_status") == "verified"]
