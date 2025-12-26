import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from infrastructure.scraping.scrapers.base_scraper import BaseScraper
import time
import random
from config import FLASHSCORE_BASE_URL

class FlashscorePage(BaseScraper):
    BASE_URL = FLASHSCORE_BASE_URL

    def open(self):
        self.open_url(self.BASE_URL)
    
    def open_results_page(self, league_url_path: str, season: str = None):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/results/"
        if season:
            full_url += f"#/season/{season}/"
        self.open_url(full_url)
    
    def wait_for_page_load(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".event__match, [class*='event__match']"))
            )
        except:
            pass

    def goto_match_results(self, league_url_path: str):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/results/"
        self.open_url(full_url)
        self.wait_for_page_load()

    def goto_league_fixtures(self, league_url_path: str):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/fixtures/"
        self.open_url(full_url)
        self.wait_for_page_load()
    
    def goto_standings(self, nation: str, league_name: str, league_id: str):
        url = f"{self.BASE_URL}/soccer/{nation}/{league_name}/standings/#/{league_id}/standings/overall/"
        self.driver.get(url)
        time.sleep(random.uniform(2, 4))
        self.wait_for_element("div.ui-table__body", timeout=10)
