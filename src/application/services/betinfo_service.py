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
        output_dir: str = config.DEFAULT_OUTPUT_DIR
    ):
        self.page = page
        self.repository = repository
        self.output_dir = output_dir
        self.parser = BetinfoMatchParser()

    def collect_latest_rounds(self, limit: int = 5) -> None:
        """최신 N개 회차 자동 수집"""
        self.page.open()
        time.sleep(2)  # 페이지 로딩 대기
        
        all_rounds = self.page.get_available_rounds()
        
        # 내림차순 정렬 (높은 숫자가 최신 회차라고 가정)
        # 예: 2025005, 2025004 ...
        sorted_rounds = sorted(all_rounds, reverse=True)
        
        target_rounds = sorted_rounds[:limit]
        
        IPCMessenger.log(f"Detected latest {len(target_rounds)} rounds: {target_rounds}", level="INFO")
        
        total = len(target_rounds)
        for idx, r_val in enumerate(target_rounds):
             IPCMessenger.send_status("COLLECTING_ROUND", r_val)
             IPCMessenger.send_progress((idx / total) * 100)
             self.collect_round(r_val)
             
        IPCMessenger.send_progress(100)
    
    def collect_round(self, round_value: str) -> None:
        self.page.open()
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
