class OddsPolicy:
    MAP = {
        "승": "win",
        "무": "draw",
        "패": "lose",
        "U": "win",
        "O": "lose",
        "언더": "win",
        "오버": "lose",
        "홀": "win",
        "짝": "lose",
    }

    @classmethod
    def calculate_result_odds(cls, result: str, win: str, draw: str, lose: str) -> str:
        if not result:
            return ""
            
        res = result.strip().upper()
        res = res.replace("Ｕ", "U").replace("Ｏ", "O")
        
        key = cls.MAP.get(res)
        if key:
            value = {"win": win, "draw": draw, "lose": lose}.get(key, "")
            return value if value and value != "-" else ""
            
        if res.startswith("U") or "언더" in res:
            return win if win != "-" else ""
        if res.startswith("O") or "오버" in res:
            return lose if lose != "-" else ""
        if "승" in res:
            return win if win != "-" else ""
        if "무" in res:
            return draw if draw != "-" else ""
        if "패" in res:
            return lose if lose != "-" else ""
            
        return ""
