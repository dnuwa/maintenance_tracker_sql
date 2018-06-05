from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from db import DBManager

app = Flask(__name__)
api= Api(app, prefix="/api/v1")

user_request_parser = RequestParser(bundle_errors=True)
user_request_parser.add_argument("email", type=str, required=True, help="Name has to be valid string")
user_request_parser.add_argument("password", required=True)

mainreq_request_parser = RequestParser(bundle_errors=True)
mainreq_request_parser.add_argument("item", type=str, required=True, help="item has to be valid string")
mainreq_request_parser.add_argument("issue", type=str, required=True, help="issue has to be valid string")
mainreq_request_parser.add_argument("issue_details", type=str, required=True, help="details must be a valid string")
mainreq_request_parser.add_argument("status", required=True)
mainreq_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")

class UserRegistration(Resource):
    def post(self):
        
        data = user_request_parser.parse_args()
        try:            
            return{
                'message':'User {} was created'.format(data['username'])
            }
        except:
            return {'message': 'something went wrong'}, 500
        
class UserLogin(Resource):
    def post(self):
        data = user_request_parser.parse_args()
        return data

class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'all users'}

class ManageRequests(Resource):
    
    def post(self):
        return {"msg": "Request added"}, 201
        
    def get(self):
        return {'message': 'All requests'}

class Manage(Resource):

    def put(self, id):
        return {'message':'request updated'} 

    def get(self, id):
        return {'message':'returns data to be eddited'}

