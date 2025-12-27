import config
from infrastructure.repositories.csv_repository import CsvRepository
from domain.models.team import Team

class TeamRepository(CsvRepository):
    COLUMN_MAP = {
        "team_id": "팀ID",
        "team_name": "팀명",
        "team_name_ko": "팀명(한)",
        "team_image_url": "팀이미지URL",
        "nation": "국가"
    }
    
    def save(self, teams: list[Team], nation: str) -> None:
        if not teams:
            print("⚠️ 저장할 팀 데이터가 없습니다.")
            return
        
        if nation is None:
            nation = teams[0].nation
        
        filename = f"data/{nation}-team.csv"
        self.save_to_csv(teams, filename, column_map=self.COLUMN_MAP, append=True, deduplicate=True)
