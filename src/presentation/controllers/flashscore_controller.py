from infrastructure.scraping.drivers.chrome_driver_factory import ChromeDriverFactory
from infrastructure.scraping.scrapers.flashscore.flashscore_page import FlashscorePage
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from application.services.flashscore_service import FlashscoreService
from application.services.flashscore_meta_service import FlashscoreMetaService
from presentation.views.console_view import ConsoleView

class FlashscoreController:
    def __init__(self, view: ConsoleView, repository: FlashscoreRepository, error_handler):
        self.view = view
        self.repository = repository
        self.error_handler = error_handler

    def start_collection(self):
        while True:
            self.view.display_flashscore_menu()
            choice = self.view.get_flashscore_choice()
            
            if choice == 'B':
                return
            elif choice == '1':
                self.error_handler.execute(self._collect_match_data)
                break
            elif choice == '2':
                self.error_handler.execute(self._collect_metadata)
                break
            else:
                self.view.display_invalid_choice()
    
    def _collect_match_data(self):
        params = self.view.get_collection_params()
        
        driver = None
        try:
            self.view.display_browser_initializing()
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
            self.view.display_match_data_complete()
            
        finally:
            if driver:
                driver.quit()
                self.view.display_browser_closed()
    
    def _collect_metadata(self):
        params = self.view.get_metadata_params()
        
        if not params:
            self.view.display_metadata_collection_canceled()
            return
        
        driver = None
        try:
            self.view.display_browser_initializing()
            driver = ChromeDriverFactory.create()
            
            meta_service = FlashscoreMetaService(driver, self.repository)
            
            self.view.display_metadata_collection_start(
                params["nation"],
                params["league_name"],
                params["league_id"],
                params["season"]
            )
            
            self.view.display_navigating_to_standings()
            
            result = meta_service.collect_metadata(
                nation=params["nation"],
                league_name=params["league_name"],
                league_id=params["league_id"],
                season=params["season"]
            )
            
            if result['success']:
                self.view.display_standings_loaded()
                self.view.display_parsing_metadata()
                self.view.display_saving_data()
            
            self.view.display_metadata_collection_result(result)
            
        finally:
            if driver:
                driver.quit()
                self.view.display_browser_closed()

