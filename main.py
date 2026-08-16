import sys
import os
import argparse
import json
import logging

from scrapers.scraper_manager import ScraperManager
from engine.deduplicator import deduplicate_jobs
from engine.legitimacy_checker import inspect_job_legitimacy, verify_url_active
from storage.db_manager import DatabaseManager
from storage.exporter import DataExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Job Scraper CLI")
    parser.add_argument("--scrape", action="store_true", help="Run full scrape across all enabled sources")
    parser.add_argument("--verify", action="store_true", help="Run verification check on all stored jobs")
    parser.add_argument("--export", action="store_true", help="Export CSV, JSON, and Markdown reports")
    parser.add_argument("--server", action="store_true", help="Start FastAPI web dashboard server")
    parser.add_argument("--port", type=int, default=8000, help="Port for web dashboard server")
    args = parser.parse_args()

    db = DatabaseManager()
    exporter = DataExporter()

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if args.scrape or (not args.verify and not args.export and not args.server):
        logging.info("Starting Scraper execution...")
        manager = ScraperManager(config)
        raw_jobs = manager.run_all()
        existing_jobs = db.get_all_jobs()
        unique_jobs, updated_all = deduplicate_jobs(raw_jobs, existing_jobs)
        db.save_jobs(updated_all)
        csv_file = exporter.export_csv(updated_all)
        md_file = exporter.export_markdown_report(updated_all)
        logging.info(f"Scrape completed successfully!")
        logging.info(f"Total raw fetched: {len(raw_jobs)}")
        logging.info(f"New unique listings: {len(unique_jobs)}")
        logging.info(f"Total listings in database: {len(updated_all)}")
        logging.info(f"CSV Export: {csv_file}")
        logging.info(f"Markdown Report: {md_file}")

    if args.verify:
        logging.info("Starting Verification Pipeline...")
        all_jobs = db.get_all_jobs()
        for j in all_jobs:
            v_status, c_verified, p_active = inspect_job_legitimacy(j)
            j["verification_status"] = v_status
            j["company_verified"] = c_verified
            j["posting_active"] = p_active
        db.save_jobs(all_jobs)
        logging.info(f"Verified {len(all_jobs)} job listings.")

    if args.export:
        all_jobs = db.get_all_jobs()
        csv_f = exporter.export_csv(all_jobs)
        md_f = exporter.export_markdown_report(all_jobs)
        logging.info(f"Exported CSV: {csv_f}")
        logging.info(f"Exported Markdown Report: {md_f}")

    if args.server:
        import uvicorn
        logging.info(f"Starting Web Dashboard server on http://0.0.0.0:{args.port}...")
        uvicorn.run("server:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
