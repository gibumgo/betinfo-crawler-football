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
        print("\n[Betinfo 수집 설정]")
        start_round = input("➡️ 시작 회차: ").strip()
        end_round = input("➡️ 종료 회차: ").strip()
        
        if not (start_round.isdigit() and end_round.isdigit()):
            self.view.display_status("회차는 숫자만 입력 가능합니다.", "error")
            return

        driver = None
        try:
            self.view.display_status("브라우저를 초기화 중입니다...", "working")
            driver = ChromeDriverFactory.create()
            
            page = BetinfoPage(driver)
            service = ProtoService(page=page, repository=self.repository)
            
            for round_num in range(int(start_round), int(end_round) + 1):
                round_val = str(round_num)
                self.view.display_status(f"{round_val} 회차 처리 중...", "working")
                service.collect_round(round_val)
                
            self.view.display_status("모든 회차 수집이 완료되었습니다.", "success")
            
        except Exception as e:
            self.view.display_status(f"Betinfo 수집 중 오류: {e}", "error")
        finally:
            if driver:
                driver.quit()
