from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Fixture:
    fixture_id: str
    league_id: str
    date: str  # YYYY-MM-DD HH:mm 형식 가정
    home_team_id: str
    away_team_id: str
    status: str  # 예: SCHEDULED, FINISHED, POSTPONED
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    @classmethod
    def of(cls, data: dict):
        return cls(
            fixture_id=data.get("fixture_id", ""),
            league_id=data.get("league_id", ""),
            date=data.get("date", ""),
            home_team_id=data.get("home_team_id", ""),
            away_team_id=data.get("away_team_id", ""),
            status=data.get("status", "SCHEDULED"),
            home_score=data.get("home_score"),
            away_score=data.get("away_score")
        )
