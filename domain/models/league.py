from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class League:
    league_id: str
    name: str
    country: Optional[str] = None
    season: Optional[str] = None
    participating_teams: List[str] = field(default_factory=list)

    @classmethod
    def of(cls, data: dict):
        return cls(
            league_id=data.get("league_id", ""),
            name=data.get("name", ""),
            country=data.get("country"),
            season=data.get("season"),
            participating_teams=data.get("teams", [])
        )
