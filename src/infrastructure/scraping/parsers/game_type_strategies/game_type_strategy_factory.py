from typing import List
from .base_game_type_strategy import BaseGameTypeStrategy
from .normal_game_strategy import NormalGameStrategy
from .handicap_game_strategy import HandicapGameStrategy
from .under_over_game_strategy import UnderOverGameStrategy
from .sum_game_strategy import SumGameStrategy


class GameTypeStrategyFactory:
    _strategies: List[BaseGameTypeStrategy] = [
        NormalGameStrategy(),
        HandicapGameStrategy(),
        UnderOverGameStrategy(),
        SumGameStrategy(),
    ]
    
    _default_strategy = NormalGameStrategy()
    
    @classmethod
    def create_strategy(cls, img_src: str) -> BaseGameTypeStrategy:
        for strategy in cls._strategies:
            if strategy.matches(img_src):
                return strategy
        
        return cls._default_strategy
    
    @classmethod
    def register_strategy(cls, strategy: BaseGameTypeStrategy) -> None:
        if strategy not in cls._strategies:
            cls._strategies.append(strategy)
