import re
from datetime import datetime
from selenium.webdriver.common.by import By


class MatchExtractor:
    CSS_TIME = ".event__time"
    CSS_PARTICIPANTS = ".event__participant"
    CSS_HOME_PARTICIPANT_NAME = ".event__homeParticipant .wcl-name_jjfMf"
    CSS_AWAY_PARTICIPANT_NAME = ".event__awayParticipant .wcl-name_jjfMf"
    CSS_HOME_PARTICIPANT = ".event__homeParticipant"
    CSS_AWAY_PARTICIPANT = ".event__awayParticipant"
    
    CSS_SCORE_HOME = ".event__score--home"
    CSS_SCORE_AWAY = ".event__score--away"
    CSS_MATCH_LINK = "a.eventRowLink"
    
    DATE_FORMAT_KO = "(%m.%d. %H:%M)"
    DATE_FORMAT_EN = "(%d.%m. %H:%M)"
    DATE_FORMAT_PARSE = "%Y.%d.%m. %H:%M"
    
    @staticmethod
    def extract_datetime(match_row, year):
        time_text = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_TIME).text.strip()
        try:
            return datetime.strptime(f"{year}.{time_text}", MatchExtractor.DATE_FORMAT_PARSE)
        except Exception as error:
            print(f"Time parsing error ({time_text}): {error}")
            return datetime.now()

    @staticmethod
    def extract_teams(match_row):
        try:
            home_team = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_HOME_PARTICIPANT_NAME).text.strip()
            away_team = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_AWAY_PARTICIPANT_NAME).text.strip()
            return home_team, away_team
        except:
            try:
                home_team = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_HOME_PARTICIPANT).text.strip()
                away_team = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_AWAY_PARTICIPANT).text.strip()
                return home_team, away_team
            except:
                return "", ""

    @staticmethod
    def extract_scores(match_row):
        try:
            home_score_text = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_SCORE_HOME).text.strip()
            away_score_text = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_SCORE_AWAY).text.strip()
            return int(home_score_text), int(away_score_text)
        except:
            return None, None

    @staticmethod
    def extract_url_info(match_row):
        link_element = match_row.find_element(By.CSS_SELECTOR, MatchExtractor.CSS_MATCH_LINK)
        match_url = link_element.get_attribute("href")
        from domain.models.flashscore_match import FlashscoreMatch
        return FlashscoreMatch.extract_url_info(match_url)
