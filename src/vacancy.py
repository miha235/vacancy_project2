from typing import List, Optional

class Vacancy:
    """
    Класс для представления вакансии.
    """
    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def __repr__(self):
        return f"Vacancy(title={self.title}, url={self.url}, salary={self.salary}, description={self.description})"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    @staticmethod
    def cast_to_object_list(vacancies: List[dict]):
        """
        Преобразует список словарей вакансий в список объектов Vacancy.
        """
        def format_salary(salary):
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
