import unittest
from unittest.mock import patch
from src.hh import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch('src.hh.requests.get')
    def test_get_vacancies(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'items': [
            {'name': 'Test', 'alternate_url': 'http://example.com', 'salary': {},
             'snippet': {'requirement': 'Test requirement'}}]}

        api = HeadHunterAPI()
        result = api.get_vacancies("Python")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test')


if __name__ == '__main__':
    unittest.main()
