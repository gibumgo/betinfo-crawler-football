import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BetinfoPage:
    URL = "https://www.betinfo.co.kr/z_protorate/protoRate2.asp"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def navigate_to_year(self, year_value: str):
        year_selector = "#mainContent > div:nth-child(5) > span > form > table.searchTable > tbody > tr:nth-child(1) > td:nth-child(5) > select:nth-child(1)"
        year_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, year_selector))
        )
        self.driver.execute_script(f"arguments[0].value='{year_value}';", year_element)
        self.driver.execute_script("getyearround(arguments[0]);", year_element)
        time.sleep(1.0)

    def navigate_to_round(self, round_value: str):
        round_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "YearRound"))
        )
        self.driver.execute_script(f"arguments[0].value='{round_value}';", round_element)
        self.driver.execute_script("pr_number_onchange(arguments[0]);", round_element)
        time.sleep(1.0)

    def extract_match_elements(self):
        return self.driver.find_elements(
            By.CSS_SELECTOR, '#listView > tbody > tr[league_gubun="1"]'
        )

    def wait_until_table_loaded(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "listView"))
        )
