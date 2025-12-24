from infrastructure.scraping.drivers.chrome_driver_factory import ChromeDriverFactory
from infrastructure.scraping.scrapers.betinfo_page import BetinfoPage
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from application.services.betinfo_service import BetinfoService
from presentation.views.console_view import ConsoleView

class BetinfoController:
    def __init__(self, view: ConsoleView, repository: BetinfoRepository, error_handler):
        self.view = view
        self.repository = repository
        self.error_handler = error_handler

    def start_collection(self):
        self.error_handler.execute(self._process_collection)

    def _process_collection(self):
        self.view.display_betinfo_settings()
        start_round = input("➡️ 시작 회차: ").strip()
        end_round = input("➡️ 종료 회차: ").strip()
        
        if not (start_round.isdigit() and end_round.isdigit()):
            self.view.display_invalid_round_input()
            return

        driver = None
        try:
            self.view.display_browser_initializing()
            driver = ChromeDriverFactory.create()
            
            page = BetinfoPage(driver)
            service = BetinfoService(page=page, repository=self.repository)
            
            for round_num in range(int(start_round), int(end_round) + 1):
                round_val = str(round_num)
                self.view.display_processing_round(round_val)
                service.collect_round(round_val)
                
            self.view.display_all_rounds_complete()
            
        finally:
            if driver:
                driver.quit()

