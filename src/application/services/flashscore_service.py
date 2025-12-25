from infrastructure.scraping.scrapers.flashscore.flashscore_page import FlashscorePage
from infrastructure.scraping.parsers.flashscore_match_parser import MatchParser
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from config import DEFAULT_SEASON

class FlashscoreService:
    def __init__(self, page: FlashscorePage, repository: FlashscoreRepository):
        self.page = page
        self.repository = repository

    def _get_safe_filename_parts(self, league_path: str):
        parts = [p for p in league_path.split("/") if p]
        nation = parts[1] if len(parts) > 1 else "unknown"
        league = parts[2] if len(parts) > 2 else "unknown"
        return nation.replace("-", "_"), league.replace("-", "_")
    
    def _extract_league_id(self, league_path: str):
        parts = [p for p in league_path.split("/") if p]
        return parts[2] if len(parts) > 2 else "unknown"

    def collect_matches_data(self, league_path: str, league_name: str, season: str = DEFAULT_SEASON, start_round: int = None, end_round: int = None):
        self.page.open_results_page(league_path, season)
        
        self.page.wait_for_page_load()
        
        if start_round is not None:
             print(f"🔍 {start_round} 라운드 데이터를 찾는 중...")
             self._load_more_until_round(start_round)
        
        html_content = self.page.get_page_source()
        
        matches = MatchParser.parse_matches(
            html_content, 
            league_name=league_name, 
            season=season,
            start_round=start_round,
            end_round=end_round
        )
        
        filename = None
        if matches:
            safe_nation, safe_league = self._get_safe_filename_parts(league_path)
            filename = f"flashscore_matches_{safe_nation}_{safe_league}_{season}.csv"
            self.repository.save_matches(filename, matches)
        else:
            print("⚠️ 수집된 경기 데이터가 없습니다. 라운드 범위나 페이지 상태를 확인하세요.")
        
        return {
            'matches': matches,
            'filename': filename,
            'match_count': len(matches) if matches else 0
        }

    def _load_more_until_round(self, target_round: int):
        from bs4 import BeautifulSoup
        import re
        
        max_attempts = 50
        
        for i in range(max_attempts):
            html = self.page.get_page_source()
            soup = BeautifulSoup(html, 'lxml')
            
            round_headers = soup.select(".event__round")
            found = False
            
            for header in round_headers:
                header_text = header.get_text(strip=True)
                match = re.search(r'(\d+)', header_text)
                if match:
                    r_num = int(match.group(1))
                    if r_num == target_round:
                        print(f"✅ {target_round} 라운드 헤더 발견: '{header_text}'")
                        found = True
                        break
                
            if found:
                break
            
            if i < max_attempts - 1:
                print(f"🔄 더 많은 경기 로딩 중... ({i+1}/{max_attempts})")
                if not self.page.click_show_more():
                    break
