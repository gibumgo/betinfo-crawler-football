# parser/odds_strategies/base_odds_strategy.py

from abc import ABC, abstractmethod


class BaseOddsStrategy(ABC):
    """
    배당 파싱 전략의 추상 기본 클래스
    
    책임:
    - td 요소에서 배당 값 추출
    
    원칙:
    - 단일 책임 원칙 (SRP): 배당 파싱만 담당
    - 개방-폐쇄 원칙 (OCP): 새로운 배당 파싱 방식 추가 시 확장 가능
    """
    
    @abstractmethod
    def parse(self, td_element) -> str:
        """
        td 요소에서 배당 값을 파싱합니다.
        
        Args:
            td_element: 배당 정보가 포함된 td 요소 (Selenium WebElement)
            
        Returns:
            파싱된 배당 값 (문자열)
        """
        pass
