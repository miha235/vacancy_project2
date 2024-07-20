from typing import List, Optional, Dict, Any

class Vacancy:
    """
    Класс для представления вакансии.
    """
    def __init__(self, title: str, url: str, salary: str, description: str) -> None:
        self.title: str = title
        self.url: str = url
        self.salary: str = salary
        self.description: str = description

    def __repr__(self) -> str:
        return f"Vacancy(title={self.title}, url={self.url}, salary={self.salary}, description={self.description})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return False

    @staticmethod
    def cast_to_object_list(vacancies: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Преобразует список словарей вакансий в список объектов Vacancy.
        """
        def format_salary(salary: Optional[Dict[str, Optional[str]]]) -> str:
            if not salary:
                return "Не указана"
            from_value: Optional[str] = salary.get("from")
            to_value: Optional[str] = salary.get("to")
            currency: str = salary.get("currency", "")
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
