import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from domain.exceptions import ParsingException

class ImageResourceExtractor:
    @staticmethod
    def extract_nation_image_url(driver):
        try:
            try:
                flag_element = driver.find_element(
                    By.CSS_SELECTOR,
                    "#mc > div.container__livetable > div.container__heading > h2 > span"
                )
            except NoSuchElementException:
                raise ParsingException("국가 플래그 요소를 찾을 수 없음")
            
            class_names = flag_element.get_attribute("class")
            match = re.search(r'fl_(\d+)', class_names)
            
            if not match:
                raise ParsingException(f"플래그 클래스 패턴 매칭 실패: {class_names}")
            
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
            
            raise ParsingException("CSS backgroundImage에서 URL 추출 실패")
            
        except Exception as e:
            if isinstance(e, ParsingException):
                raise e
            raise ParsingException("국가 이미지 URL 추출 중 예외 발생", original_exception=e)
