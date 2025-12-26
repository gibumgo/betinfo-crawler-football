import re
from bs4 import Tag

class RoundExtractor:
    KEYWORD_ROUND_KR = "라운드"
    KEYWORD_ROUND_EN = "Round"
    
    @staticmethod
    def extract_info(row: Tag, start_round: int, detected_latest_round: int):
        round_text = row.get_text(strip=True)
        
        match = re.search(r'(\d+)', round_text)
        if not match:
            return 0, detected_latest_round, False
            
        current_round_number = int(match.group(1))

        should_stop = False
        if start_round is None:
             if detected_latest_round is None:
                 detected_latest_round = current_round_number
             elif current_round_number != detected_latest_round:
                 should_stop = True
                 
        return current_round_number, detected_latest_round, should_stop
