from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class VacancySaver(ABC):
    """
    Абстрактный базовый класс для сохранения и получения вакансий.
    """

    @abstractmethod
    def add_vacancies(self, vacancies: List[Dict[str, str]]) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, filter_words: Optional[List[str]] = None, top_n: Optional[int] = None, salary_range: Optional[str] = None) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def remove_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> None:
        pass