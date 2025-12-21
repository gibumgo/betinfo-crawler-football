from scraper.base_scraper import BaseScraper

class FlashscorePage(BaseScraper):
    BASE_URL = "https://www.flashscore.co.kr"

    def open(self):
        self.open_url(self.BASE_URL)

    def goto_league_standings(self, league_url_path: str):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/standings/"
        self.open_url(full_url)
        self.wait_for_element(".tableCellParticipant__name")

    def goto_team_details(self, team_url_path: str):
        path = team_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/"
        self.open_url(full_url)
        self.wait_for_element(".teamHeader__name")

    def goto_match_results(self, league_url_path: str):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/results/"
        self.open_url(full_url)
        self.wait_for_element(".event__match")

    def goto_league_fixtures(self, league_url_path: str):
        path = league_url_path.rstrip('/')
        full_url = f"{self.BASE_URL}{path}/fixtures/"
        self.open_url(full_url)
        self.wait_for_element(".event__match")

    def click_show_more(self) -> bool:
        """'더 보기' 버튼이 있으면 클릭합니다."""
        try:
            from selenium.webdriver.common.by import By
            show_more_button = self.driver.find_element(By.CSS_SELECTOR, ".event__more")
            self.driver.execute_script("arguments[0].click();", show_more_button)
            return True
        except:
            return False
