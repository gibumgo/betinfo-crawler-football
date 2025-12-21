from selenium.webdriver.common.by import By
from domain.models.flashscore_match import FlashscoreMatch

class MatchParser:
    @staticmethod
    def parse_matches(driver, league_id: int, season: str = "2025-2026", start_round: int = None, end_round: int = None) -> list[FlashscoreMatch]:
        match_list = []
        web_elements = driver.find_elements(By.CSS_SELECTOR, ".event__match, .event__round")
        
        parsing_context = {
            "current_round": 0, 
            "match_count": 0, 
            "latest_round": None, 
            "is_collection_finished": False
        }
        
        for element in web_elements:
            match_object = MatchParser._process_element(
                element, 
                parsing_context, 
                start_round, 
                end_round, 
                league_id, 
                season
            )
            
            if parsing_context["is_collection_finished"]: 
                break
                
            if match_object: 
                match_list.append(match_object)
                
        return match_list

    @staticmethod
    def _process_element(element, context, start_round, end_round, league_id, season) -> FlashscoreMatch:
        try:
            class_names = element.get_attribute("class")
            
            if MatchParser._is_round_header(class_names):
                MatchParser._handle_round_header(element, context, start_round)
                return None

            if not MatchParser._is_target_match(context["current_round"], start_round, end_round, class_names):
                return None

            return MatchParser._handle_match_row(element, context, league_id, season)
        except Exception as e:
            print(f"Match parse error: {e}")
            return None

    @staticmethod
    def _handle_round_header(element, context, start_round):
        context["current_round"] = FlashscoreMatch.parse_round_number(element.text)
        
        if start_round is not None: 
            return
            
        if context["latest_round"] is None: 
            context["latest_round"] = context["current_round"]
            return
            
        if context["current_round"] != context["latest_round"]: 
            context["is_collection_finished"] = True

    @staticmethod
    def _handle_match_row(element, context, league_id, season) -> FlashscoreMatch:
        context["match_count"] += 1
        extracted_data = MatchParser._extract_row_data(element)
        extracted_data.update({
            "id": context["match_count"], 
            "league_id": league_id, 
            "round": context["current_round"], 
            "season": season
        })
        return FlashscoreMatch.of(extracted_data)

    @staticmethod
    def _is_target_match(current_round, start_round, end_round, class_names) -> bool:
        if not MatchParser._is_in_range(current_round, start_round, end_round): 
            return False
        if not MatchParser._is_match_row(class_names): 
            return False
        return True

    @staticmethod
    def _is_round_header(class_names: str) -> bool:
        return "event__round" in class_names

    @staticmethod
    def _is_match_row(class_names: str) -> bool:
        return "event__match" in class_names

    @staticmethod
    def _is_in_range(current: int, start: int, end: int) -> bool:
        if start is not None and current < start: return False
        if end is not None and current > end: return False
        return True

    @staticmethod
    def _extract_row_data(element) -> dict:
        match_time_raw = element.find_element(By.CSS_SELECTOR, ".event__time").text.strip()
        match_link_element = element.find_element(By.CSS_SELECTOR, "a.eventRowLink")
        url_info = FlashscoreMatch.extract_url_info(match_link_element.get_attribute("href"))
        home_team, away_team = MatchParser._extract_team_names(element)
        home_score, away_score = MatchParser._extract_scores(element)
        
        return {
            "time": match_time_raw,
            "url_info": url_info,
            "home": home_team,
            "away": away_team,
            "h_score": home_score,
            "a_score": away_score
        }

    @staticmethod
    def _extract_team_names(element) -> tuple:
        try:
            home = element.find_element(By.CSS_SELECTOR, ".event__homeParticipant .wcl-name_jjfMf").text.strip()
            away = element.find_element(By.CSS_SELECTOR, ".event__awayParticipant .wcl-name_jjfMf").text.strip()
        except:
            home = element.find_element(By.CSS_SELECTOR, ".event__homeParticipant").text.strip()
            away = element.find_element(By.CSS_SELECTOR, ".event__awayParticipant").text.strip()
        return home, away

    @staticmethod
    def _extract_scores(element) -> tuple:
        try:
            home_score_text = element.find_element(By.CSS_SELECTOR, ".event__score--home").text.strip()
            away_score_text = element.find_element(By.CSS_SELECTOR, ".event__score--away").text.strip()
            return home_score_text, away_score_text
        except:
            return None, None
