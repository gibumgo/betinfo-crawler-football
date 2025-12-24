from infrastructure.scraping.scrapers.flashscore.flashscore_page import FlashscorePage
from infrastructure.scraping.parsers.flashscore.league_meta_parser import LeagueMetaParser
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from config import DEFAULT_SEASON

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
        season: str = DEFAULT_SEASON
    ):
        self.page.goto_standings(nation, league_name, league_id)
        
        metadata = LeagueMetaParser.parse_metadata(
            self.driver, 
            league_id, 
            nation, 
            league_name, 
            season
        )
        
        if not metadata['league'] and not metadata['errors']:
            return {
                'success': False,
                'error': '리그 정보 추출 실패'
            }
            
        if metadata.get('errors'):
            print(f"⚠️ 파싱 중 {len(metadata['errors'])}건의 오류가 발생했습니다:")
            for err in metadata['errors']:
                print(f" - {err}")
        
        if metadata['league']:
            self.repository.save_leagues([metadata['league']])
        
        if metadata['teams']:
            self.repository.save_teams(metadata['teams'], nation)
        
        if metadata['league_teams']:
            self.repository.save_league_teams(metadata['league_teams'])
        
        return {
            'success': True if metadata['league'] else False,
            'league': metadata['league'],
            'teams': metadata['teams'],
            'league_teams': metadata['league_teams'],
            'team_count': len(metadata['teams']),
            'relation_count': len(metadata['league_teams']),
            'errors': [str(e) for e in metadata.get('errors', [])]
        }

