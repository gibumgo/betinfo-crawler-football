import config
from domain.models.flashscore_match import FlashscoreMatch
from domain.models.league import League
from domain.models.team import Team
from domain.models.league_team import LeagueTeam
from domain.models.league_team import LeagueTeam
from infrastructure.repositories.csv_repository import CsvRepository
import pandas as pd
import os
from datetime import datetime
from typing import Optional


class FlashscoreRepository(CsvRepository):
    def save_matches(self, filename: str, matches: list[FlashscoreMatch], append: bool = False):
        self.save_to_csv(matches, filename, append=append, deduplicate=True, deduplicate_subset=['match_id'])

    def save_leagues(self, leagues: list[League]):
        self.save_to_csv(leagues, config.DEFAULT_LEAGUES_CSV_PATH, append=True, deduplicate=True, deduplicate_subset=['league_id'])

    def save_teams(self, teams: list[Team], nation: str):
        self.save_to_csv(teams, config.DEFAULT_TEAMS_CSV_PATH, append=True, deduplicate=True, deduplicate_subset=['team_id'])

    def save_league_teams(self, league_teams: list[LeagueTeam]):
        self.save_to_csv(league_teams, config.LEAGUE_TEAMS_FILENAME, append=True, deduplicate=True)

    def get_latest_match_time(self, filename: str) -> Optional[datetime]:
        if not os.path.exists(filename):
            return None
        try:
            df = pd.read_csv(filename)
            if 'time' not in df.columns or df.empty:
                return None
            
            df['time'] = pd.to_datetime(df['time'])
            return df['time'].max()
        except Exception as e:
            print(f"⚠️ Error reading latest match time from {filename}: {e}")
            return None
