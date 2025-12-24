import pandas as pd
from dataclasses import asdict
from datetime import datetime
from domain.models.flashscore_match import FlashscoreMatch
from domain.models.league import League
from domain.models.team import Team
from domain.models.league_team import LeagueTeam
from repository.league_repository import LeagueRepository
from repository.team_repository import TeamRepository
from repository.league_team_repository import LeagueTeamRepository

class FlashscoreRepository:
    MATCH_COLUMN_MAP = {
        "id": "경기 id",
        "league_id": "리그ID",
        "home_team_name": "홈팀",
        "away_team_name": "어웨이팀",
        "url_team1_name_en": "팀1 영문 이름",
        "url_team2_name_en": "팀2 영문 이름",
        "url_team1_id": "팀1_ID",
        "url_team2_id": "팀2_ID",
        "match_datetime": "경기일시",
        "round": "라운드",
        "season": "시즌",
        "home_score": "홈점수",
        "away_score": "원정점수",
        "flashscore_match_id": "경기ID"
    }

    def __init__(self):
        self.league_repo = LeagueRepository()
        self.team_repo = TeamRepository()
        self.league_team_repo = LeagueTeamRepository()

    def save_matches(self, filename: str, match_list: list[FlashscoreMatch]) -> None:
        self._save_to_csv(match_list, self.MATCH_COLUMN_MAP, filename)

    def save(self, filename: str, match_list: list[FlashscoreMatch]) -> None:
        self.save_matches(filename, match_list)

    def _save_to_csv(self, items: list, column_map: dict, filename: str) -> None:
        csv_rows = []
        for item in items:
            data_dict = asdict(item)
            
            for key, value in data_dict.items():
                if isinstance(value, datetime):
                    data_dict[key] = value.strftime("%Y-%m-%d %H:%M")
            
            mapped_row = {column_map.get(key, key): value for key, value in data_dict.items()}
            csv_rows.append(mapped_row)

        dataframe = pd.DataFrame(csv_rows)
        dataframe.to_csv(filename, index=False, encoding="utf-8-sig")

    def save_leagues(self, leagues: list[League], filename: str = "league.csv") -> None:
        self.league_repo.save(leagues, filename)
    
    def save_teams(self, teams: list[Team], nation: str = None) -> None:
        self.team_repo.save(teams, nation)
    
    def save_league_teams(self, league_teams: list[LeagueTeam], filename: str = "league_team.csv") -> None:
        self.league_team_repo.save(league_teams, filename)

