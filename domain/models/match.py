from dataclasses import dataclass

@dataclass(frozen=True)
class Match:
    round: str
    game_number: str
    datetime: str
    league: str
    home: str
    away: str
    game_type: str

    win_domestic: str
    draw_domestic: str
    lose_domestic: str

    init_win_domestic: str
    init_draw_domestic: str
    init_lose_domestic: str

    win_foreign: str
    draw_foreign: str
    lose_foreign: str

    init_win_foreign: str
    init_draw_foreign: str
    init_lose_foreign: str

    score: str
    result: str
    result_odds: str

    @classmethod
    def create_from_extracted_data(cls, data: dict, round_val: str):
        from domain.policies.odds_policy import OddsPolicy
        
        result = data.get("result", "")
        win = data.get("win_domestic", "")
        draw = data.get("draw_domestic", "")
        lose = data.get("lose_domestic", "")
        
        return cls(
            round=round_val,
            game_number=data.get("game_number", ""),
            datetime=data.get("datetime", ""),
            league=data.get("league", ""),
            home=data.get("home", ""),
            away=data.get("away", ""),
            game_type=data.get("game_type", ""),
            win_domestic=win,
            draw_domestic=draw,
            lose_domestic=lose,
            init_win_domestic=data.get("init_win_domestic", ""),
            init_draw_domestic=data.get("init_draw_domestic", ""),
            init_lose_domestic=data.get("init_lose_domestic", ""),
            win_foreign=data.get("win_foreign", ""),
            draw_foreign=data.get("draw_foreign", ""),
            lose_foreign=data.get("lose_foreign", ""),
            init_win_foreign=data.get("init_win_foreign", ""),
            init_draw_foreign=data.get("init_draw_foreign", ""),
            init_lose_foreign=data.get("init_lose_foreign", ""),
            score=data.get("score", ""),
            result=result,
            result_odds=OddsPolicy.calculate_result_odds(result, win, draw, lose)
        )

