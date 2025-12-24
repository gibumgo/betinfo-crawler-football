from infrastructure.repositories.csv_repository import CsvRepository
from domain.models.league import League

class LeagueRepository(CsvRepository):
    COLUMN_MAP = {
        "league_id": "리그ID",
        "nation": "국가",
        "nation_ko": "국가명(한)",
        "league_name": "리그명",
        "league_name_ko": "리그명(한)",
        "league_image_url": "리그이미지URL",
        "nation_image_url": "국가이미지URL",
        "current_season": "시즌"
    }
    
    def save(self, leagues: list[League], filename: str = "league.csv") -> None:
        self.save_to_csv(leagues, filename, column_map=self.COLUMN_MAP, append=True, deduplicate=True)
