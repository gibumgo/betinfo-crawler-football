from driver.chrome_driver_factory import ChromeDriverFactory
from scraper.flashscore.flashscore_page import FlashscorePage
from repository.flashscore_repository import FlashscoreRepository
from service.flashscore_service import FlashscoreService
from view.console_view import ConsoleView

class FlashscoreController:
    def __init__(self):
        self.view = ConsoleView()
        self.repository = FlashscoreRepository()

    def start_collection(self):
        self.view.display_welcome()
        params = self.view.get_collection_params()
        
        driver = None
        try:
            self.view.display_status("브라우저를 초기화 중입니다...", "working")
            driver = ChromeDriverFactory.create()
            
            page = FlashscorePage(driver)
            service = FlashscoreService(page, self.repository)
            
            self.view.display_status(f"데이터 수집을 시작합니다... ({params['season']})", "info")
            
            service.collect_matches_data(
                league_path=params["league_path"],
                season=params["season"],
                start_round=params["start_round"],
                end_round=params["end_round"]
            )
            
            safe_nation = params["league_path"].split("/")[2] if len(params["league_path"].split("/")) > 2 else "unknown"
            filename = f"flashscore_matches_{safe_nation}_{params['season']}.csv"
            
            self.view.display_status("데이터 저장 및 후처리가 완료되었습니다.", "success")
            
        except Exception as e:
            self.view.display_status(f"수집 작업 중 오류 발생: {e}", "error")
            
        finally:
            if driver:
                driver.quit()
                self.view.display_status("브라우저 세션이 종료되었습니다.", "info")
