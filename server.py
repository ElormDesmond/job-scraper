import os
import json
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from scrapers.scraper_manager import ScraperManager
from engine.deduplicator import deduplicate_jobs
from engine.legitimacy_checker import verify_url_active, inspect_job_legitimacy
from storage.db_manager import DatabaseManager
from storage.exporter import DataExporter

app = FastAPI(title="Antigravity Job Scraper & Monitoring System", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
PREFS_PATH = os.path.join(BASE_DIR, "user_preferences.json")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

db = DatabaseManager()
exporter = DataExporter()

# Mount dashboard static files if directory exists
if os.path.exists(DASHBOARD_DIR):
    app.mount("/static", StaticFiles(directory=DASHBOARD_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_file = os.path.join(DASHBOARD_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Antigravity Job Scraper API Running</h1>"

@app.get("/api/jobs")
def get_jobs(
    query: str = "",
    location: str = "",
    category: str = "",
    visa_only: bool = False,
    diversity_only: bool = False,
    min_salary: int = 0
):
    jobs = db.get_all_jobs()
    filtered = []
    for j in jobs:
        if query and not (query.lower() in (j.get("job_title") or "").lower() or query.lower() in (j.get("company_name") or "").lower() or query.lower() in (j.get("job_description_raw") or "").lower()):
            continue
        if location and not (location.lower() in (j.get("location") or "").lower() or location.lower() in (j.get("country") or "").lower()):
            continue
        if category and not (category.lower() in (j.get("job_title") or "").lower() or any(category.lower() in k.lower() for k in j.get("required_skills", []))):
            continue
        if visa_only and j.get("visa_sponsorship") not in ["yes", "case_by_case"]:
            continue
        if diversity_only and len(j.get("diversity_badges", [])) == 0:
            continue
        sal = j.get("salary_range", {})
        sal_min = sal.get("min", 0)
        if min_salary > 0 and sal_min > 0 and sal_min < min_salary:
            continue
        filtered.append(j)
    return {"status": "success", "count": len(filtered), "data": filtered}

@app.post("/api/scrape")
def trigger_scrape():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    manager = ScraperManager(config)
    raw_jobs = manager.run_all()
    existing_jobs = db.get_all_jobs()
    unique_jobs, updated_all = deduplicate_jobs(raw_jobs, existing_jobs)
    db.save_jobs(updated_all)
    csv_file = exporter.export_csv(updated_all)
    md_file = exporter.export_markdown_report(updated_all)
    return {
        "status": "success",
        "message": f"Scrape completed. Found {len(raw_jobs)} total, {len(unique_jobs)} new unique jobs.",
        "new_jobs_count": len(unique_jobs),
        "total_jobs_count": len(updated_all),
        "exports": {"csv": csv_file, "markdown": md_file}
    }

@app.post("/api/verify")
def trigger_verification():
    all_jobs = db.get_all_jobs()
    updated_count = 0
    for j in all_jobs:
        v_status, c_verified, p_active = inspect_job_legitimacy(j)
        j["verification_status"] = v_status
        j["company_verified"] = c_verified
        j["posting_active"] = p_active
        j["last_checked"] = datetime.datetime.utcnow().isoformat() + "Z"
        updated_count += 1
    db.save_jobs(all_jobs)
    return {"status": "success", "verified_count": updated_count}

@app.get("/api/export/csv")
def download_csv():
    jobs = db.get_all_jobs()
    filepath = exporter.export_csv(jobs)
    return FileResponse(filepath, media_type="text/csv", filename=os.path.basename(filepath))

@app.get("/api/export/json")
def download_json():
    jobs = db.get_all_jobs()
    json_path = os.path.join(exporter.output_dir, "jobs_database.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2)
    return FileResponse(json_path, media_type="application/json", filename="jobs_database.json")

@app.get("/api/export/markdown")
def download_markdown():
    jobs = db.get_all_jobs()
    filepath = exporter.export_markdown_report(jobs)
    return FileResponse(filepath, media_type="text/markdown", filename=os.path.basename(filepath))

@app.get("/api/preferences")
def get_preferences():
    if os.path.exists(PREFS_PATH):
        with open(PREFS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

class PrefsModel(BaseModel):
    preferred_locations: list
    job_categories: list
    min_salary_usd: int
    must_include_sponsorship: bool
    prefer_diversity_roles: bool
    experience_level: str

@app.post("/api/preferences")
def update_preferences(prefs: PrefsModel):
    try:
        with open(PREFS_PATH, 'w', encoding='utf-8') as f:
            json.dump(prefs.dict(), f, indent=2)
    except Exception:
        pass
    return {"status": "success", "data": prefs.dict()}

@app.get("/api/health")
def health_check():
    jobs = db.get_all_jobs()
    ghana_count = len([j for j in jobs if "Ghana" in j.get("country", "") or "Ghana" in j.get("location", "")])
    visa_count = len([j for j in jobs if j.get("visa_sponsorship") in ["yes", "case_by_case"]])
    diversity_count = len([j for j in jobs if len(j.get("diversity_badges", [])) > 0])
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "total_jobs": len(jobs),
        "ghana_jobs": ghana_count,
        "visa_jobs": visa_count,
        "diversity_jobs": diversity_count,
        "sources_active": 6
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8085, reload=False)
