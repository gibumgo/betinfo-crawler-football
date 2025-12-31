import sys
from application.services.betinfo_service import BetinfoService
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from infrastructure.scraping.drivers.chrome_driver_factory import ChromeDriverFactory
from infrastructure.scraping.scrapers.betinfo_page import BetinfoPage
from infrastructure.storage.history_manager import HistoryManager
from shared.ipc_messenger import IPCMessenger

from infrastructure.constants.crawler_constants import CRAWLER_BETINFO
from infrastructure.constants.error_codes import ERR_INVALID_ARGUMENT, ERR_RUNTIME_FAILURE
from infrastructure.constants.ipc_constants import LOG_LEVEL_INFO, LOG_LEVEL_WARN

class CliBetinfoController:
    def __init__(self, repository: BetinfoRepository):
        self.repository = repository
        self.history_manager = HistoryManager()

    def run(self, args):
        session_id = self.history_manager.start_session(mode=CRAWLER_BETINFO, args=vars(args))
        IPCMessenger.send_status("START", "Betinfo Crawler Started")
        
        target_rounds = self._resolve_target_rounds(args)
        
        if not args.recent and not target_rounds:
            msg = "No target rounds specified. Use --recent or --rounds."
            IPCMessenger.send_error(ERR_INVALID_ARGUMENT, msg)
            self.history_manager.end_session(session_id, "FAILED", error=msg)
            return

        self.driver = None
        try:
            IPCMessenger.log("Initializing Chrome Driver...", level=LOG_LEVEL_INFO)
            self.driver = ChromeDriverFactory.create()
            
            page = BetinfoPage(self.driver)
            
            service = BetinfoService(
                page=page, 
                repository=self.repository, 
                output_dir=args.output_dir,
                skip_existing=args.skip_existing
            )
            
            self._process_collection(service, target_rounds, args)
            
            summary = f"Processed rounds"
            IPCMessenger.send_status("COMPLETE", summary)
            self.history_manager.end_session(session_id, "SUCCESS", summary=summary)
            
        except Exception as e:
            error_msg = str(e)
            IPCMessenger.send_error(ERR_RUNTIME_FAILURE, str(e))
            
            import traceback
            tb = traceback.format_exc()
            IPCMessenger.log(tb, level="ERROR")
            
            self.history_manager.end_session(session_id, "FAILED", error=str(e))
            
        finally:
            self.stop()

    def stop(self):
        if self.driver:
            try:
                self.driver.quit()
                IPCMessenger.log("Browser Closed", level=LOG_LEVEL_INFO)
            except Exception:
                pass
            self.driver = None

    def _resolve_target_rounds(self, args) -> list[str]:
        import datetime
        rounds = []
        year = str(args.year) if args.year else str(datetime.datetime.now().year)
        
        def format_round(r_val):
            r_str = str(r_val).strip()
            if len(r_str) > 3:
                return r_str
            return f"{year}{r_str.zfill(3)}"

        if args.rounds:
            raw_rounds = [r.strip() for r in args.rounds.split(",") if r.strip()]
            rounds = [format_round(r) for r in raw_rounds]
            
        elif args.start_round and args.end_round:
            try:
                start = int(args.start_round)
                end = int(args.end_round)
                rounds = [format_round(r) for r in range(start, end + 1)]
            except ValueError:
                IPCMessenger.send_error(ERR_INVALID_ARGUMENT, "Round range must be integers")
        return rounds

    def _process_collection(self, service: BetinfoService, rounds: list[str], args):
        if args.recent:
            IPCMessenger.log(f"Auto-detecting top {args.recent} recent rounds...", level=LOG_LEVEL_INFO)
            if hasattr(service, 'collect_latest_rounds'):
                service.collect_latest_rounds(limit=args.recent)
            else:
                IPCMessenger.log("collect_latest_rounds method not implemented yet.", level=LOG_LEVEL_WARN)
            return

        total = len(rounds)
        for idx, round_val in enumerate(rounds):
            IPCMessenger.send_status("COLLECTING_ROUND", round_val)
            IPCMessenger.send_progress((idx / total) * 100)
            
            try:
                year_context = None
                if len(round_val) >= 4 and round_val[:4].isdigit():
                    year_context = round_val[:4]
                
                service.collect_round(round_val, year=year_context)
            except Exception as e:
                IPCMessenger.log(f"Failed to collect round {round_val}: {e}", level=LOG_LEVEL_WARN)
                
        IPCMessenger.send_progress(100)
