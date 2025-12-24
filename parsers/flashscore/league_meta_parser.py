from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from domain.models.league import League
from domain.models.team import Team
from domain.models.league_team import LeagueTeam

class LeagueMetaParser:  
    @staticmethod
    def parse_metadata(driver, league_id: str, nation: str, league_name: str, season: str = "2025-2026"):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.container__heading"))
            )
            
            league = LeagueMetaParser._parse_league_info(
                driver, league_id, nation, league_name, season
            )
            
            teams = LeagueMetaParser._parse_teams_info(driver, nation)
            
            league_teams = [
                LeagueTeam.create(
                    league_id=league_id,
                    team_id=team.team_id,
                    season=season
                )
                for team in teams
            ]
            
            return {
                'league': league,
                'teams': teams,
                'league_teams': league_teams
            }
            
        except Exception as e:
            print(f"❌ 메타데이터 파싱 중 오류: {e}")
            return {'league': None, 'teams': [], 'league_teams': []}
    
    @staticmethod
    def _parse_league_info(driver, league_id: str, nation: str, league_name: str, season: str):
        try:
            nation_ko = ""
            try:
                nation_element = driver.find_element(
                    By.CSS_SELECTOR, 
                    "#mc > div.container__livetable > div.container__heading > h2 > a:nth-child(5)"
                )
                nation_ko = nation_element.text.strip()
            except NoSuchElementException:
                print("⚠️ 국가명(한) 추출 실패")
            
            league_name_ko = ""
            try:
                league_name_element = driver.find_element(
                    By.CSS_SELECTOR,
                    "#mc > div.container__livetable > div.container__heading > div.heading > div.heading__title > div.heading__name"
                )
                league_name_ko = league_name_element.text.strip()
            except NoSuchElementException:
                print("⚠️ 리그명(한) 추출 실패")
            
            league_image_url = ""
            try:
                league_img_element = driver.find_element(
                    By.CSS_SELECTOR,
                    "#mc > div.container__livetable > div.container__heading > div.heading > img"
                )
                league_image_url = league_img_element.get_attribute("src")
            except NoSuchElementException:
                print("⚠️ 리그 이미지 URL 추출 실패")
            
            nation_image_url = LeagueMetaParser._extract_nation_image_url(driver)
            
            return League.create(
                league_id=league_id,
                nation=nation,
                nation_ko=nation_ko,
                league_name=league_name,
                league_name_ko=league_name_ko,
                league_image_url=league_image_url,
                nation_image_url=nation_image_url,
                current_season=season
            )
            
        except Exception as e:
            print(f"❌ 리그 정보 추출 중 오류: {e}")
            return None
    
    @staticmethod
    def _extract_nation_image_url(driver):
        try:
            # 국가 플래그 요소 찾기
            flag_element = driver.find_element(
                By.CSS_SELECTOR,
                "#mc > div.container__livetable > div.container__heading > h2 > span"
            )
            
            # 클래스명에서 플래그 번호 추출 (예: flag fl_198)
            class_names = flag_element.get_attribute("class")
            match = re.search(r'fl_(\d+)', class_names)
            
            if not match:
                print("⚠️ 플래그 클래스에서 번호 추출 실패")
                return ""
            
            flag_number = match.group(1)
            
            script = f"""
                var element = document.querySelector('.flag.fl_{flag_number}');
                if (element) {{
                    var style = window.getComputedStyle(element);
                    return style.backgroundImage;
                }}
                return '';
            """
            background_image = driver.execute_script(script)
            
            url_match = re.search(r'url\(["\']?([^"\']+)["\']?\)', background_image)
            if url_match:
                relative_url = url_match.group(1)
                if relative_url.startswith('/'):
                    return f"https://static.flashscore.com{relative_url}"
                elif relative_url.startswith('http'):
                    return relative_url
                else:
                    return f"https://static.flashscore.com/{relative_url}"
            
            print("⚠️ CSS에서 국가 이미지 URL 추출 실패")
            return ""
            
        except Exception as e:
            print(f"⚠️ 국가 이미지 URL 추출 중 오류: {e}")
            return ""
    
    @staticmethod
    def _parse_teams_info(driver, nation: str):
        teams = []
        
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
                        print(f"⚠️ href 파싱 실패: {href}")
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
                        print(f"⚠️ 팀 이미지 URL 추출 실패: {team_name_ko}")
                    
                    team = Team.create(
                        team_id=team_id,
                        team_name=team_name,
                        team_name_ko=team_name_ko,
                        team_image_url=team_image_url,
                        nation=nation
                    )
                    teams.append(team)
                    
                except Exception as e:
                    print(f"⚠️ 팀 정보 추출 중 오류 (개별 로우): {e}")
                    continue
            
            print(f"✅ {len(teams)}개 팀 정보 추출 완료")
            
        except Exception as e:
            print(f"❌ 팀 정보 추출 중 오류: {e}")
        
        return teams
