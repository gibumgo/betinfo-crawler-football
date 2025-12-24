from typing import Dict
from .base_game_type_strategy import BaseGameTypeStrategy


class SumGameStrategy(BaseGameTypeStrategy):
    def matches(self, img_src: str) -> bool:
        return "ico_sum.gif" in img_src
    
    def identify_type_name(self) -> str:
        return "SUM"
    
    def parse_result(self, td_element) -> Dict[str, str]:
        try:
            text = td_element.text.strip()
            lines = text.split('\n')
            
            result = lines[0].strip() if lines else ""
            score = lines[1].strip() if len(lines) > 1 else ""
            
            return {
                "result": result,
                "score": score
            }
        except Exception:
            return {
                "result": "",
                "score": ""
            }
