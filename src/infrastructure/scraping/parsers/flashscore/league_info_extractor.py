from bs4 import BeautifulSoup
from domain.models.league import League
from domain.exceptions import ParsingException
from infrastructure.scraping.parsers.flashscore.image_resource_extractor import ImageResourceExtractor

class LeagueInfoExtractor:
    @staticmethod
    def extract(html_content: str, league_id: str, nation: str, league_name: str, season: str):
        errors_context = {}
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            nation_ko = ""
            try:
                nation_element = soup.select_one(
                    "#mc > div.container__livetable > div.container__heading > h2 > a:nth-child(5)"
                )
                if nation_element:
                    nation_ko = nation_element.get_text(strip=True)
            except Exception:
                errors_context['nation_ko_error'] = "국가명(한) 요소 없음"
            
            league_name_ko = ""
            try:
                league_name_element = soup.select_one(
                    "#mc > div.container__livetable > div.container__heading > div.heading > div.heading__title > div.heading__name"
                )
                if league_name_element:
                    league_name_ko = league_name_element.get_text(strip=True)
            except Exception:
                errors_context['league_name_ko_error'] = "리그명(한) 요소 없음"
            
            league_image_url = ""
            try:
                league_img_element = soup.select_one(
                    "#mc > div.container__livetable > div.container__heading > div.heading > img"
                )
                if league_img_element:
                    league_image_url = league_img_element.get("src", "")
            except Exception:
                errors_context['league_image_error'] = "리그 이미지 요소 없음"
            
            try:
                nation_image_url = ImageResourceExtractor.extract_nation_image_url(soup)
            except ParsingException as e:
                nation_image_url = ""
                errors_context['nation_image_error'] = str(e)
            
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
            raise ParsingException(
                message="리그 상세 정보 파싱 중 치명적 오류",
                original_exception=e,
                context=errors_context
            )
