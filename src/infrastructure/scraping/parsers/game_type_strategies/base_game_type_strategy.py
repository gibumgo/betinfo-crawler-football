from abc import ABC, abstractmethod
from typing import Dict
from bs4 import Tag


class BaseGameTypeStrategy(ABC):
    @abstractmethod
    def matches(self, img_src: str) -> bool:
        pass
    
    @abstractmethod
    def identify_type_name(self) -> str:
        pass
    
    @abstractmethod
    def parse_result(self, td_element: Tag) -> Dict[str, str]:
        pass
