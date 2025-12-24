from driver.chrome_driver_factory import ChromeDriverFactory
from scraper.flashscore.flashscore_page import FlashscorePage
from repository.flashscore_repository import FlashscoreRepository
from service.flashscore_service import FlashscoreService
from service.flashscore_meta_service import FlashscoreMetaService
from view.console_view import ConsoleView

class FlashscoreController:
    def __init__(self):
        self.view = ConsoleView()
        self.repository = FlashscoreRepository()

    def start_collection(self):
        while True:
            self.view.display_flashscore_menu()
            choice = self.view.get_flashscore_choice()
            
            if choice == 'B':
                return
            elif choice == '1':
                self._collect_match_data()
                break
            elif choice == '2':
                self._collect_metadata()
                break
            else:
                self.view.display_status("잘못된 입력입니다. 다시 선택해주세요.", "warning")
    
    def _collect_match_data(self):
        params = self.view.get_collection_params()
        
        driver = None
        try:
            self.view.display_status("브라우저를 초기화 중입니다...", "working")
            driver = ChromeDriverFactory.create()
            
            page = FlashscorePage(driver)
            service = FlashscoreService(page, self.repository)
            
            self.view.display_match_collection_start(params['season'], params['league_path'])
            
            if params['start_round'] is not None:
                self.view.display_loading_round(params['start_round'])
            
            result = service.collect_matches_data(
                league_path=params["league_path"],
                season=params["season"],
                start_round=params["start_round"],
                end_round=params["end_round"]
            )
            
            self.view.display_match_collection_result(result)
            self.view.display_status("데이터 저장 및 후처리가 완료되었습니다.", "success")
            
        except Exception as e:
            self.view.display_status(f"수집 작업 중 오류 발생: {e}", "error")
            
        finally:
            if driver:
                driver.quit()
                self.view.display_status("브라우저 세션이 종료되었습니다.", "info")
    
    def _collect_metadata(self):
        params = self.view.get_metadata_params()
        
        if not params:
            self.view.display_status("메타데이터 수집이 취소되었습니다.", "warning")
            return
        
        driver = None
        try:
            self.view.display_status("브라우저를 초기화 중입니다...", "working")
            driver = ChromeDriverFactory.create()
            
            meta_service = FlashscoreMetaService(driver, self.repository)
            
            self.view.display_metadata_collection_start(
                params["nation"],
                params["league_name"],
                params["league_id"],
                params["season"]
            )
            
            self.view.display_status("🔗 순위표 페이지로 이동 중...", "working")
            
            result = meta_service.collect_metadata(
                nation=params["nation"],
                league_name=params["league_name"],
                league_id=params["league_id"],
                season=params["season"]
            )
            
            if result['success']:
                self.view.display_status("✅ 순위표 페이지 로딩 완료", "success")
                self.view.display_status("🔍 메타데이터 파싱 중...", "working")
                self.view.display_status("💾 데이터 저장 중...", "working")
            
            self.view.display_metadata_collection_result(result)
            
        except Exception as e:
            self.view.display_status(f"메타데이터 수집 중 오류 발생: {e}", "error")
            import traceback
            traceback.print_exc()
            
        finally:
            if driver:
                driver.quit()
                self.view.display_status("브라우저 세션이 종료되었습니다.", "info")

