from dataclasses import dataclass
import config
from typing import Optional

@dataclass
class LeagueTarget:
    nation: str
    league_name: str
    league_id: str
    season: str

    def get_matches_url(self) -> str:
        return config.FS_RESULTS_URL_TEMPLATE.format(
            base_url=config.FLASHSCORE_BASE_URL,
            nation=self.nation,
            league=self.league_name,
            season=self.season
        )

    def get_summary_url(self) -> str:
        return config.FS_SUMMARY_URL_TEMPLATE.format(
            base_url=config.FLASHSCORE_BASE_URL,
            nation=self.nation,
            league=self.league_name,
            season=self.season,
            league_id=self.league_id
        )

    @property
    def season_start_year(self) -> int:
        try:
            return int(self.season.split("-")[0])
        except (ValueError, IndexError):
            return 0
