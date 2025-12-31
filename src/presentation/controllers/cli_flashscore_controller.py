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
from application.services.flashscore_discovery_service import FlashscoreDiscoveryService
from infrastructure.constants.crawler_constants import (
    CRAWLER_FLASH, FLASH_TASK_METADATA, FLASH_TASK_MATCHES, FLASH_TASK_DISCOVER, FLASH_TASK_INTEGRATED
)

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

        if args.task == FLASH_TASK_DISCOVER:
            if args.country:
                try:
                    self._discover_leagues(args)
                    IPCMessenger.send_status("COMPLETE", "Discovery Finished")
                    self.history_manager.end_session(session_id, "SUCCESS", summary=f"Discovery completed for {args.country}")
                except Exception as e:
                    IPCMessenger.send_error(ERR_RUNTIME_FAILURE, f"Discovery Failed: {e}")
            else:
                try:
                    self._discover_countries(args)
                    IPCMessenger.send_status("COMPLETE", "Discovery Finished")
                    self.history_manager.end_session(session_id, "SUCCESS", summary="Country Discovery completed")
                except Exception as e:
                     IPCMessenger.send_error(ERR_RUNTIME_FAILURE, f"Discovery Failed: {e}")
            
            return

        self.driver = None
        try:
            IPCMessenger.log("Initializing Chrome Driver...", level=LOG_LEVEL_INFO)
            self.driver = ChromeDriverFactory.create()
            
            page = FlashscorePage(self.driver) 

            service = FlashscoreService(page=page, repository=self.repository)
            
            if args.task == FLASH_TASK_METADATA:
                self._collect_metadata(service, args)
            elif args.task == FLASH_TASK_MATCHES:
                self._collect_matches(service, args)
            elif args.task == FLASH_TASK_INTEGRATED:
                self._collect_integrated(service, args)
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
            self.stop()

    def stop(self):
        if self.driver:
            try:
                self.driver.quit()
                IPCMessenger.log("Browser Closed", level=LOG_LEVEL_INFO)
            except Exception:
                pass
            self.driver = None

    def _collect_metadata(self, service: FlashscoreService, args):
        IPCMessenger.log("Starting Metadata Collection...", level=LOG_LEVEL_INFO)
        
        driver = service.page.driver
        meta_service = FlashscoreMetaService(driver, self.repository)
        
        url = args.url
        if not url and args.country and args.league:
            url = self._construct_league_url(args.country, args.league, "standings")
            IPCMessenger.log(f"Auto-constructed Standings URL: {url}", level=LOG_LEVEL_INFO)

        if not url:
            raise ValueError("URL or both Country and League must be specified for metadata task.")

        league_path = self._extract_path_from_url(url)
        if not league_path:
             raise ValueError("Invalid URL format. Expected URL containing /soccer/ or /football/...")

        league_id = self._extract_league_id_from_url(url)
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
             IPCMessenger.send_data("METADATA_RESULT", result)
        else:
             errs = result.get('errors', [])
             if errs:
                  for e in errs:
                       IPCMessenger.log(f"Metadata Error: {e}", level=LOG_LEVEL_ERROR)
             raise RuntimeError("Metadata collection failed or returned incomplete data.")

    def _construct_league_url(self, country: str, league: str, subpath: str = "") -> str:
        from config import FLASHSCORE_BASE_URL
        base = FLASHSCORE_BASE_URL.rstrip('/')
        url = f"{base}/soccer/{country}/{league}/"
        if subpath:
            url += f"{subpath}/"
        return url

    def _extract_league_id_from_url(self, url: str) -> str:
        if "/standings/#/" not in url:
            return None
        
        try:
            parts = url.split("/standings/#/")
            if len(parts) > 1:
                after_hash = parts[1]
                
                id_part = after_hash.split("/")[0]
                if id_part:
                    return id_part
            return None
        except Exception:
            return None

    def _extract_nation(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2:
            return parts[1]
        return "unknown"

    def _collect_matches(self, service: FlashscoreService, args):
         IPCMessenger.log("Starting Match Data Collection...", level=LOG_LEVEL_INFO)
         
         url = args.url
         if not url and args.country and args.league:
             league_slug = args.league
             if args.season and args.season not in league_slug:
                 league_slug = f"{league_slug}-{args.season}"
             
             url = self._construct_league_url(args.country, league_slug, "results")
             IPCMessenger.log(f"Auto-constructed Results URL: {url}", level=LOG_LEVEL_INFO)

         if not url:
             raise ValueError("URL or both Country and League must be specified for matches task.")

         league_path = self._extract_path_from_url(url)
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
        if "/soccer/" not in url and "/football/" not in url:
            if "flashscore" not in url:
                return None
        
        try:
            if "://" in url:
                start_idx = url.find("/soccer/")
                if start_idx == -1:
                     start_idx = url.find("/football/")
                
                if start_idx != -1:
                     path = url[start_idx:]
                else:
                     path = url
            else:
                path = url

            for suffix in ["/results", "/fixtures", "/standings"]:
                if suffix in path:
                    path = path.split(suffix)[0]
            
            if "?" in path:
                path = path.split("?")[0]
            if "#" in path:
                path = path.split("#")[0]
                
            return path
        except ValueError:
            return None

    def _extract_league_name(self, path: str) -> str:
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 3:
            name = parts[2]
            import re
            name = re.sub(r'-\d{4}-\d{4}$', '', name)
            return name
        return "unknown-league"

    def _discover_leagues(self, args):
        IPCMessenger.log(f"Discovering leagues for {args.country}...", level=LOG_LEVEL_INFO)
        discovery_service = FlashscoreDiscoveryService()
        leagues = discovery_service.discover_leagues(args.country)
        IPCMessenger.send_data("LEAGUES", leagues)
        if not leagues:
             IPCMessenger.send_error(ERR_RUNTIME_FAILURE, f"No leagues found for {args.country}")

    def _discover_countries(self, args):
        IPCMessenger.log(f"Discovering countries...", level=LOG_LEVEL_INFO)
        discovery_service = FlashscoreDiscoveryService()
        countries = discovery_service.discover_countries()
        IPCMessenger.send_data("COUNTRIES", countries)
        if not countries:
             IPCMessenger.send_error(ERR_RUNTIME_FAILURE, "No countries found")
             
    def _collect_integrated(self, service: FlashscoreService, args):
         IPCMessenger.log("Starting Integrated Collection...", level=LOG_LEVEL_INFO)
         
         country = args.country
         league = args.league
         
         if not country or not league:
             if args.url:
                 league_path = self._extract_path_from_url(args.url)
                 if league_path:
                     country = self._extract_nation(league_path)
                     league = self._extract_league_name(league_path)
         
         if not country or not league:
             raise ValueError("Country and League must be specified via arguments or URL.")
         
         service.collect_season_data_integrated(
             country=country,
             league=league,
             season=args.season,
             options={
                 'skip_standings': False,
                 'force_full': not args.resume if hasattr(args, 'resume') else False 
             }
         )

