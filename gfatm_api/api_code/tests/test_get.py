'''
    Author: Kyle Simpson
    Purpose: Basic tests of the API
'''

import unittest
from gfatm_api.api_code import api_core as api

class TestGet(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()

    def test_get_one_document(self):
        response = self.app.get('http://127.0.0.1:5000/api/v1/resources/program_docs?id=3')
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()