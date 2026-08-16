import sqlite3
import json
import os
import datetime
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "/home/kali/Projects/antigravity_job_scraper/data/jobs.db", json_path: str = "/home/kali/Projects/antigravity_job_scraper/data/jobs_database.json"):
        self.db_path = db_path
        self.json_path = json_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_sqlite()

    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_title TEXT,
                    company_name TEXT,
                    location TEXT,
                    work_location_type TEXT,
                    country TEXT,
                    posting_date TEXT,
                    source TEXT,
                    source_url TEXT,
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
            conn.commit()

    def save_jobs(self, jobs: List[Dict[str, Any]]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for j in jobs:
                sal = j.get("salary_range", {})
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs 
                    (job_id, job_title, company_name, location, work_location_type, country, posting_date, source, source_url, salary_min, salary_max, currency, verification_status, company_verified, posting_active, last_checked, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    j["job_id"],
                    j["job_title"],
                    j["company_name"],
                    j["location"],
                    j["work_location_type"],
                    j["country"],
                    j["posting_date"],
                    j["source"],
                    j["source_url"],
                    sal.get("min", 0),
                    sal.get("max", 0),
                    sal.get("currency", "USD"),
                    j["verification_status"],
                    j["company_verified"],
                    j["posting_active"],
                    j["last_checked"],
                    json.dumps(j)
                ))
            conn.commit()

        # Update cumulative JSON database
        all_jobs = self.get_all_jobs()
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, indent=2)

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT raw_data FROM jobs ORDER BY posting_date DESC')
            rows = cursor.fetchall()
            return [json.loads(r[0]) for r in rows]

    def get_active_verified_jobs(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT raw_data FROM jobs WHERE posting_active = "yes" ORDER BY posting_date DESC')
            rows = cursor.fetchall()
            return [json.loads(r[0]) for r in rows]
