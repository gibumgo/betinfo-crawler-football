from bs4 import Tag
from .base_odds_strategy import BaseOddsStrategy


class CurrentOddsStrategy(BaseOddsStrategy):
    def parse(self, td_element: Tag) -> str:
        try:
            span_elements = td_element.find_all("span")
            if span_elements:
                span_text = span_elements[0].get_text(strip=True)
                return span_text.split('(')[0].strip() if '(' in span_text else span_text
            
            strings = list(td_element.stripped_strings)
            return strings[0] if strings else ""
        except Exception:
            return ""
