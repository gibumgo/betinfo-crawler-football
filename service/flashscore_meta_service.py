from scraper.flashscore.flashscore_page import FlashscorePage
from parsers.flashscore.league_meta_parser import LeagueMetaParser
from repository.flashscore_repository import FlashscoreRepository

class FlashscoreMetaService:
    def __init__(self, driver, repository: FlashscoreRepository):
        self.driver = driver
        self.repository = repository
        self.page = FlashscorePage(driver)
    
    def collect_metadata(
        self, 
        nation: str, 
        league_name: str, 
        league_id: str, 
        season: str = "2025-2026"
    ):
        self.page.goto_standings(nation, league_name, league_id)
        
        metadata = LeagueMetaParser.parse_metadata(
            self.driver, 
            league_id, 
            nation, 
            league_name, 
            season
        )
        
        if not metadata['league']:
            return {
                'success': False,
                'error': '리그 정보 추출 실패'
            }
        
        self.repository.save_leagues([metadata['league']])
        
        if metadata['teams']:
            self.repository.save_teams(metadata['teams'], nation)
        
        if metadata['league_teams']:
            self.repository.save_league_teams(metadata['league_teams'])
        
        return {
            'success': True,
            'league': metadata['league'],
            'teams': metadata['teams'],
            'league_teams': metadata['league_teams'],
            'team_count': len(metadata['teams']),
            'relation_count': len(metadata['league_teams'])
        }

