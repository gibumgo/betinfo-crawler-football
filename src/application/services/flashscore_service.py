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

    def collect_matches_data(self, league_path: str, season: str = DEFAULT_SEASON, start_round: int = None, end_round: int = None):
        self.page.open_league_url(league_path, season)
        
        self.page.wait_for_page_load()
        if start_round is not None:
             self._load_more_until_round(start_round)
        
        matches = MatchParser.parse_matches(
            self.page.driver, 
            league_id=1, 
            season=season,
            start_round=start_round,
            end_round=end_round
        )
        
        filename = None
        if matches:
            safe_nation, safe_league = self._get_safe_filename_parts(league_path)
            filename = f"flashscore_matches_{safe_nation}_{safe_league}_{season}.csv"
            self.repository.save_matches(filename, matches)
        
        return {
            'matches': matches,
            'filename': filename,
            'match_count': len(matches) if matches else 0
        }

    def _load_more_until_round(self, target_round: int):
        max_attempts = 20
        for _ in range(max_attempts):
            html = self.page.driver.page_source
            if f"{target_round} 라운드" in html or f"Round {target_round}" in html:
                break
            
            if not self.page.click_show_more():
                break

