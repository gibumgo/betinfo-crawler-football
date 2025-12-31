import os
import time
import config
from bs4 import BeautifulSoup
from infrastructure.scraping.scrapers.betinfo_page import BetinfoPage
from infrastructure.scraping.parsers.betinfo_match_parser import BetinfoMatchParser
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from domain.models.match import Match
from shared.ipc_messenger import IPCMessenger


class BetinfoService:
    def __init__(
        self,
        page: BetinfoPage,
        repository: BetinfoRepository,
        output_dir: str = config.DEFAULT_OUTPUT_DIR,
        skip_existing: bool = False
    ):
        self.page = page
        self.repository = repository
        self.output_dir = output_dir
        self.skip_existing = skip_existing
        self.parser = BetinfoMatchParser()

    def collect_latest_rounds(self, limit: int = 5) -> None:
        self.page.open()
        time.sleep(2)

        available_years = self.page.get_available_years()
        available_years.sort(reverse=True)
        
        target_rounds_with_year = []
        
        for year in available_years:
            if len(target_rounds_with_year) >= limit:
                break
                
            IPCMessenger.log(f"Checking rounds for year {year}...", level="INFO")
            self.page.navigate_to_year(year)
            time.sleep(1)
            
            rounds = self.page.get_available_rounds()
            rounds.sort(reverse=True)
            
            for r in rounds:
                if len(target_rounds_with_year) >= limit:
                    break
                target_rounds_with_year.append((year, r))
        
        if not target_rounds_with_year:
             IPCMessenger.log("No available rounds found.", level="WARNING")
             return

        IPCMessenger.log(f"Detected latest {len(target_rounds_with_year)} rounds: {target_rounds_with_year}", level="INFO")
        
        total = len(target_rounds_with_year)
        
        for idx, (year, r_val) in enumerate(target_rounds_with_year):
             IPCMessenger.send_status("COLLECTING_ROUND", r_val)
             IPCMessenger.send_progress((idx / total) * 100)
             self.collect_round(r_val, year=year)
             
        IPCMessenger.send_progress(100)
    
    def collect_round(self, round_value: str, year: str = None) -> None:
        filename = f"betinfo_proto_rate_{round_value}.csv"
        full_path = os.path.join(config.DIR_DATA_CRAWLED_BETINFO, filename)

        if self.skip_existing and os.path.exists(full_path):
            IPCMessenger.log(f"⏩ Round {round_value} already exists. Skipping...", level="INFO")
            return

        self.page.open()
        
        if year:
            self.page.navigate_to_year(year)
            time.sleep(1)
        
        available_rounds = self.page.get_available_rounds()
        if round_value not in available_rounds:
            IPCMessenger.log(f"{round_value}회차는 존재하지 않습니다. (Year: {year if year else 'Default'})", level="WARNING")
            return

        self.page.navigate_to_round(round_value)
        self.page.wait_until_table_loaded()

        html_content = self.page.get_page_source()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        match_rows = soup.select('#listView > tbody > tr[league_gubun="1"]')
        
        round_display = round_value
        if len(round_value) > 4:
            round_display = round_value[4:]
        
        matches = []
        for row in match_rows:
            try:
                data_dict = self.parser.parse_row(row)
                if data_dict:
                    match = Match.of(data_dict, round_display)
                    matches.append(match)
            except Exception as e:
                print(f"Error parsing match: {e}")
                continue

        filename = f"betinfo_proto_rate_{round_value}.csv"
        full_path = os.path.join(config.DIR_DATA_CRAWLED_BETINFO, filename)
        
        self.repository.save(full_path, matches)
        
        IPCMessenger.log(f"✅ {round_value} round: {len(matches)} matches saved to {full_path}", level="INFO")
