from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Match(BaseModel):
    id: str = Field(default="")
    round: str = Field(default="")
    game_number: str = Field(default="")
    datetime: str = Field(default="")
    league: str = Field(default="")
    home: str = Field(default="")
    away: str = Field(default="")
    game_type: str = Field(default="")
    handicap_value: str = Field(default="")
    bet_type: str = Field(default="")
    line: str = Field(default="")

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

        game_type = str(data.get("game_type", ""))
        handicap_value = data.get("handicap_value")
        
        bet_type_map = {
            "일반": "G",
            "핸디캡": "H",
            "언더오버": "U",
            "SUM": "S"
        }
        bet_type_code = bet_type_map.get(game_type, "G")

        line = "0"
        if bet_type_code in ["G", "S"]:
            line = "0"
        elif handicap_value:
            try:
                clean_val = handicap_value.replace("+", "")
                float_val = float(clean_val)
                
                val_str = f"{float_val:g}"
                
                if bet_type_code == "H" and float_val > 0:
                    line = f"+{val_str}"
                else:
                    line = val_str
            except ValueError:
                line = handicap_value
             pass
             pass

        game_number_str = str(data.get("game_number", ""))
        try:
            match_no_padded = f"{int(game_number_str):03d}"
        except ValueError:
            match_no_padded = game_number_str

        unique_id = f"{round_val}_{match_no_padded}_{bet_type_code}_{line}"
        
        round_display = round_val
        if len(round_val) > 4 and round_val.isdigit():
             pass

        display_round = round_val
        if len(round_val) > 4:
            display_round = round_val[4:]

        return cls(
            id=unique_id,
            round=str(display_round),
            game_number=game_number_str,
            datetime=str(data.get("datetime", "")),
            league=str(data.get("league", "")),
            home=str(data.get("home", "")),
            away=str(data.get("away", "")),
            game_type=game_type,
            bet_type=bet_type_code,
            line=line,
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

