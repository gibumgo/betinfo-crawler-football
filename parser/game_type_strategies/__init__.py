# parser/game_type_strategies/__init__.py

"""
경기 유형별 파싱 전략 패키지

이 패키지는 전략 패턴을 사용하여 경기 유형별로 다른 파싱 로직을 제공합니다.

사용 예시:
    >>> from parser.game_type_strategies import GameTypeStrategyFactory
    >>> 
    >>> img_src = "../images/_button/ico_handicap.gif"
    >>> strategy = GameTypeStrategyFactory.get_strategy(img_src)
    >>> 
    >>> game_type = strategy.get_type_name()  # "핸디캡"
    >>> result_data = strategy.parse_result(td_element)
"""

from .base_game_type_strategy import BaseGameTypeStrategy
from .normal_game_strategy import NormalGameStrategy
from .handicap_game_strategy import HandicapGameStrategy
from .under_over_game_strategy import UnderOverGameStrategy
from .sum_game_strategy import SumGameStrategy
from .game_type_strategy_factory import GameTypeStrategyFactory

__all__ = [
    "BaseGameTypeStrategy",
    "NormalGameStrategy",
    "HandicapGameStrategy",
    "UnderOverGameStrategy",
    "SumGameStrategy",
    "GameTypeStrategyFactory",
]
