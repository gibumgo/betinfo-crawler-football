from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class Team:
    id: str                # 시스템ID
    league_id: str         # 리그ID
    name_ko: str           # 팀명(한)
    name_en: str           # 팀명(영)
    flashscore_id: str     # 플래시스코어ID
    logo_url: Optional[str] = None # 로고URL
    stadium_ko: Optional[str] = None # 경기장(한)
    stadium_en: Optional[str] = None # 경기장(영)

    @classmethod
    def of(cls, data: dict):
        return cls(
            id=data.get("id", ""),
            league_id=data.get("league_id", ""),
            name_ko=data.get("name_ko", ""),
            name_en=data.get("name_en", ""),
            flashscore_id=data.get("flashscore_id", ""),
            logo_url=data.get("logo_url"),
            stadium_ko=data.get("stadium_ko"),
            stadium_en=data.get("stadium_en")
        )
