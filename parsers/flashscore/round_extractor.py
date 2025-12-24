from domain.models.flashscore_match import FlashscoreMatch


class RoundExtractor:
    KEYWORD_ROUND_KR = "라운드"
    KEYWORD_ROUND_EN = "Round"
    
    @staticmethod
    def extract_info(row, start_round, detected_latest_round):
        round_text = row.text.strip()
        
        if RoundExtractor.KEYWORD_ROUND_KR in round_text:
            try:
                current_round_number = int(round_text.replace(RoundExtractor.KEYWORD_ROUND_KR, "").strip())
            except ValueError:
                return 0, detected_latest_round, False
        elif RoundExtractor.KEYWORD_ROUND_EN in round_text:
            try:
                current_round_number = int(round_text.replace(RoundExtractor.KEYWORD_ROUND_EN, "").strip())
            except ValueError:
                return 0, detected_latest_round, False
        else:
            return 0, detected_latest_round, False

        should_stop = False
        if start_round is None:
             if detected_latest_round is None:
                 detected_latest_round = current_round_number
             elif current_round_number != detected_latest_round:
                 should_stop = True
                 
        return current_round_number, detected_latest_round, should_stop

