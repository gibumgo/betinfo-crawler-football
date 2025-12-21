from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class Team:
    team_id: str
    name: str
    league_id: str
    stadium: Optional[str] = None
    manager: Optional[str] = None
    detailed_info: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def of(cls, data: dict):
        return cls(
            team_id=data.get("team_id", ""),
            name=data.get("name", ""),
            league_id=data.get("league_id", ""),
            stadium=data.get("stadium"),
            manager=data.get("manager"),
            detailed_info=data.get("detailed_info", {})
        )
