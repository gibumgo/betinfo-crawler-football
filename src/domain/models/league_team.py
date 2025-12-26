from dataclasses import dataclass

@dataclass(frozen=True)
class LeagueTeam:
    league_id: str          # 리그 ID
    team_id: str            # 팀 ID
    season: str = "2025-2026"  # 시즌 (기본값: 2025-2026)

    @classmethod
    def create(cls, **kwargs):
        return cls(
            league_id=kwargs.get("league_id", ""),
            team_id=kwargs.get("team_id", ""),
            season=kwargs.get("season", "2025-2026")
        )
