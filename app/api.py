from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from app.db import DatabaseManager, RequestsManager
import re


from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity)

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

user_request_parser = RequestParser(bundle_errors=True)
user_request_parser.add_argument(
    "email", type=str, required=True, help="Name has to be valid string")
user_request_parser.add_argument("password", required=True)

mainreq_request_parser = RequestParser(bundle_errors=True)
mainreq_request_parser.add_argument(
    "item", type=str, required=True, help="item has to be valid string")
mainreq_request_parser.add_argument(
    "issue", type=str, required=True, help="issue has to be valid string")
mainreq_request_parser.add_argument(
    "issue_details", type=str, required=True, help="details must be a valid string")
#state = mainreq_request_parser.add_argument("status", required=True)
mainreq_request_parser.add_argument(
    "mode", type=str, help="item has to be valid string")
mainreq_request_parser.add_argument(
    "standing", type=str, required=True, help="item has to be valid string")


class UserRegistration(Resource):
    def post(self):
        data = user_request_parser.parse_args()
        email = data['email']
        password = data['password']
        #password = generate_password_hash(data['password'], method="sha256")     
        if not email:
            return {'message': 'please enter email'}
        if not password:
            return {'message': 'enter a valid email'}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'message': 'Invalid email address'}


        db = DatabaseManager()
        db.create_table()
        db.insert_new_record(email, password)
        return {'message':'User {} was created'.format(data['email'])}, 201
       


class UserLogin(Resource):
    def post(self):
        data = user_request_parser.parse_args()
        email = data['email']
        password = data['password']
        user_login = DatabaseManager()
        result = user_login.login(email, password)
        return result, 200
               
        # access_token = create_access_token(identity=data['email'])
        # return {
        #     'message': 'Logged in as {}'.format(data['email']),
        #     'access_token': access_token
        # }


class AllUsers(Resource):
   # @jwt_required
    def get(self):
        db = DatabaseManager()
        return db.query_all()


class ManageRequests(Resource):
   # @jwt_required
    def post(self):
        data = mainreq_request_parser.parse_args()
        item = data['item']
        issue = data['issue']
        details = data['issue_details']
        mode = data['mode']
        db = RequestsManager()
        db.create_table()
        db.insert_new_record(item, issue, details, mode)
        return {'messege': 'successful!'}, 201


class AllRequests(Resource):
    #@jwt_required
    def get(self):
        db = RequestsManager()
        return db.query_all()


class Manage(Resource):
    #@jwt_required
    def put(self, id):
        data = mainreq_request_parser.parse_args()
        item = data['item']
        issue = data['issue']
        details = data['issue_details']
        mode = data['mode']
        standing =data['standing']
        db = RequestsManager()
        db.edit_a_record(id, item, issue, details, mode, standing,)
        return {'message': 'request updated'}

    def get(self, id):
        db = RequestsManager()
        return db.query_by_id(id), 200

