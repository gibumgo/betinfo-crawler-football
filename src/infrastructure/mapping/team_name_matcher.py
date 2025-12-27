from typing import List
from infrastructure.mapping.base_name_matcher import BaseNameMatcher
import config
from infrastructure.mapping.base_name_matcher import BaseNameMatcher
from infrastructure.constants.mapping_constants import (
    COL_TEAM_ID, COL_TEAM_NAME_KO, COL_TEAM_NAME_EN
)

class TeamNameMatcher(BaseNameMatcher):
    def __init__(
        self, 
        teams_csv_path: str = config.DEFAULT_TEAMS_CSV_PATH,
        mappings_json_path: str = config.DEFAULT_TEAM_MAPPING_JSON_PATH
    ):
        super().__init__(teams_csv_path, mappings_json_path, "Team")

    def _build_search_list(self) -> List[dict]:
        candidates = []
        for team in self.master_data:
            tid = str(team.get(COL_TEAM_ID, ''))
            if not tid: continue
            
            name_ko = str(team.get(COL_TEAM_NAME_KO, ''))
            name_en = str(team.get(COL_TEAM_NAME_EN, ''))
            
            if name_ko:
                candidates.append({
                    'id': tid,
                    'search_name': name_ko,
                    'display': f"{name_ko} ({name_en})"
                })
            if name_en:
                candidates.append({
                    'id': tid,
                    'search_name': name_en,
                    'display': f"{name_ko} ({name_en})"
                })
        return candidates
