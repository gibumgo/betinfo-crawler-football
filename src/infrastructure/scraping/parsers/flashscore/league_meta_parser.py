from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from domain.models.league_team import LeagueTeam
from config import DEFAULT_SEASON
from domain.exceptions import ParsingException
from infrastructure.scraping.parsers.flashscore.league_info_extractor import LeagueInfoExtractor
from infrastructure.scraping.parsers.flashscore.team_list_extractor import TeamListExtractor

class LeagueMetaParser:  
    @staticmethod
    def parse_metadata(driver, league_id: str, nation: str, league_name: str, season: str = DEFAULT_SEASON):
        result = {
            'league': None,
            'teams': [],
            'league_teams': [],
            'errors': []
        }
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.container__heading"))
            )
            
            try:
                result['league'] = LeagueInfoExtractor.extract(
                    driver, league_id, nation, league_name, season
                )
            except Exception as e:
                if isinstance(e, ParsingException):
                    result['errors'].append(e)
                else:
                    result['errors'].append(ParsingException(
                        message="리그 정보 추출 실패",
                        original_exception=e,
                        context={'league_id': league_id}
                    ))
            
            try:
                teams, team_errors = TeamListExtractor.extract(driver, nation)
                result['teams'] = teams
                result['errors'].extend(team_errors)
                
                result['league_teams'] = [
                    LeagueTeam.create(
                        league_id=league_id,
                        team_id=team.team_id,
                        season=season
                    )
                    for team in result['teams']
                ]
            except Exception as e:
                result['errors'].append(ParsingException(
                    message="팀 목록 추출 및 관계 생성 실패",
                    original_exception=e,
                    context={'league_id': league_id}
                ))
            
            return result
            
        except Exception as e:
            result['errors'].append(ParsingException(
                message="메타데이터 파싱 중 알 수 없는 오류",
                original_exception=e
            ))
            return result
