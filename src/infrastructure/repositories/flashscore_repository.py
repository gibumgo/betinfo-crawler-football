import config
from domain.models.flashscore_match import FlashscoreMatch
from domain.models.league import League
from domain.models.team import Team
from domain.models.league_team import LeagueTeam
from infrastructure.repositories.csv_repository import CsvRepository


class FlashscoreRepository(CsvRepository):
    def save_matches(self, filename: str, matches: list[FlashscoreMatch]):
        self.save_to_csv(matches, filename)

    def save_leagues(self, leagues: list[League]):
        self.save_to_csv(leagues, config.LEAGUES_FILENAME, append=True, deduplicate=True)

    def save_teams(self, teams: list[Team], nation: str):
        self.save_to_csv(teams, config.TEAMS_FILENAME, append=True, deduplicate=True)

    def save_league_teams(self, league_teams: list[LeagueTeam]):
        self.save_to_csv(league_teams, config.LEAGUE_TEAMS_FILENAME, append=True, deduplicate=True)
