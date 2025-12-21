from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class BaseScraper(ABC):
    def __init__(self, driver):
        self.update_driver(driver)

    def update_driver(self, driver):
        """드라이버 세션 재시작 시 내부 참조를 최신화합니다."""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    @abstractmethod
    def open(self):
        pass

    def open_url(self, url: str):
        self.driver.get(url)

    def wait_for_element(self, css_selector: str, timeout: int = 15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception:
            raise Exception(f"요소를 찾을 수 없습니다: {css_selector}")

    def click_show_more(self, selector: str = ".event__more") -> bool:
        """'더 보기' 버튼을 찾아 클릭합니다."""
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            self.driver.execute_script("arguments[0].click();", button)
            time.sleep(1.5)
            return True
        except:
            return False
