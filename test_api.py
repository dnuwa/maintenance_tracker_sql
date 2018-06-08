import json
import unittest


from flask_testing import TestCase
from run import *


class BaseTestCase(TestCase):
    def create_app(self):
        return app

class TestUserService(BaseTestCase):
    #Tests for the Users Service endpoints

    def test_access_all_requests(self):
        #Ensuring the routes behave in a correct way correctly.
        response = self.client.get('/api/v1/requests')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        #print(data)
        self.assertIn('issue', data)
        self.assertIn('issue_details', data)
        self.assertIn('item',data)

    def test_user_registers_successfuly(self):
        datax = {'email':'daniel.nuwa@yahoo.com', 'password':'53423'}
        response = self.client.post('/api/v1/auth/login',data = json.dumps(datax), content_type='application/json',)
        #print(response)
        self.assertEqual(response.status_code, 201)        

    def test_return_all_requests(self):
        response = self.client.get('/api/v1/user/request')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        #print(data)
        self.assertIn('item', data)
            
    def test_access_request_by_id(self):
        response = self.client.get('/api/v1/user/request/1')
        self.assertEqual(response.status_code, 200)  

if __name__ == '__main__':
    unittest.main()