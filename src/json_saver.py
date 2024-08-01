import json
import re
from typing import List, Optional, Dict, Any
from src.vacancy_saver_api import VacancySaver

class JSONSaver(VacancySaver):
    """
    Класс для сохранения и получения вакансий в формате JSON.
    """

    def __init__(self, filename: str = 'data/vacancies.json'):
        self._filename = filename # Приватный атрибут

    def add_vacancies(self, vacancies: List[Dict[str, str]]) -> None:
        """
        Добавляет список вакансий в JSON-файл.
        """
        with open(self._filename, 'w') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def remove_highlight_tags(self, text: str) -> str:
        """
        Удаляет теги <highlighttext> из строки.
        """
        if text is None:
            return ""
        return text.replace('<highlighttext>', '').replace('</highlighttext>', '')

    def parse_salary(self, salary_str: str) -> Optional[tuple[int, int]]:
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

    def check_salary(self, salary: str, min_salary: int, max_salary: int) -> bool:
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

    def get_vacancies(self, filter_words: Optional[List[str]] = None, top_n: Optional[int] = None, salary_range: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Получает список вакансий из JSON-файла, фильтрует их и возвращает результат.
        """
        try:
            with open(self._filename, 'r') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            vacancies = []

        if filter_words:
            vacancies = [v for v in vacancies if v.get('description') and all(word in v['description'] for word in filter_words)]

        if salary_range:
            min_salary, max_salary = map(int, salary_range.split('-'))
            vacancies = [v for v in vacancies if self.check_salary(v.get('salary'), min_salary, max_salary)]

        if top_n:
            def get_salary(v):
                salary = v.get('salary')
                if isinstance(salary, str):
                    from_salary, to_salary = self.parse_salary(salary)
                    return from_salary or to_salary or 0
                elif isinstance(salary, dict):
                    return salary.get('from', 0) or salary.get('to', 0)
                return 0

            vacancies = sorted(vacancies, key=get_salary, reverse=True)[:top_n]

        return vacancies

    def remove_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> None:
        """
        Удаляет вакансии из JSON-файла на основе заданных критериев.
        Если критерии не заданы, удаляет все вакансии.
        """
        try:
            with open(self._filename, 'r') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            return

        if criteria:
            filtered_vacancies = []
            for vacancy in vacancies:
                match = True
                for key, value in criteria.items():
                    if vacancy.get(key) != value:
                        match = False
                        break
                if not match:
                    filtered_vacancies.append(vacancy)
            with open(self._filename, 'w') as file:
                json.dump(filtered_vacancies, file, ensure_ascii=False, indent=4)
        else:
            open(self._filename, 'w').close()

    def get_filename(self) -> str:
        """
        Возвращает имя файла.
        """
        return self._filename

    def set_filename(self, filename: str) -> None:
        """
        Устанавливает новое имя файла.
        """
        self._filename = filename