from driver.chrome_driver_factory import ChromeDriverFactory
from scraper.betinfo_page import BetinfoPage
from repository.csv_repository import CSVRepository
from service.proto_service import ProtoService
from view.console_view import ConsoleView

class BetinfoController:
    def __init__(self):
        self.view = ConsoleView()
        self.repository = CSVRepository()

    def start_collection(self):
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
            service = ProtoService(page=page, repository=self.repository)
            
            for round_num in range(int(start_round), int(end_round) + 1):
                round_val = str(round_num)
                self.view.display_processing_round(round_val)
                service.collect_round(round_val)
                
            self.view.display_all_rounds_complete()
            
        except Exception as e:
            self.view.display_betinfo_collection_error(e)
        finally:
            if driver:
                driver.quit()

