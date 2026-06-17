import unittest
from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_greeting_is_not_fallback(self):
        response = self.client.post('/ask', json={'message': 'hello there'})
        self.assertNotEqual(response.json['response'], "Sorry, I didn't understand.")

    def test_help_is_not_fallback(self):
        response = self.client.post('/ask', json={'message': 'I need help with my account'})
        self.assertNotEqual(response.json['response'], "Sorry, I didn't understand.")


if __name__ == '__main__':
    unittest.main()
