from domain.models.match import Match
from domain.repositories.match_repository import MatchRepository
from infrastructure.repositories.csv_repository import CsvRepository

class BetinfoRepository(MatchRepository, CsvRepository):
    COLUMN_MAP = {
        "id": "id",
        "round": "round",
        "game_number": "match_no",
        "datetime": "datetime",
        "league": "league",
        "home": "home_team",
        "away": "away_team",
        "bet_type": "bet_type",
        "line": "line",
        
        "win_domestic": "odds_win_kr",
        "draw_domestic": "odds_draw_kr",
        "lose_domestic": "odds_lose_kr",
        
        "init_win_domestic": "init_odds_win_kr",
        "init_draw_domestic": "init_odds_draw_kr",
        "init_lose_domestic": "init_odds_lose_kr",
        
        "win_foreign": "odds_win_overseas",
        "draw_foreign": "odds_draw_overseas",
        "lose_foreign": "odds_lose_overseas",
        
        "init_win_foreign": "init_odds_win_overseas",
        "init_draw_foreign": "init_odds_draw_overseas",
        "init_lose_foreign": "init_odds_lose_overseas",
        
        "score": "score",
        "result": "result",
        "result_odds": "result_odds",
    }

    def save(self, filename: str, matches: list[Match]) -> None:
        self.save_to_csv(matches, filename, column_map=self.COLUMN_MAP)
