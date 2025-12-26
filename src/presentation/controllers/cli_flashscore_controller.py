import sys
from application.services.flashscore_service import FlashscoreService
from application.services.flashscore_meta_service import FlashscoreMetaService
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from infrastructure.scraping.drivers.chrome_driver_factory import ChromeDriverFactory
from infrastructure.scraping.scrapers.flashscore.flashscore_page import FlashscorePage
from infrastructure.storage.history_manager import HistoryManager

from infrastructure.constants.crawler_constants import (
    CRAWLER_FLASH, FLASH_TASK_METADATA, FLASH_TASK_MATCHES
)
from infrastructure.constants.error_codes import (
    ERR_SUCCESS, ERR_INVALID_ARGUMENT, ERR_RUNTIME_FAILURE
)
from infrastructure.constants.ipc_constants import LOG_LEVEL_INFO, LOG_LEVEL_ERROR
from shared.ipc_messenger import IPCMessenger

class CliFlashscoreController:
    
    def __init__(self, repository: FlashscoreRepository):
        self.repository = repository
        self.history_manager = HistoryManager()

    def run(self, args):
        session_id = self.history_manager.start_session(CRAWLER_FLASH, vars(args))
        IPCMessenger.send_status("START", "Flashscore Crawler Started")
        
        if not args.task:
             msg = "Task is required for Flashscore mode (e.g., --task matches)"
             IPCMessenger.send_error(ERR_INVALID_ARGUMENT, msg)
             self.history_manager.end_session(session_id, "FAILED", error=msg)
             return

        driver = None
        try:
            IPCMessenger.log("Initializing Chrome Driver...", level=LOG_LEVEL_INFO)
            driver = ChromeDriverFactory.create()
            
            page = FlashscorePage(driver) 

            service = FlashscoreService(page=page, repository=self.repository)
            
            if args.task == FLASH_TASK_METADATA:
                self._collect_metadata(service, args)
            elif args.task == FLASH_TASK_MATCHES:
                self._collect_matches(service, args)
            else:
                 raise ValueError(f"Unknown task: {args.task}")

            IPCMessenger.send_status("COMPLETE", "Task Finished")
            self.history_manager.end_session(session_id, "SUCCESS", summary=f"Task {args.task} completed")

        except Exception as e:
            error_msg = str(e)
            IPCMessenger.send_error(ERR_RUNTIME_FAILURE, f"Crawling Failed: {error_msg}")
            
            import traceback
            tb = traceback.format_exc()
            IPCMessenger.log(tb, level=LOG_LEVEL_ERROR)
            
            self.history_manager.end_session(session_id, "FAILED", error=error_msg)
            
        finally:
            if driver:
                try:
                    driver.quit()
                    IPCMessenger.log("Browser Closed", level=LOG_LEVEL_INFO)
                except Exception:
                    pass

    def _collect_metadata(self, service: FlashscoreService, args):
        IPCMessenger.log("Starting Metadata Collection...", level=LOG_LEVEL_INFO)
        
        # Note: 'service' passed here is FlashscoreService, but we need FlashscoreMetaService.
        # We need access to the driver. Since 'driver' is local to 'run', 
        # we can access it via service.page.driver because FlashscorePage has self.driver.
        
        driver = service.page.driver
        meta_service = FlashscoreMetaService(driver, self.repository)
        
        league_path = self._extract_path_from_url(args.url)
        if not league_path:
             raise ValueError("Invalid URL format. Expected URL containing /soccer/ or /football/...")

        league_id = self._extract_league_id_from_url(args.url)
        if not league_id:
            raise ValueError("Invalid Standings URL. Could not find League ID (e.g., .../standings/#/ID/...).")

        nation = self._extract_nation(league_path)
        league_name = self._extract_league_name(league_path)

        result = meta_service.collect_metadata(
            nation=nation,
            league_name=league_name,
            league_id=league_id,
            season=args.season
        )
        
        if result.get('success'):
             IPCMessenger.log(f"Metadata collected successfully. Teams: {result.get('team_count', 0)}", level=LOG_LEVEL_INFO)
        else:
             errs = result.get('errors', [])
             if errs:
                  for e in errs:
                       IPCMessenger.log(f"Metadata Error: {e}", level=LOG_LEVEL_ERROR)
             raise RuntimeError("Metadata collection failed or returned incomplete data.")

    def _extract_league_id_from_url(self, url: str) -> str:
        # Expected format: .../standings/#/OEEq9Yvp/standings/overall/
        # or .../standings/#/OEEq9Yvp/
        if "/standings/#/" not in url:
            return None
        
        try:
            # Split by /standings/#/
            parts = url.split("/standings/#/")
            if len(parts) > 1:
                # The ID is essentially the first part after #/
                # e.g. OEEq9Yvp/standings/overall/
                after_hash = parts[1]
                
                # Split by / to get the ID
                id_part = after_hash.split("/")[0]
                if id_part:
                    return id_part
            return None
        except Exception:
            return None

    def _extract_nation(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        # /soccer/england/premier-league/ -> england
        if len(parts) >= 2:
            return parts[1]
        return "unknown"

    def _collect_matches(self, service: FlashscoreService, args):
         IPCMessenger.log("Starting Match Data Collection...", level=LOG_LEVEL_INFO)
         
         league_path = self._extract_path_from_url(args.url)
         if not league_path:
             raise ValueError("Invalid URL format. Expected URL containing /football/...")
             
         service.collect_matches_data(
             league_path=league_path,
             league_name=self._extract_league_name(league_path),
             season=args.season,
             start_round=args.fs_start_round,
             end_round=args.fs_end_round
         )

    def _extract_path_from_url(self, url: str) -> str:
        # Check for typical Flashscore URL pattern
        if "/soccer/" not in url and "/football/" not in url:
            # Fallback for old style or specific inputs, though user said 'soccer' is correct for .co.kr
            if "flashscore" not in url:
                return None
        
        try:
            # Normalize to path only
            if "://" in url:
                start_idx = url.find("/soccer/")
                if start_idx == -1:
                     start_idx = url.find("/football/")
                
                if start_idx != -1:
                     path = url[start_idx:]
                else:
                     # Fallback: maybe just path was given?
                     path = url
            else:
                path = url

            # Strip known suffixes to get the base league path
            # Suffixes: /results/, /fixtures/, /standings/
            for suffix in ["/results", "/fixtures", "/standings"]:
                if suffix in path:
                    path = path.split(suffix)[0]
            
            # Ensure trailing slash for consistency if needed, 
            # but FlashscorePage.open_results_page does rstrip('/'), so it's fine.
            # However, to be clean, let's keep it clean.
            
            # Remove hash or query params
            if "?" in path:
                path = path.split("?")[0]
            if "#" in path:
                path = path.split("#")[0]
                
            return path
        except ValueError:
            return None

    def _extract_league_name(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        # /football/england/premier-league/ -> premier-league
        # /football/england/premier-league-2023-2024/ -> premier-league
        if len(parts) >= 3:
            name = parts[2]
            # Strip year suffix like -2023-2024
            import re
            name = re.sub(r'-\d{4}-\d{4}$', '', name)
            return name
        return "unknown-league"
