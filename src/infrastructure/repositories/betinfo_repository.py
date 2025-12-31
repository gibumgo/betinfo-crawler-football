from domain.models.match import Match
from domain.repositories.match_repository import MatchRepository
from infrastructure.repositories.csv_repository import CsvRepository

class BetinfoRepository(MatchRepository, CsvRepository):
    COLUMN_MAP = {
        "round": "회차",
        "game_number": "경기번호",
        "datetime": "날짜 및 시간",
        "league": "리그명",
        "home": "홈",
        "away": "원정",
        "game_type": "유형",
        "handicap_value": "핸디캡",

        "win_domestic": "승(국내)",
        "draw_domestic": "무(국내)",
        "lose_domestic": "패(국내)",

        "init_win_domestic": "초기 승(국내)",
        "init_draw_domestic": "초기 무(국내)",
        "init_lose_domestic": "초기 패(국내)",

        "win_foreign": "승(해외)",
        "draw_foreign": "무(해외)",
        "lose_foreign": "패(해외)",

        "init_win_foreign": "초기 승(해외)",
        "init_draw_foreign": "초기 무(해외)",
        "init_lose_foreign": "초기 패(해외)",

        "score": "스코어",
        "result": "경기 결과",
        "result_odds": "결과 배당",
    }

    def save(self, filename: str, matches: list[Match]) -> None:
        self.save_to_csv(matches, filename, column_map=self.COLUMN_MAP)
