from datetime import datetime
from selenium.webdriver.common.by import By
from domain.models.flashscore_match import FlashscoreMatch


class MatchExtractor:
    @staticmethod
    def extract_datetime(match_row, year):
        time_text = match_row.find_element(By.CSS_SELECTOR, ".event__time").text.strip()
        try:
            return datetime.strptime(f"{year}.{time_text}", "%Y.%d.%m. %H:%M")
        except Exception as error:
            print(f"Time parsing error ({time_text}): {error}")
            return datetime.now()

    @staticmethod
    def extract_teams(match_row):
        try:
            home = match_row.find_element(By.CSS_SELECTOR, ".event__homeParticipant .wcl-name_jjfMf").text.strip()
            away = match_row.find_element(By.CSS_SELECTOR, ".event__awayParticipant .wcl-name_jjfMf").text.strip()
            return home, away
        except:
            try:
                home = match_row.find_element(By.CSS_SELECTOR, ".event__homeParticipant").text.strip()
                away = match_row.find_element(By.CSS_SELECTOR, ".event__awayParticipant").text.strip()
                return home, away
            except:
                return "", ""

    @staticmethod
    def extract_scores(match_row):
        try:
            h_text = match_row.find_element(By.CSS_SELECTOR, ".event__score--home").text.strip()
            a_text = match_row.find_element(By.CSS_SELECTOR, ".event__score--away").text.strip()
            return int(h_text), int(a_text)
        except:
            return None, None

    @staticmethod
    def extract_url_info(match_row):
        link_elem = match_row.find_element(By.CSS_SELECTOR, "a.eventRowLink")
        url = link_elem.get_attribute("href")
        return FlashscoreMatch.extract_url_info(url)
