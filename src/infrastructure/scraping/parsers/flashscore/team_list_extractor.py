import re
from bs4 import BeautifulSoup
from domain.models.team import Team
from domain.exceptions import ParsingException

class TeamListExtractor:
    @staticmethod
    def extract(html_content: str, nation: str):
        teams = []
        errors = []
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            table_body = soup.select_one(
                "#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body"
            )
            
            if not table_body:
                errors.append(ParsingException(
                    message="팀 테이블 본문을 찾을 수 없음"
                ))
                return teams, errors
            
            rows = table_body.select("div.ui-table__row")
            
            for row in rows:
                try:
                    team_link = row.select_one("a.tableCellParticipant__name")
                    if not team_link:
                        continue
                        
                    team_name_ko = team_link.get_text(strip=True)
                    href = team_link.get("href", "")
                    
                    match = re.search(r'/team/([^/]+)/([^/]+)/', href)
                    if not match:
                        errors.append(ParsingException(
                            message=f"href 파싱 실패: {href}",
                            context={'href': href}
                        ))
                        continue
                    
                    team_name = match.group(1)
                    team_id = match.group(2)
                    
                    team_image_url = ""
                    try:
                        team_img = row.select_one("a.tableCellParticipant__image > img")
                        if team_img:
                            team_image_url = team_img.get("src", "")
                    except Exception:
                        pass
                    
                    team = Team.create(
                        team_id=team_id,
                        team_name=team_name,
                        team_name_ko=team_name_ko,
                        team_image_url=team_image_url,
                        nation=nation
                    )
                    teams.append(team)
                    
                except Exception as e:
                    errors.append(ParsingException(
                        message="팀 정보 추출 중 오류 (개별 로우)",
                        original_exception=e,
                        context={'row_text': row.get_text()[:30] if row else 'N/A'}
                    ))
                    continue
            
        except Exception as e:
            errors.append(ParsingException(
                message="팀 테이블 전체 파싱 실패",
                original_exception=e
            ))
        
        return teams, errors
