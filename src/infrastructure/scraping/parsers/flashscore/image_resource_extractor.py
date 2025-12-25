import re
import config
from bs4 import BeautifulSoup
from domain.exceptions import ParsingException

class ImageResourceExtractor:
    @staticmethod
    def extract_nation_image_url(soup: BeautifulSoup):
        try:
            flag_element = soup.select_one(
                "#mc > div.container__livetable > div.container__heading > h2 > span"
            )
            
            if not flag_element:
                raise ParsingException("국가 플래그 요소를 찾을 수 없음")
            
            class_names = flag_element.get("class", [])
            class_str = " ".join(class_names) if isinstance(class_names, list) else class_names
            match = re.search(r'fl_(\d+)', class_str)
            
            if not match:
                raise ParsingException(f"플래그 클래스 패턴 매칭 실패: {class_str}")
            
            flag_number = match.group(1)
            
            return ""
            
        except Exception as e:
            if isinstance(e, ParsingException):
                raise e
            raise ParsingException("국가 이미지 URL 추출 중 예외 발생", original_exception=e)
