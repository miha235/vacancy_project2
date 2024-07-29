from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VacancyAPI(ABC):
    """
    Абстрактный базовый класс для работы с API вакансий.
    """

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получает список вакансий по заданному запросу.

        :param search_query: Поисковый запрос для вакансий.
        :return: Список вакансий.
        """
        pass
