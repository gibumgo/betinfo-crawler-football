from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class League:
    league_id: str              # Flashscore 리그 고유 ID (예: OEEq9Yvp)
    nation: str                 # URL용 국가명 (예: england)
    nation_ko: str              # 한국어 국가명
    league_name: str            # URL용 리그명 (예: premier-league)
    league_name_ko: str         # 한국어 리그명
    league_image_url: str       # 리그 로고 이미지 URL
    nation_image_url: str       # 국가 플래그 이미지 URL
    current_season: str = "2025-2026"  # 현재 시즌

    @classmethod
    def create(cls, **kwargs):
        """파서에서 사용하는 명시적 생성 메서드"""
        return cls(
            league_id=kwargs.get("league_id", ""),
            nation=kwargs.get("nation", ""),
            nation_ko=kwargs.get("nation_ko", ""),
            league_name=kwargs.get("league_name", ""),
            league_name_ko=kwargs.get("league_name_ko", ""),
            league_image_url=kwargs.get("league_image_url", ""),
            nation_image_url=kwargs.get("nation_image_url", ""),
            current_season=kwargs.get("current_season", "2025-2026")
        )
