import logging
from typing import List, Dict, Any
from scrapers.remotive_scraper import RemotiveScraper
from scrapers.weworkremotely_scraper import WeWorkRemotelyScraper
from scrapers.jobberman_scraper import JobbermanScraper
from scrapers.myjobmag_scraper import MyJobMagScraper
from scrapers.tonaton_scraper import TonatonScraper
from scrapers.relocateme_scraper import RelocateMeScraper
from scrapers.jobhouse_scraper import JobhouseScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.glassdoor_scraper import GlassdoorScraper
from scrapers.wellfound_scraper import WellfoundScraper
from scrapers.company_careers_scraper import CompanyCareersScraper

class ScraperManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("ANTIGRAVITY_JOB_SCRAPER", {})
        self.sources_cfg = self.config.get("sources", {})
        self.scrapers = []
        
        if self.sources_cfg.get("remotive", {}).get("enabled", True):
            self.scrapers.append(RemotiveScraper(self.sources_cfg.get("remotive", {}).get("rate_limit_per_min", 15)))
        if self.sources_cfg.get("weworkremotely", {}).get("enabled", True):
            self.scrapers.append(WeWorkRemotelyScraper(self.sources_cfg.get("weworkremotely", {}).get("rate_limit_per_min", 10)))
        if self.sources_cfg.get("jobberman", {}).get("enabled", True):
            self.scrapers.append(JobbermanScraper(self.sources_cfg.get("jobberman", {}).get("rate_limit_per_min", 12)))
        if self.sources_cfg.get("myjobmag", {}).get("enabled", True):
            self.scrapers.append(MyJobMagScraper(self.sources_cfg.get("myjobmag", {}).get("rate_limit_per_min", 10)))
        if self.sources_cfg.get("tonaton", {}).get("enabled", True):
            self.scrapers.append(TonatonScraper(self.sources_cfg.get("tonaton", {}).get("rate_limit_per_min", 10)))
        if self.sources_cfg.get("relocateme", {}).get("enabled", True):
            self.scrapers.append(RelocateMeScraper(self.sources_cfg.get("relocateme", {}).get("rate_limit_per_min", 8)))
        if self.sources_cfg.get("jobhouse", {}).get("enabled", True):
            self.scrapers.append(JobhouseScraper(self.sources_cfg.get("jobhouse", {}).get("rate_limit_per_min", 10)))
        if self.sources_cfg.get("linkedin", {}).get("enabled", True):
            self.scrapers.append(LinkedInScraper(self.sources_cfg.get("linkedin", {}).get("rate_limit_per_min", 10)))
        if self.sources_cfg.get("glassdoor", {}).get("enabled", True):
            self.scrapers.append(GlassdoorScraper(self.sources_cfg.get("glassdoor", {}).get("rate_limit_per_min", 5)))
        if self.sources_cfg.get("wellfound", {}).get("enabled", True):
            self.scrapers.append(WellfoundScraper(self.sources_cfg.get("wellfound", {}).get("rate_limit_per_min", 8)))
        if self.sources_cfg.get("company_careers", {}).get("enabled", True):
            self.scrapers.append(CompanyCareersScraper(self.sources_cfg.get("company_careers", {}).get("rate_limit_per_min", 10)))

    def run_all(self) -> List[Dict[str, Any]]:
        all_jobs = []
        for scraper in self.scrapers:
            try:
                logging.info(f"Running scraper: {scraper.source_name}...")
                jobs = scraper.scrape()
                logging.info(f"Source {scraper.source_name} returned {len(jobs)} jobs.")
                all_jobs.extend(jobs)
            except Exception as e:
                logging.error(f"Error running scraper {scraper.source_name}: {e}")
        return all_jobs
