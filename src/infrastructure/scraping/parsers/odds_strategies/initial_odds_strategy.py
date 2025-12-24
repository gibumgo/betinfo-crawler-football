# parser/odds_strategies/initial_odds_strategy.py

from selenium.webdriver.common.by import By
from .base_odds_strategy import BaseOddsStrategy


class InitialOddsStrategy(BaseOddsStrategy):
    """
    초기 배당 파싱 전략
    
    특징:
    - 첫 번째 줄의 배당 값을 추출
    
    구조 예시:
        2.06
        <span>2.16</span>(0.10)↑
        
    → 초기 배당: 2.06
    """
    
    def parse(self, td_element) -> str:
        """
        초기 배당 값을 파싱합니다.
        
        Args:
            td_element: 배당 정보가 포함된 td 요소
            
        Returns:
            초기 배당 값 (첫 번째 줄)
        """
        try:
            text = td_element.text.strip()
            lines = text.split('\n')
            
            # 첫 번째 줄이 초기 배당
            return lines[0].strip() if lines else ""
        except Exception:
            return ""
