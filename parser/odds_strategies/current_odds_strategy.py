# parser/odds_strategies/current_odds_strategy.py

from selenium.webdriver.common.by import By
from .base_odds_strategy import BaseOddsStrategy


class CurrentOddsStrategy(BaseOddsStrategy):
    """
    현재 배당 파싱 전략
    
    특징:
    - span 태그 안의 배당 값을 추출
    - span이 없으면 초기 배당과 동일
    
    구조 예시:
        2.06
        <span>2.16</span>(0.10)↑
        
    → 현재 배당: 2.16
    """
    
    def parse(self, td_element) -> str:
        """
        현재 배당 값을 파싱합니다.
        
        Args:
            td_element: 배당 정보가 포함된 td 요소
            
        Returns:
            현재 배당 값 (span 태그 안의 값, 없으면 초기 배당)
        """
        try:
            # span 태그 안의 값이 현재 배당
            span_elements = td_element.find_elements(By.TAG_NAME, "span")
            if span_elements:
                span_text = span_elements[0].text.strip()
                # (0.10)↑ 같은 변화량 제거
                return span_text.split('(')[0].strip() if '(' in span_text else span_text
            
            # span이 없으면 초기 배당과 동일
            text = td_element.text.strip()
            lines = text.split('\n')
            return lines[0].strip() if lines else ""
        except Exception:
            return ""
