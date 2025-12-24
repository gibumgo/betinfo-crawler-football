class OddsPolicy:
    MAP = {
        "승": "win",
        "무": "draw",
        "패": "lose",
        "U": "win",
        "O": "lose",
        "홀": "win",
        "짝": "lose",
    }

    @classmethod
    def calculate_result_odds(cls, result, win, draw, lose):
        key = cls.MAP.get(result.strip())
        return {"win": win, "draw": draw, "lose": lose}.get(key, "")
