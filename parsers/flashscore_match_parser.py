import re
from datetime import datetime
from selenium.webdriver.common.by import By
from domain.models.flashscore_match import FlashscoreMatch

class MatchParser:
    @staticmethod
    def parse_matches(driver, league_id: int, season: str = "2025-2026", start_round: int = None, end_round: int = None) -> list:
        match_list = []
        elements = driver.find_elements(By.CSS_SELECTOR, ".event__match, .event__round")
        
        current_round = 0
        current_year = datetime.now().year
        match_count = 0
        
        latest_round_detected = None
        
        for elem in elements:
            try:
                classes = elem.get_attribute("class")
                if "event__round" in classes:
                    round_text = elem.text.strip()
                    current_round = FlashscoreMatch.parse_round_number(round_text)
                    
                    if start_round is None:
                        if latest_round_detected is None:
                            latest_round_detected = current_round
                        elif current_round != latest_round_detected:
                            break
                    continue

                if start_round is not None and current_round < start_round:
                    continue
                if end_round is not None and current_round > end_round:
                    continue

                if "event__match" in classes:
                    match_count += 1
                    
                    time_str = elem.find_element(By.CSS_SELECTOR, ".event__time").text.strip()
                    try:
                        match_dt = datetime.strptime(f"{current_year}.{time_str}", "%Y.%d.%m. %H:%M")
                    except Exception as e:
                        print(f"Time parsing error ({time_str}): {e}")
                        match_dt = datetime.now()

                    link_elem = elem.find_element(By.CSS_SELECTOR, "a.eventRowLink")
                    href = link_elem.get_attribute("href")
                    
                    url_info = FlashscoreMatch.extract_url_info(href)
                    
                    try:
                        home_name_ko = elem.find_element(By.CSS_SELECTOR, ".event__homeParticipant .wcl-name_jjfMf").text.strip()
                        away_name_ko = elem.find_element(By.CSS_SELECTOR, ".event__awayParticipant .wcl-name_jjfMf").text.strip()
                    except:
                        try:
                            home_name_ko = elem.find_element(By.CSS_SELECTOR, ".event__homeParticipant").text.strip()
                            away_name_ko = elem.find_element(By.CSS_SELECTOR, ".event__awayParticipant").text.strip()
                        except:
                            home_name_ko, away_name_ko = "", ""

                    try:
                        home_score_text = elem.find_element(By.CSS_SELECTOR, ".event__score--home").text.strip()
                        away_score_text = elem.find_element(By.CSS_SELECTOR, ".event__score--away").text.strip()
                        home_score = int(home_score_text)
                        away_score = int(away_score_text)
                    except:
                        home_score, away_score = None, None

                    match_list.append(FlashscoreMatch.create(
                        id=match_count,
                        league_id=league_id,
                        home_team_name=home_name_ko,
                        away_team_name=away_name_ko,
                        url_team1_name_en=url_info["t1_slug"],
                        url_team2_name_en=url_info["t2_slug"],
                        url_team1_id=url_info["t1_id"],
                        url_team2_id=url_info["t2_id"],
                        match_datetime=match_dt.strftime("%Y-%m-%d %H:%M:%S"),
                        round=current_round,
                        season=season,
                        home_score=home_score,
                        away_score=away_score,
                        flashscore_match_id=url_info["match_id"]
                    ))
            except Exception as e:
                print(f"Match parse error: {e}")
                
        return match_list
