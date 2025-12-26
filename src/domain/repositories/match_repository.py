from abc import ABC, abstractmethod
from typing import List
from domain.models.match import Match

class MatchRepository(ABC):
    @abstractmethod
    def save(self, filename: str, matches: List[Match]) -> None:
        pass
