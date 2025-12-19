# parser/odds_strategies/__init__.py

"""
배당 파싱 전략 패키지

이 패키지는 전략 패턴을 사용하여 초기 배당과 현재 배당을 파싱합니다.

사용 예시:
    >>> from parser.odds_strategies import InitialOddsStrategy, CurrentOddsStrategy
    >>> 
    >>> initial_strategy = InitialOddsStrategy()
    >>> current_strategy = CurrentOddsStrategy()
    >>> 
    >>> init_odds = initial_strategy.parse(td_element)
    >>> current_odds = current_strategy.parse(td_element)
"""

from .base_odds_strategy import BaseOddsStrategy
from .initial_odds_strategy import InitialOddsStrategy
from .current_odds_strategy import CurrentOddsStrategy

__all__ = [
    "BaseOddsStrategy",
    "InitialOddsStrategy",
    "CurrentOddsStrategy",
]
