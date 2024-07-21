import requests
from typing import List, Dict, Any

class HeadHunterAPI:
    """
    Класс для взаимодействия с API HeadHunter.
    """

    BASE_URL: str = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Получает список вакансий с HeadHunter API по заданному запросу и области.
        :param search_query: Поисковый запрос для вакансий.
        :return: Список словарей с информацией о вакансиях.
        """
        params: Dict[str, Any] = {
            "text": search_query,
            "area": "2",  # 1 - для Москвы, 2 - для Питера
            "per_page": 20  # количество вакансий на странице
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()  # для выброса исключений в случае неудачи запроса
        return response.json().get('items', [])
