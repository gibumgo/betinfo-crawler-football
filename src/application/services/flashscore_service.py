from infrastructure.scraping.scrapers.flashscore.flashscore_page import FlashscorePage
from infrastructure.scraping.parsers.flashscore_match_parser import MatchParser
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
import config
from config import DEFAULT_SEASON
import datetime
import time

class FlashscoreService:
    def __init__(self, page: FlashscorePage, repository: FlashscoreRepository):
        self.page = page
        self.repository = repository

    def _sanitize_filename(self, name: str) -> str:
        return name.replace("-", "_").replace(" ", "_").lower()
    
    def _extract_league_id(self, league_path: str):
        parts = [p for p in league_path.split("/") if p]
        return parts[2] if len(parts) > 2 else "unknown"

    def _get_safe_filename_parts(self, league_path: str):
        parts = [p for p in league_path.split("/") if p]
        if len(parts) >= 3:
            nation = self._sanitize_filename(parts[1])
            league = self._sanitize_filename(parts[2])
            return nation, league
        return "unknown", "unknown"

    def collect_matches_data(self, league_path: str, league_name: str, season: str = DEFAULT_SEASON, start_round: int = None, end_round: int = None):
        pass

    def collect_season_data_integrated(self, country: str, league: str, season: str, options: dict = None):
        if options is None:
            options = {}
            
        league_path = f"/soccer/{self._sanitize_filename(country)}/{self._sanitize_filename(league)}"
        
        safe_nation, safe_league = self._get_safe_filename_parts(league_path)
        matches_filename = f"{config.DIR_DATA_CRAWLED_FLASHSCORE}/flashscore_matches_{safe_nation}_{safe_league}_{season}.csv"
        
        latest_match_time = None
        if not options.get('force_full', False):
            latest_match_time = self.repository.get_latest_match_time(matches_filename)
            if latest_match_time:
                print(f"🔄 Smart Resume: Existing data found until {latest_match_time}. Only fetching newer matches.")
        
        if not options.get('skip_standings', False):
            print("📊 Phase 1: Collecting Standings & Metadata...")
            self.page.open_standings_page(league_path, season)
            time.sleep(1)
        
        print("⚽ Phase 2: Collecting Match Results...")
        self.page.open_results_page(league_path, season)
        self.page.wait_for_page_load()
        
        if latest_match_time:
             self._load_matches_until_overlap(latest_match_time, safe_league, season)
        else:
             self._load_all_matches()
        
        html_content = self.page.get_page_source()
        matches = MatchParser.parse_matches(
            html_content, 
            league_name=safe_league,
            season=season
        )
        
        if latest_match_time:
            match_count_before = len(matches)
            matches = [m for m in matches if m.time and m.time > latest_match_time]
            print(f"✨ Filtered overlapping matches: {match_count_before} -> {len(matches)} new matches.")
            
        if matches:
            print(f"💾 Saving {len(matches)} matches to {matches_filename}...")
            self.repository.save_matches(matches_filename, matches, append=(latest_match_time is not None))
        else:
            print("⚠️ No new matches found to save.")
            
        return matches

    def _load_matches_until_overlap(self, threshold_date: datetime.datetime, league_name: str, season: str):
        max_attempts = 20
        for i in range(max_attempts):
            html = self.page.get_page_source()
            matches = MatchParser.parse_matches(html, league_name, season)
            if not matches:
                break
                
            oldest_fetched = min([m.time for m in matches if m.time] or [datetime.datetime.max])
            
            if oldest_fetched != datetime.datetime.max and oldest_fetched < threshold_date:
                print(f"✅ Reached overlap point ({oldest_fetched} < {threshold_date}). Stopping load.")
                return
            
            print(f"🔄 Loading more... Oldest loaded: {oldest_fetched}")
            if not self.page.click_show_more():
                print("⚠️ No more matches to load.")
                break

    def _load_all_matches(self):
        print("📥 Loading all matches for the season...")
        max_attempts = 50
        for i in range(max_attempts):
            if not self.page.click_show_more():
                break
            time.sleep(0.5)

    def collect_matches_data(self, league_path: str, league_name: str, season: str = DEFAULT_SEASON, start_round: int = None, end_round: int = None):
        self.page.open_results_page(league_path, season)
        self.page.wait_for_page_load()
        if start_round is not None:
             self._load_more_until_round(start_round)
        html_content = self.page.get_page_source()
        matches = MatchParser.parse_matches(html_content, league_name=league_name, season=season, start_round=start_round, end_round=end_round)
        filename = None
        if matches:
            safe_nation, safe_league = self._get_safe_filename_parts(league_path)
            filename = f"{config.DIR_DATA_CRAWLED_FLASHSCORE}/flashscore_matches_{safe_nation}_{safe_league}_{season}.csv"
            self.repository.save_matches(filename, matches)
        return {'matches': matches, 'filename': filename, 'match_count': len(matches) if matches else 0}

    def _load_more_until_round(self, target_round: int):
        pass
