from typing import Dict
from bs4 import Tag
from .base_game_type_strategy import BaseGameTypeStrategy


class HandicapGameStrategy(BaseGameTypeStrategy):
    def matches(self, img_src: str) -> bool:
        return "ico_handicap.gif" in img_src
    
    def identify_type_name(self) -> str:
        return "핸디캡"
    
    def parse_result(self, td_element: Tag) -> Dict[str, str]:
        try:
            strings = list(td_element.stripped_strings)
            
            result = strings[0] if strings else ""
            score = strings[1] if len(strings) > 1 else ""
            
            return {
                "result": result,
                "score": score
            }
        except Exception:
            return {
                "result": "",
                "score": ""
            }
