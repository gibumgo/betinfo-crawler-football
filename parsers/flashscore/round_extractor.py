from domain.models.flashscore_match import FlashscoreMatch


class RoundExtractor:
    @staticmethod
    def extract_info(round_row, start_round, detected_latest):
        round_label = round_row.text.strip()
        round_num = FlashscoreMatch.parse_round_number(round_label)

        should_stop = False
        if start_round is None:
            if detected_latest is None:
                detected_latest = round_num
            elif round_num != detected_latest:
                should_stop = True

        return round_num, detected_latest, should_stop
