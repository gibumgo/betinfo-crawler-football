from datetime import datetime
from selenium.webdriver.common.by import By
from domain.models.flashscore_match import FlashscoreMatch
from parsers.flashscore.round_extractor import RoundExtractor
from parsers.flashscore.match_extractor import MatchExtractor




class MatchParser:
    @staticmethod
    def parse_matches(driver, league_id, season="2025-2026", start_round=None, end_round=None):
        parsed_matches = []
        rows = driver.find_elements(By.CSS_SELECTOR, ".event__match, .event__round")
        
        ctx = {
            "round_num": 0,
            "match_count": 0,
            "year": datetime.now().year,
            "detected_latest": None
        }

        for row in rows:
            try:
                class_names = row.get_attribute("class")

                if "event__round" in class_names:
                    ctx["round_num"], ctx["detected_latest"], stop = RoundExtractor.extract_info(
                        row, start_round, ctx["detected_latest"]
                    )
                    if stop: break
                    continue

                if "event__match" in class_names:
                    match_obj = MatchParser._process_match_row(row, league_id, season, start_round, end_round, ctx)
                    if match_obj:
                        ctx["match_count"] += 1
                        parsed_matches.append(match_obj)

            except Exception as error:
                print(f"Row parsing error: {error}")

        return parsed_matches

    @staticmethod
    def _process_match_row(row, league_id, season, start_round, end_round, ctx):
        if start_round is not None and ctx["round_num"] < start_round: return None
        if end_round is not None and ctx["round_num"] > end_round: return None

        dt = MatchExtractor.extract_datetime(row, ctx["year"])
        teams = MatchExtractor.extract_teams(row)
        scores = MatchExtractor.extract_scores(row)
        url_info = MatchExtractor.extract_url_info(row)

        return FlashscoreMatch.create(
            id=ctx["match_count"] + 1,
            league_id=league_id,
            home_team_name=teams[0],
            away_team_name=teams[1],
            url_team1_name_en=url_info["t1_slug"],
            url_team2_name_en=url_info["t2_slug"],
            url_team1_id=url_info["t1_id"],
            url_team2_id=url_info["t2_id"],
            match_datetime=dt.strftime("%Y-%m-%d %H:%M:%S"),
            round=ctx["round_num"],
            season=season,
            home_score=scores[0],
            away_score=scores[1],
            flashscore_match_id=url_info["match_id"]
        )

