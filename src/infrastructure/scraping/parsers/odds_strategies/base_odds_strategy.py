from abc import ABC, abstractmethod


class BaseOddsStrategy(ABC):
    @abstractmethod
    def parse(self, td_element) -> str:
        pass
