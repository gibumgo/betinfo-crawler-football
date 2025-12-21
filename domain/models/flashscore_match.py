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
    home_score: Optional[int] # 홈점수
    away_score: Optional[int] # 원정점수
    flashscore_match_id: str  # 경기ID

    @classmethod
    def create(cls, **kwargs):
        """파서에서 사용하는 명시적 생성 메서드"""
        return cls(
            id=str(kwargs.get("id", "")),
            league_id=str(kwargs.get("league_id", "")),
            home_team_name=kwargs.get("home_team_name", ""),
            away_team_name=kwargs.get("away_team_name", ""),
            url_team1_name_en=kwargs.get("url_team1_name_en", ""),
            url_team2_name_en=kwargs.get("url_team2_name_en", ""),
            url_team1_id=kwargs.get("url_team1_id", ""),
            url_team2_id=kwargs.get("url_team2_id", ""),
            match_datetime=str(kwargs.get("match_datetime", "")),
            round=str(kwargs.get("round", "0")),
            season=kwargs.get("season", ""),
            home_score=kwargs.get("home_score"),
            away_score=kwargs.get("away_score"),
            flashscore_match_id=kwargs.get("flashscore_match_id", "")
        )

    @classmethod
    def of(cls, raw_data: dict):
        return cls(
            id=str(raw_data.get("id", "")),
            league_id=str(raw_data.get("league_id", "")),
            home_team_name=raw_data.get("home", ""),
            away_team_name=raw_data.get("away", ""),
            url_team1_name_en=raw_data.get("url_info", {}).get("t1_slug", ""),
            url_team2_name_en=raw_data.get("url_info", {}).get("t2_slug", ""),
            url_team1_id=raw_data.get("url_info", {}).get("t1_id", ""),
            url_team2_id=raw_data.get("url_info", {}).get("t2_id", ""),
            match_datetime=raw_data.get("time", ""),
            round=str(raw_data.get("round", "0")),
            season=raw_data.get("season", ""),
            home_score=cls._safe_score(raw_data.get("h_score")),
            away_score=cls._safe_score(raw_data.get("a_score")),
            flashscore_match_id=raw_data.get("url_info", {}).get("match_id", "")
        )

    @staticmethod
    def parse_round_number(text: str) -> int:
        import re
        match = re.search(r"(\d+)", text.strip())
        return int(match.group(1)) if match else 0

    @staticmethod
    def _safe_score(score) -> Optional[str]:
        if score is None or str(score).strip() == "":
            return None
        return str(score)

    @staticmethod
    def extract_url_info(href: str) -> dict:
        import re
        info = {"match_id": "", "t1_slug": "", "t1_id": "", "t2_slug": "", "t2_id": ""}
        
        match_search = re.search(r"mid=([a-zA-Z0-9]+)", href)
        if match_search: info["match_id"] = match_search.group(1)
            
        team_segments = re.findall(r"/([^/]+-[a-zA-Z0-9]{8})(?=/)", href)
        if len(team_segments) >= 1:
            seg = team_segments[0]
            idx = seg.rfind('-')
            info["t1_slug"], info["t1_id"] = (seg[:idx], seg[idx+1:]) if idx != -1 else ("", seg)
            
        if len(team_segments) >= 2:
            seg = team_segments[1]
            idx = seg.rfind('-')
            info["t2_slug"], info["t2_id"] = (seg[:idx], seg[idx+1:]) if idx != -1 else ("", seg)
            
        return info
