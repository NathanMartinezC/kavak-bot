from abc import ABC, abstractmethod
from fastapi import UploadFile

from src.core.entities import Car

class CarsDBRepository(ABC):
    @abstractmethod
    def initialize_stock(self, file: UploadFile) -> None:
        pass
    
    @abstractmethod
    def get_cars_by_filter(self, filter: str) -> list[Car]:
        pass
