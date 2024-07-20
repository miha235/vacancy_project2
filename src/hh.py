import requests
from typing import List, Dict

class HeadHunterAPI:
    """
    Класс для взаимодействия с API HeadHunter.
    """

    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str):
        """
        Получает список вакансий с HeadHunter API по заданному запросу и области.
        """
        params = {
            "text": search_query,
            "area": "2",  # 1 - для Москвы #  - для Питера
            "per_page": 20  # количество вакансий на странице
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()  # для выброса исключений в случае неудачи запроса
        return response.json().get('items', [])
