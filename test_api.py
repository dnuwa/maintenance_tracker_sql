import json
import unittest

from app.api import (AllUsers, AllRequests, Manage, ManageRequests, UserLogin,
                     UserRegistration, api, app)
from flask_testing import TestCase
import run


class BaseTestCase(TestCase):
    def create_app(self):
        return app

class TestUserService(BaseTestCase):
    #Tests for the Users Service endpoints

    def test_access_all_requests(self):
        response = self.client.get('/api/v1/requests')
        #result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        #print(result)
        # self.assertIn('issue', result)
        

    def test_user_registers_successfuly(self):
        userdata = {'email':'daniel.nuwa@yahoo.com', 'password':'53423'}
        response = self.client.post('/api/v1/auth/signup',data = json.dumps(userdata), content_type='application/json',)
        print(response)
        self.assertEqual(response.status_code, 201) 

    # def test_user_login_successfuly(self):
    #     response = self.client.post('/api/v1/auth/login')
    #     self.assertEqual(response.status_code, 200)      

            
    def test_access_request_by_id(self):
        response = self.client.get('/api/v1/users/requests/1')
        self.assertEqual(response.status_code, 200) 

    def test_adding_user_request(self):
        requestData = {'item':'car','issue':'broken dash','issue_details':'radio not working', 'mode':'', 'standing':''} 
        response = self.client.post('/api/v1/users/requests', data = json.dumps(requestData), content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()