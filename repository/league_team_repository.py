from repository.base_repository import BaseRepository
from domain.models.league_team import LeagueTeam

class LeagueTeamRepository(BaseRepository):
    COLUMN_MAP = {
        "league_id": "리그ID",
        "team_id": "팀ID",
        "season": "시즌"
    }
    
    def __init__(self):
        super().__init__(self.COLUMN_MAP)
    
    def save(self, league_teams: list[LeagueTeam], filename: str = "league_team.csv") -> None:
        self.save_to_csv(league_teams, filename)
