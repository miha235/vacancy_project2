import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_cast_to_object_list(self):
        vacancies = [
            {
                "name": "Test",
                "alternate_url": "http://example.com",
                "salary": {"from": 1000, "to": 2000, "currency": "RUB"},
                "snippet": {"requirement": "Test requirement"}
            }
        ]
        result = Vacancy.cast_to_object_list(vacancies)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Vacancy)
        self.assertEqual(result[0].title, "Test")
        self.assertEqual(result[0].salary, "1000 - 2000 RUB")


if __name__ == '__main__':
    unittest.main()
