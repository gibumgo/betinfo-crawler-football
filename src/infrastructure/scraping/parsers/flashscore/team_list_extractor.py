import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from domain.models.team import Team
from domain.exceptions import ParsingException

class TeamListExtractor:
    @staticmethod
    def extract(driver, nation: str):
        teams = []
        errors = []
        
        try:
            table_body = driver.find_element(
                By.CSS_SELECTOR,
                "#tournament-table-tabs-and-content > div:nth-child(3) > div:nth-child(1) > div > div > div.ui-table__body"
            )
            
            rows = table_body.find_elements(By.CSS_SELECTOR, "div.ui-table__row")
            
            for row in rows:
                try:
                    team_link = row.find_element(By.CSS_SELECTOR, "a.tableCellParticipant__name")
                    team_name_ko = team_link.text.strip()
                    href = team_link.get_attribute("href")
                    
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
                        team_img = row.find_element(
                            By.CSS_SELECTOR, 
                            "a.tableCellParticipant__image > img"
                        )
                        team_image_url = team_img.get_attribute("src")
                    except NoSuchElementException:
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
                        context={'row_text': row.text[:30] if row else 'N/A'}
                    ))
                    continue
            
        except Exception as e:
            errors.append(ParsingException(
                message="팀 테이블 전체 파싱 실패",
                original_exception=e
            ))
        
        return teams, errors
