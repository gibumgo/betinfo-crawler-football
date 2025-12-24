from infrastructure.scraping.scrapers.betinfo_page import BetinfoPage
from infrastructure.scraping.parsers.betinfo_match_parser import BetinfoMatchParser
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from domain.models.match import Match


class BetinfoService:
    def __init__(
        self,
        page: BetinfoPage,
        repository: BetinfoRepository
    ):
        self.page = page
        self.repository = repository
        self.parser = BetinfoMatchParser()
    
    def collect_round(self, round_value: str) -> None:
        self.page.open()
        self.page.navigate_to_round(round_value)
        self.page.wait_until_table_loaded()

        elements = self.page.extract_match_elements()
        
        round_display = round_value
        if len(round_value) > 4:
            round_display = round_value[4:]
        
        matches = []
        for element in elements:
            try:
                data_dict = self.parser.parse_row(element)
                if data_dict:
                    match = Match.of(data_dict, round_display)
                    matches.append(match)
            except Exception as e:
                print(f"Error parsing match: {e}")
                continue

        filename = f"betinfo_proto_rate_{round_value}.csv"
        self.repository.save(filename, matches)
        
        print(f"✅ {round_value} round: {len(matches)} matches saved.")
