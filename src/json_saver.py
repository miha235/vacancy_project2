import json
import re
from typing import List, Dict, Any, Tuple, Optional

class JSONSaver:
    """
    Класс для сохранения и получения вакансий в формате JSON.
    """

    def __init__(self, filename: str = 'data/vacancies.json'):
        self.filename = filename

    def add_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Добавляет список вакансий в JSON-файл.

        :param vacancies: Список вакансий.
        """
        self.validate_vacancies(vacancies)

        for vacancy in vacancies:
            vacancy['description'] = self.remove_highlight_tags(vacancy['description'])

        with open(self.filename, 'w') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    @staticmethod
    def remove_highlight_tags(text: Optional[str]) -> str:
        if text is None:
            return ""
        return text.replace('<highlighttext>', '').replace('</highlighttext>', '')

    @staticmethod
    def validate_vacancies(vacancies: List[Dict[str, Any]]) -> None:
        if not isinstance(vacancies, list):
            raise ValueError("Vacancies must be a list.")
        for vacancy in vacancies:
            if not isinstance(vacancy, dict):
                raise ValueError("Each vacancy must be a dictionary.")

    def parse_salary(self, salary_str: str) -> Tuple[Optional[int], Optional[int]]:
        if not isinstance(salary_str, str):
            raise ValueError("Salary must be a string.")
        match = re.search(r"(\d+)\s*-\s*(\d+)", salary_str)
        if match:
            return int(match.group(1)), int(match.group(2))

        match = re.search(r"от\s*(\d+)", salary_str)
        if match:
            return int(match.group(1)), None

        match = re.search(r"до\s*(\d+)", salary_str)
        if match:
            return None, int(match.group(1))

        return None, None

    def check_salary(self, salary: Any, min_salary: int, max_salary: int) -> bool:
        if isinstance(salary, str):
            from_salary, to_salary = self.parse_salary(salary)
            if from_salary and to_salary:
                return (min_salary <= from_salary <= max_salary) or (min_salary <= to_salary <= max_salary)
            elif from_salary:
                return min_salary <= from_salary <= max_salary
            elif to_salary:
                return min_salary <= to_salary <= max_salary
        elif isinstance(salary, dict):
            from_salary = salary.get('from', 0)
            to_salary = salary.get('to', 0)
            return (from_salary and min_salary <= from_salary <= max_salary) or (to_salary and min_salary <= to_salary <= max_salary)
        return False

    def get_vacancies(self, filter_words: Optional[List[str]] = None, top_n: Optional[int] = None, salary_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получает список вакансий из JSON-файла, фильтрует их и возвращает результат.

        :param filter_words: Список ключевых слов для фильтрации вакансий.
        :param top_n: Количество вакансий для вывода в топ N.
        :param salary_range: Диапазон зарплат для фильтрации вакансий.
        :return: Отфильтрованный список вакансий.
        """
        try:
            with open(self.filename, 'r') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            vacancies = []

        if filter_words:
            vacancies = [v for v in vacancies if v.get('description') and all(word in v['description'] for word in filter_words)]

        if salary_range:
            min_salary, max_salary = map(int, salary_range.split('-'))
            vacancies = [v for v in vacancies if self.check_salary(v.get('salary'), min_salary, max_salary)]

        if top_n:
            def get_salary(v: Dict[str, Any]) -> int:
                salary = v.get('salary')
                if isinstance(salary, str):
                    from_salary, to_salary = self.parse_salary(salary)
                    return from_salary or to_salary or 0
                elif isinstance(salary, dict):
                    return salary.get('from', 0) or salary.get('to', 0)
                return 0

            vacancies = sorted(vacancies, key=get_salary, reverse=True)[:top_n]

        return vacancies
