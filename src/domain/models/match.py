from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Match(BaseModel):
    round: str = Field(default="")
    game_number: str = Field(default="")
    datetime: str = Field(default="")
    league: str = Field(default="")
    home: str = Field(default="")
    away: str = Field(default="")
    game_type: str = Field(default="")

    win_domestic: str = Field(default="")
    draw_domestic: str = Field(default="")
    lose_domestic: str = Field(default="")

    init_win_domestic: str = Field(default="")
    init_draw_domestic: str = Field(default="")
    init_lose_domestic: str = Field(default="")

    win_foreign: str = Field(default="")
    draw_foreign: str = Field(default="")
    lose_foreign: str = Field(default="")

    init_win_foreign: str = Field(default="")
    init_draw_foreign: str = Field(default="")
    init_lose_foreign: str = Field(default="")

    score: str = Field(default="")
    result: str = Field(default="")
    result_odds: str = Field(default="")

    @classmethod
    def of(cls, data: dict, round_val: str):
        from domain.policies.odds_policy import OddsPolicy
        
        result = data.get("result", "")
        win = data.get("win_domestic", "")
        draw = data.get("draw_domestic", "")
        lose = data.get("lose_domestic", "")
        
        return cls(
            round=str(round_val),
            game_number=str(data.get("game_number", "")),
            datetime=str(data.get("datetime", "")),
            league=str(data.get("league", "")),
            home=str(data.get("home", "")),
            away=str(data.get("away", "")),
            game_type=str(data.get("game_type", "")),
            win_domestic=str(win),
            draw_domestic=str(draw),
            lose_domestic=str(lose),
            init_win_domestic=str(data.get("init_win_domestic", "")),
            init_draw_domestic=str(data.get("init_draw_domestic", "")),
            init_lose_domestic=str(data.get("init_lose_domestic", "")),
            win_foreign=str(data.get("win_foreign", "")),
            draw_foreign=str(data.get("draw_foreign", "")),
            lose_foreign=str(data.get("lose_foreign", "")),
            init_win_foreign=str(data.get("init_win_foreign", "")),
            init_draw_foreign=str(data.get("init_draw_foreign", "")),
            init_lose_foreign=str(data.get("init_lose_foreign", "")),
            score=str(data.get("score", "")),
            result=str(result),
            result_odds=str(OddsPolicy.calculate_result_odds(result, win, draw, lose))
        )

