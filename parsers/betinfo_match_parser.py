from selenium.webdriver.common.by import By
from parsers.game_type_strategies.game_type_strategy_factory import GameTypeStrategyFactory
from parsers.odds_strategies.initial_odds_strategy import InitialOddsStrategy
from parsers.odds_strategies.current_odds_strategy import CurrentOddsStrategy


class BetinfoMatchParser:
    def __init__(self):
        self.initial_odds_parser = InitialOddsStrategy()
        self.current_odds_parser = CurrentOddsStrategy()
    
    def parse_row(self, row) -> dict:
        tds = row.find_elements(By.TAG_NAME, "td")
        
        if len(tds) < 21:
            return None
        
        game_type_img = self._extract_image_source(tds[3])
        game_type_strategy = GameTypeStrategyFactory.create_strategy(game_type_img)
        
        game_type = game_type_strategy.identify_type_name()
        handicap_value = tds[7].text.strip() if tds[7].text.strip() else None
        result_data = game_type_strategy.parse_result(tds[20])
        
        return {
            "game_number": tds[0].text.strip(),
            "datetime": tds[1].text.strip(),
            "league": tds[2].text.strip(),
            "home": tds[4].text.strip(),
            "game_type": game_type,
            "away": tds[6].text.strip(),
            "handicap_value": handicap_value,
            
            "init_win_foreign": self.initial_odds_parser.parse(tds[10]),
            "win_foreign": self.current_odds_parser.parse(tds[10]),
            "init_draw_foreign": self.initial_odds_parser.parse(tds[11]),
            "draw_foreign": self.current_odds_parser.parse(tds[11]),
            "init_lose_foreign": self.initial_odds_parser.parse(tds[12]),
            "lose_foreign": self.current_odds_parser.parse(tds[12]),
            
            "init_win_domestic": self.initial_odds_parser.parse(tds[13]),
            "win_domestic": self.current_odds_parser.parse(tds[13]),
            "init_draw_domestic": self.initial_odds_parser.parse(tds[14]),
            "draw_domestic": self.current_odds_parser.parse(tds[14]),
            "init_lose_domestic": self.initial_odds_parser.parse(tds[15]),
            "lose_domestic": self.current_odds_parser.parse(tds[15]),
            
            "result": result_data.get("result"),
            "score": result_data.get("score"),
        }
    
    def _extract_image_source(self, td_element) -> str:
        try:
            img_elements = td_element.find_elements(By.TAG_NAME, "img")
            if img_elements:
                return img_elements[0].get_attribute("src")
        except Exception:
            pass
        return ""
