from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class FlashscoreMatch(BaseModel):
    id: str = Field(default="")
    league_id: str = Field(default="")
    home_team_name: str = Field(default="")
    away_team_name: str = Field(default="")
    url_team1_name_en: str = Field(default="")
    url_team2_name_en: str = Field(default="")
    url_team1_id: str = Field(default="")
    url_team2_id: str = Field(default="")
    match_datetime: str = Field(default="")
    round: str = Field(default="0")
    season: str = Field(default="")
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    flashscore_match_id: str = Field(default="")

    @field_validator('home_score', 'away_score', mode='before')
    @classmethod
    def check_score(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
             if not v.isdigit(): return None
             return int(v)
        if isinstance(v, int):
            if v < 0:
                raise ValueError("Score cannot be negative")
        return v

    @classmethod
    def create(cls, **kwargs):
        """파서에서 사용하는 명시적 생성 메서드"""
        data = {
            "id": str(kwargs.get("id", "")),
            "league_id": str(kwargs.get("league_id", "")),
            "home_team_name": kwargs.get("home_team_name", ""),
            "away_team_name": kwargs.get("away_team_name", ""),
            "url_team1_name_en": kwargs.get("url_team1_name_en", ""),
            "url_team2_name_en": kwargs.get("url_team2_name_en", ""),
            "url_team1_id": kwargs.get("url_team1_id", ""),
            "url_team2_id": kwargs.get("url_team2_id", ""),
            "match_datetime": str(kwargs.get("match_datetime", "")),
            "round": str(kwargs.get("round", "0")),
            "season": kwargs.get("season", ""),
            "home_score": kwargs.get("home_score"),
            "away_score": kwargs.get("away_score"),
            "flashscore_match_id": kwargs.get("flashscore_match_id", "")
        }
        return cls.model_validate(data)

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
            home_score=raw_data.get("h_score"),
            away_score=raw_data.get("a_score"),
            flashscore_match_id=raw_data.get("url_info", {}).get("match_id", "")
        )

    @staticmethod
    def parse_round_number(text: str) -> int:
        match = re.search(r"(\d+)", text.strip())
        return int(match.group(1)) if match else 0

    @staticmethod
    def extract_url_info(href: str) -> dict:
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
