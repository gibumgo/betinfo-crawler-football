import time
import random
from scraper.flashscore.flashscore_page import FlashscorePage
from parser.flashscore.match_parser import MatchParser
from repository.flashscore_repository import FlashscoreRepository

class FlashscoreService:
    def __init__(self, page: FlashscorePage, repository: FlashscoreRepository):
        self.page = page
        self.repository = repository

    def _get_safe_filename_parts(self, league_path: str):
        parts = [p for p in league_path.split("/") if p]
        nation = parts[1] if len(parts) > 1 else "unknown"
        league = parts[2] if len(parts) > 2 else "unknown"
        return nation.replace("-", "_"), league.replace("-", "_")

    def collect_matches_data(self, league_path: str, season: str = "2025-2026", start_round: int = None, end_round: int = None):
        league_path = league_path.rstrip('/')
        if season and season != "2025-2026" and f"-{season}" not in league_path:
            league_path = f"{league_path}-{season}"
        league_path += "/"

        print(f"🕒 경기 결과 수집 시작 ({season}): {league_path}")
        
        try:
            print(f"🔗 접속 시도: {self.page.BASE_URL}{league_path}results/")
            self.page.goto_match_results(league_path)
            time.sleep(random.uniform(2, 4))
            
            if start_round is not None:
                self._load_more_until_round(start_round)
            
            matches = MatchParser.parse_matches(
                self.page.driver, 
                league_id=1, 
                season=season,
                start_round=start_round,
                end_round=end_round
            )
            
            if matches:
                safe_nation, safe_league = self._get_safe_filename_parts(league_path)
                filename = f"flashscore_matches_{safe_nation}_{safe_league}_{season}.csv"
                self.repository.save_matches(filename, matches)
                print(f"💾 경기 결과 저장 완료: {filename} ({len(matches)}개)")
            else:
                print("⚠️ 수집된 경기 데이터가 없습니다. 라운드 범위나 페이지 상태를 확인하세요.")

        except Exception as e:
            print(f"❌ 경기 수집 중 오류: {e}")

    def _load_more_until_round(self, target_round: int):
        print(f"🔍 {target_round} 라운드 데이터를 찾는 중...")
        max_attempts = 20
        for _ in range(max_attempts):
            html = self.page.driver.page_source
            if f"{target_round} 라운드" in html or f"Round {target_round}" in html:
                print(f"✨ 목표 라운드 도달!")
                break
            
            if not self.page.click_show_more():
                print("🏁 더 이상 불러올 데이터가 없습니다.")
                break
