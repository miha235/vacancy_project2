from typing import List, Dict, Optional
from src.hh import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver

def user_interaction() -> None:
    """
    Взаимодействие с пользователем для поиска вакансий, их
    фильтрации и вывода результатов.
    """

    hh_api: HeadHunterAPI = HeadHunterAPI()
    json_saver: JSONSaver = JSONSaver()

    search_query: str = input("Введите поисковый запрос: ")
    hh_vacancies: List[Dict[str, Optional[str]]] = hh_api.get_vacancies(search_query)

    vacancies_list: List[Vacancy] = Vacancy.cast_to_object_list(hh_vacancies)
    vacancies_dict_list: List[Dict[str, Optional[str]]] = [vacancy.__dict__ for vacancy in vacancies_list]

    print(f"Найдено {len(vacancies_dict_list)} вакансий по запросу '{search_query}'")

    json_saver.add_vacancies(vacancies_dict_list)

    top_n: int = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words: List[str] = input("Введите ключевые слова для фильтрации вакансий: ").split()

    while True:
        salary_range: str = input("Введите диапазон зарплат (например, 100000-150000): ")
        if '-' in salary_range:
            try:
                min_salary, max_salary = map(int, salary_range.split('-'))
                break
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите диапазон зарплат в формате '100000-150000'.")
        else:
            print("Некорректный ввод. Пожалуйста, введите диапазон зарплат в формате '100000-150000'.")

    filtered_vacancies: List[Dict[str, Optional[str]]] = json_saver.get_vacancies(filter_words, top_n, salary_range)

    if not filtered_vacancies:
        print("Не найдено вакансий, соответствующих заданным фильтрам.")
    else:
        print("\nОтфильтрованные вакансии:")

        for vacancy in filtered_vacancies:
            print(f"Заголовок: {vacancy['title']}")
            description: Optional[str] = vacancy.get('description', '')
            if description:
                description = description.replace('<highlighttext>', '').replace('</highlighttext>', '')
            print(f"Описание: {description}")
            if vacancy.get('salary'):
                print(f"Зарплата: {vacancy['salary']}")
            print(f"URL: {vacancy['url']}")
            print()

if __name__ == "__main__":
    user_interaction()
