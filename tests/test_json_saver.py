import unittest
import json
from src.json_saver import JSONSaver


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        self.json_saver = JSONSaver(filename='test_vacancies.json')

    def tearDown(self):
        import os
        os.remove('test_vacancies.json')

    def test_add_vacancies(self):
        vacancies = [{'title': 'Test'}]
        self.json_saver.add_vacancies(vacancies)

        with open('test_vacancies.json', 'r') as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test')

    def test_get_vacancies(self):
        vacancies = [
            {
                "title": "Test",
                "salary": {"from": 1000, "to": 2000, "currency": "RUB"},
                "description": "Test requirement"
            }
        ]
        self.json_saver.add_vacancies(vacancies)
        result = self.json_saver.get_vacancies()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test')


if __name__ == '__main__':
    unittest.main()
