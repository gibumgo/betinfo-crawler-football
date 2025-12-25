from datetime import datetime
from bs4 import BeautifulSoup
from domain.models.flashscore_match import FlashscoreMatch
from infrastructure.scraping.parsers.flashscore.round_extractor import RoundExtractor
from infrastructure.scraping.parsers.flashscore.match_extractor import MatchExtractor
from config import DEFAULT_SEASON


class MatchParser:
    CSS_MATCH_ROWS = ".event__match, .event__round"
    CLASS_EVENT_ROUND = "event__round"
    CLASS_EVENT_MATCH = "event__match"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def parse_matches(html_content, league_id, season=DEFAULT_SEASON, start_round=None, end_round=None):
        parsed_matches = []
        soup = BeautifulSoup(html_content, 'lxml')
        match_rows = soup.select(MatchParser.CSS_MATCH_ROWS)
        
        parsing_state = {
            "round_num": 0,
            "match_count": 0,
            "year": datetime.now().year,
            "detected_latest": None
        }

        for row in match_rows:
            try:
                class_names = row.get("class", [])

                if MatchParser.CLASS_EVENT_ROUND in class_names:
                    parsing_state["round_num"], parsing_state["detected_latest"], stop = RoundExtractor.extract_info(
                        row, start_round, parsing_state["detected_latest"]
                    )
                    if stop: break
                    continue

                if MatchParser.CLASS_EVENT_MATCH in class_names:
                    match_obj = MatchParser._process_match_row(row, league_id, season, start_round, end_round, parsing_state)
                    if match_obj:
                        parsing_state["match_count"] += 1
                        parsed_matches.append(match_obj)

            except Exception as error:
                pass

        return parsed_matches

    @staticmethod
    def _process_match_row(row, league_id, season, start_round, end_round, parsing_state):
        if start_round is not None and parsing_state["round_num"] < start_round: return None
        if end_round is not None and parsing_state["round_num"] > end_round: return None

        match_datetime = MatchExtractor.extract_datetime(row, parsing_state["year"])
        teams = MatchExtractor.extract_teams(row)
        scores = MatchExtractor.extract_scores(row)
        url_info = MatchExtractor.extract_url_info(row)

        return FlashscoreMatch.create(
            id=parsing_state["match_count"] + 1,
            league_id=league_id,
            home_team_name=teams[0],
            away_team_name=teams[1],
            url_team1_name_en=url_info["t1_slug"],
            url_team2_name_en=url_info["t2_slug"],
            url_team1_id=url_info["t1_id"],
            url_team2_id=url_info["t2_id"],
            match_datetime=match_datetime.strftime(MatchParser.DATE_FORMAT),
            round=parsing_state["round_num"],
            season=season,
            home_score=scores[0],
            away_score=scores[1],
            flashscore_match_id=url_info["match_id"]
        )


