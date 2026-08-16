import schedule
import time
import json
import logging
import datetime
from scrapers.scraper_manager import ScraperManager
from engine.deduplicator import deduplicate_jobs
from engine.legitimacy_checker import verify_url_active, inspect_job_legitimacy
from storage.db_manager import DatabaseManager
from storage.exporter import DataExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class JobScraperScheduler:
    def __init__(self, config_path: str = "/home/kali/Projects/antigravity_job_scraper/config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.db = DatabaseManager()
        self.exporter = DataExporter()
        self.manager = ScraperManager(self.config)

    def run_full_scrape(self):
        logging.info("Starting scheduled Full Scrape...")
        raw_jobs = self.manager.run_all()
        existing_jobs = self.db.get_all_jobs()
        unique_jobs, updated_all = deduplicate_jobs(raw_jobs, existing_jobs)
        self.db.save_jobs(updated_all)
        self.exporter.export_csv(updated_all)
        self.exporter.export_markdown_report(updated_all)
        logging.info(f"Full Scrape complete. {len(unique_jobs)} new jobs added. Total stored: {len(updated_all)}")

    def run_light_check(self):
        logging.info("Starting scheduled Lightweight Check...")
        raw_jobs = self.manager.run_all()
        existing_jobs = self.db.get_all_jobs()
        unique_jobs, updated_all = deduplicate_jobs(raw_jobs, existing_jobs)
        if unique_jobs:
            self.db.save_jobs(updated_all)
            self.exporter.export_csv(updated_all)
        logging.info(f"Lightweight check complete. {len(unique_jobs)} new jobs found.")

    def run_verification_cycle(self):
        logging.info("Starting scheduled Verification Cycle...")
        all_jobs = self.db.get_all_jobs()
        modified = 0
        for j in all_jobs:
            # Check URL activity
            active = verify_url_active(j.get("source_url", ""))
            v_status, c_verified, p_active = inspect_job_legitimacy(j)
            if not active:
                p_active = "no"
                v_status = "expired"
            j["verification_status"] = v_status
            j["company_verified"] = c_verified
            j["posting_active"] = p_active
            j["last_checked"] = datetime.datetime.utcnow().isoformat() + "Z"
            modified += 1
        self.db.save_jobs(all_jobs)
        logging.info(f"Verification cycle complete. Verified {modified} jobs.")

    def start_schedules(self):
        # Register schedules
        schedule.every().day.at("06:00").do(self.run_full_scrape)
        schedule.every().day.at("14:00").do(self.run_light_check)
        schedule.every().day.at("22:00").do(self.run_light_check)
        schedule.every(2).days.at("03:00").do(self.run_verification_cycle)
        logging.info("Scheduler initialized with defined UTC cron intervals.")

    def run_pending(self):
        schedule.run_pending()

if __name__ == "__main__":
    scheduler = JobScraperScheduler()
    scheduler.start_schedules()
    logging.info("Scheduler loop started. Performing initial execution...")
    scheduler.run_full_scrape()
    while True:
        scheduler.run_pending()
        time.sleep(60)
