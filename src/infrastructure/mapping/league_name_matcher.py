from typing import List
from infrastructure.mapping.base_name_matcher import BaseNameMatcher
import config
from infrastructure.mapping.base_name_matcher import BaseNameMatcher
from infrastructure.constants.mapping_constants import (
    COL_LEAGUE_ID, COL_LEAGUE_NAME_KO, COL_LEAGUE_NAME_EN,
    COL_LEAGUE_NATION, COL_LEAGUE_NATION_KO
)

class LeagueNameMatcher(BaseNameMatcher):
    def __init__(
        self, 
        leagues_csv_path: str = config.DEFAULT_LEAGUES_CSV_PATH,
        mappings_json_path: str = config.DEFAULT_LEAGUE_MAPPING_JSON_PATH
    ):
        super().__init__(leagues_csv_path, mappings_json_path, "League")

    def _build_search_list(self) -> List[dict]:
        candidates = []
        for league in self.master_data:
            lid = str(league.get(COL_LEAGUE_ID, ''))
            if not lid: continue
            
            name_ko = str(league.get(COL_LEAGUE_NAME_KO, ''))
            name_en = str(league.get(COL_LEAGUE_NAME_EN, ''))
            nation = str(league.get(COL_LEAGUE_NATION, ''))
            nation_ko = str(league.get(COL_LEAGUE_NATION_KO, ''))
            
            display_ko = f"{name_ko} ({nation_ko})" if name_ko and nation_ko else name_ko
            display_en = f"{name_en} ({nation})" if name_en and nation else name_en
            
            if name_ko:
                candidates.append({
                    'id': lid,
                    'search_name': name_ko,
                    'display': display_ko
                })
            if name_en:
                candidates.append({
                    'id': lid,
                    'search_name': name_en,
                    'display': display_en
                })
        return candidates
