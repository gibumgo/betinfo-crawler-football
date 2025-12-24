import pandas as pd
import os
import config
from domain.models.flashscore_match import FlashscoreMatch
from domain.models.league import League
from domain.models.team import Team
from domain.models.league_team import LeagueTeam


class FlashscoreRepository:
    def save_matches(self, filename: str, matches: list[FlashscoreMatch]):
        data = [match.model_dump() for match in matches]
        df = pd.DataFrame(data)
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ {len(matches)} matches saved to {filename}")

    def save_leagues(self, leagues: list[League]):
        filename = config.LEAGUES_FILENAME
        self._append_to_csv_safe(filename, leagues)


    def save_teams(self, teams: list[Team], nation: str):
        filename = config.TEAMS_FILENAME
        self._append_to_csv_safe(filename, teams)

    def save_league_teams(self, league_teams: list[LeagueTeam]):
        filename = config.LEAGUE_TEAMS_FILENAME
        self._append_to_csv_safe(filename, league_teams)

    def _append_to_csv_safe(self, filename: str, items: list):
        if not items:
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        from dataclasses import asdict, is_dataclass
        
        new_data = []
        for item in items:
            if hasattr(item, 'model_dump'):
                new_data.append(item.model_dump())
            elif is_dataclass(item):
                new_data.append(asdict(item))
            else:
                new_data.append(item.__dict__)
                
        new_df = pd.DataFrame(new_data)
        
        if os.path.exists(filename):
            existing_df = pd.read_csv(filename)
            combined_df = pd.concat([existing_df, new_df])
            combined_df.drop_duplicates(inplace=True)
            combined_df.to_csv(filename, index=False, encoding="utf-8-sig")
        else:
            new_df.to_csv(filename, index=False, encoding="utf-8-sig")
        
        print(f"✅ {len(items)} items processed for {filename}")
