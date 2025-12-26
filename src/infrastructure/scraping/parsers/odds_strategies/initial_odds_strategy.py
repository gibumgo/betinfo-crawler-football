from bs4 import Tag
from .base_odds_strategy import BaseOddsStrategy


class InitialOddsStrategy(BaseOddsStrategy):
    def parse(self, td_element: Tag) -> str:
        try:
            strings = list(td_element.stripped_strings)
            return strings[0] if strings else ""
        except Exception:
            return ""
