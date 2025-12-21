from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class FlashscoreMatch:
    id: str                   # 경기 id
    league_id: str            # 리그ID
    home_team_name: str       # 홈팀
    away_team_name: str       # 어웨이팀
    url_team1_name_en: str    # 팀1 영문 이름
    url_team2_name_en: str    # 팀2 영문 이름
    url_team1_id: str         # 팀1_ID
    url_team2_id: str         # 팀2_ID
    match_datetime: str       # 경기일시
    round: str                # 라운드
    season: str               # 시즌
    home_score: Optional[str] # 홈점수
    away_score: Optional[str] # 원정점수
    flashscore_match_id: str  # 경기ID

    @classmethod
    def of(cls, data: dict):
        return cls(
            id=data.get("id", ""),
            league_id=data.get("league_id", ""),
            home_team_name=data.get("home_team_name", ""),
            away_team_name=data.get("away_team_name", ""),
            url_team1_name_en=data.get("url_team1_name_en", ""),
            url_team2_name_en=data.get("url_team2_name_en", ""),
            url_team1_id=data.get("url_team1_id", ""),
            url_team2_id=data.get("url_team2_id", ""),
            match_datetime=data.get("match_datetime", ""),
            round=data.get("round", ""),
            season=data.get("season", ""),
            home_score=str(data.get("home_score", "")) if data.get("home_score") is not None else None,
            away_score=str(data.get("away_score", "")) if data.get("away_score") is not None else None,
            flashscore_match_id=data.get("flashscore_match_id", "")
        )
