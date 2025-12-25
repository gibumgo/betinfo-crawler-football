import re
from datetime import datetime
from bs4 import Tag

class MatchExtractor:
    CSS_TIME = ".event__time"
    CSS_PARTICIPANTS = ".event__participant"
    CSS_HOME_PARTICIPANT_NAME = ".event__homeParticipant [class*='wcl-name_']"
    CSS_AWAY_PARTICIPANT_NAME = ".event__awayParticipant [class*='wcl-name_']"
    CSS_HOME_PARTICIPANT = ".event__homeParticipant"
    CSS_AWAY_PARTICIPANT = ".event__awayParticipant"
    
    CSS_SCORE_HOME = ".event__score--home"
    CSS_SCORE_AWAY = ".event__score--away"
    CSS_MATCH_LINK = "a.eventRowLink"
    
    DATE_FORMAT_KO = "(%m.%d. %H:%M)"
    DATE_FORMAT_EN = "(%d.%m. %H:%M)"
    DATE_FORMAT_PARSE = "%Y.%d.%m. %H:%M"
    
    @staticmethod
    def extract_datetime(match_row: Tag, year: int):
        element = match_row.select_one(MatchExtractor.CSS_TIME)
        if not element:
            return datetime.now()

        time_text = element.get_text(strip=True)
        time_text = time_text.strip('()')
        try:
            return datetime.strptime(f"{year}.{time_text}", MatchExtractor.DATE_FORMAT_PARSE)
        except Exception as error:
            print(f"Time parsing error ({time_text}): {error}")
            return datetime.now()

    @staticmethod
    def extract_teams(match_row: Tag):
        try:
            home_elem = match_row.select_one(MatchExtractor.CSS_HOME_PARTICIPANT_NAME)
            away_elem = match_row.select_one(MatchExtractor.CSS_AWAY_PARTICIPANT_NAME)
            
            if not home_elem:
                home_elem = match_row.select_one(MatchExtractor.CSS_HOME_PARTICIPANT)
            if not away_elem:
                away_elem = match_row.select_one(MatchExtractor.CSS_AWAY_PARTICIPANT)

            home_team = home_elem.get_text(strip=True) if home_elem else ""
            away_team = away_elem.get_text(strip=True) if away_elem else ""
            return home_team, away_team
        except:
            return "", ""

    @staticmethod
    def extract_scores(match_row: Tag):
        try:
            home_elem = match_row.select_one(MatchExtractor.CSS_SCORE_HOME)
            away_elem = match_row.select_one(MatchExtractor.CSS_SCORE_AWAY)
            
            if home_elem and away_elem:
                return int(home_elem.get_text(strip=True)), int(away_elem.get_text(strip=True))
            return None, None
        except:
            return None, None

    @staticmethod
    def extract_url_info(match_row: Tag):
        link_element = match_row.select_one(MatchExtractor.CSS_MATCH_LINK)
        if link_element and link_element.has_attr("href"):
            match_url = link_element["href"]
            from domain.models.flashscore_match import FlashscoreMatch
            return FlashscoreMatch.extract_url_info(match_url)
        return {"t1_slug": "", "t2_slug": "", "t1_id": "", "t2_id": "", "match_id": ""}
