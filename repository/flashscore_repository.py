import pandas as pd
from dataclasses import asdict
from datetime import datetime
from domain.models.flashscore_match import FlashscoreMatch
from domain.models.team import Team

class FlashscoreRepository:
    MATCH_COLUMN_MAP = {
        "id": "경기 id",
        "league_id": "리그ID",
        "home_team_name": "홈팀",
        "away_team_name": "어웨이팀",
        "url_team1_name_en": "팀1 영문 이름",
        "url_team2_name_en": "팀2 영문 이름",
        "url_team1_id": "팀1_ID",
        "url_team2_id": "팀2_ID",
        "match_datetime": "경기일시",
        "round": "라운드",
        "season": "시즌",
        "home_score": "홈점수",
        "away_score": "원정점수",
        "flashscore_match_id": "경기ID"
    }

    TEAM_COLUMN_MAP = {
        "id": "시스템ID",
        "league_id": "리그ID",
        "name_ko": "팀명(한)",
        "name_en": "팀명(영)",
        "flashscore_id": "플래시스코어ID",
        "logo_url": "로고URL",
        "stadium_ko": "경기장(한)",
        "stadium_en": "경기장(영)"
    }

    def save_matches(self, filename: str, match_list: list[FlashscoreMatch]) -> None:
        self._save_to_csv(match_list, self.MATCH_COLUMN_MAP, filename)

    def save_teams(self, filename: str, team_list: list[Team]) -> None:
        self._save_to_csv(team_list, self.TEAM_COLUMN_MAP, filename)

    def save(self, filename: str, match_list: list[FlashscoreMatch]) -> None:
        self.save_matches(filename, match_list)

    def _save_to_csv(self, items: list, column_map: dict, filename: str) -> None:
        """데이터를 컬럼 맵핑에 따라 CSV로 저장하는 공통 로직"""
        csv_rows = []
        for item in items:
            data_dict = asdict(item)
            
            # 날짜형 데이터가 있을 경우 문자열로 변환
            for key, value in data_dict.items():
                if isinstance(value, datetime):
                    data_dict[key] = value.strftime("%Y-%m-%d %H:%M")
            
            mapped_row = {column_map.get(key, key): value for key, value in data_dict.items()}
            csv_rows.append(mapped_row)

        dataframe = pd.DataFrame(csv_rows)
        dataframe.to_csv(filename, index=False, encoding="utf-8-sig")
