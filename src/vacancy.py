from typing import List, Dict, Optional, Any

class Vacancy:
    """
    Класс для представления вакансии.
    """

    def __init__(self, title: str, url: str, salary: str, description: Optional[str]):
        self.title = self.validate_title(title)
        self.url = self.validate_url(url)
        self.salary = self.validate_salary(salary)
        self.description = self.validate_description(description)

    @staticmethod
    def validate_title(title: str) -> str:
        if not title:
            raise ValueError("Title cannot be empty.")
        return title

    @staticmethod
    def validate_url(url: str) -> str:
        if not url.startswith("http"):
            raise ValueError("Invalid URL.")
        return url

    @staticmethod
    def validate_salary(salary: str) -> str:
        if not isinstance(salary, str):
            raise ValueError("Salary must be a string.")
        return salary

    @staticmethod
    def validate_description(description: Optional[str]) -> str:
        if description is None or not isinstance(description, str):
            return "Не указано"
        return description

    def __repr__(self) -> str:
        return f"Vacancy(title={self.title}, url={self.url}, salary={self.salary}, description={self.description})"

    def __eq__(self, other: 'Vacancy') -> bool:
        return self.salary == other.salary

    def __lt__(self, other: 'Vacancy') -> bool:
        return self.salary < other.salary

    @staticmethod
    def cast_to_object_list(vacancies: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Преобразует список словарей вакансий в список объектов Vacancy.

        :param vacancies: Список словарей вакансий.
        :return: Список объектов Vacancy.
        """
        def format_salary(salary: Optional[Dict[str, Any]]) -> str:
            if not salary:
                return "Не указана"
            from_value = salary.get("from")
            to_value = salary.get("to")
            currency = salary.get("currency", "")
            if from_value and to_value:
                return f"{from_value} - {to_value} {currency}"
            if from_value:
                return f"от {from_value} {currency}"
            if to_value:
                return f"до {to_value} {currency}"
            return "Не указана"

        return [
            Vacancy(
                title=vacancy["name"],
                url=vacancy["alternate_url"],
                salary=format_salary(vacancy.get("salary")),
                description=vacancy["snippet"].get("requirement", "Не указано")
            )
            for vacancy in vacancies
        ]
