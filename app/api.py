from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from app.db import DatabaseManager, RequestsManager
import re
from werkzeug.security import generate_password_hash, check_password_hash


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
mainreq_request_parser.add_argument(
    "mode", type=str, help="item has to be valid string")
mainreq_request_parser.add_argument(
    "standing", type=str, required=True, help="item has to be valid string")


class UserRegistration(Resource):
    def post(self):
        data = user_request_parser.parse_args()
        email = data['email']
        password = data['password']
        hashed_password = generate_password_hash(password, method="sha256")
        if not email:
            return {'message': 'please enter email'}
        if not password:
            return {'message': 'enter a valid password'}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'message': 'Invalid email address'}

        db = DatabaseManager()
        db.create_table()
        #querydb = db.login(email, password)
        querydb = db.should_be_unique(email)
        if (querydb == None):
            db.insert_new_record(email, hashed_password)
            return {'message': 'User {} was created'.format(data['email'])}, 201
        else:
            return {'message': 'User {} already exists'.format(data['email'])}, 400


class UserLogin(Resource):
    def post(self):        
                      
        try:
            data = user_request_parser.parse_args()
            email = data['email']
            password = data['password']
            userobj = DatabaseManager()
            result =userobj.should_be_unique(email) 

            if (result['email']==email and check_password_hash(result['password'], password)):
                #result =userobj.should_be_unique(email)
                access_token = create_access_token(identity=result['id'])
                return {
                    'message': 'Logged in as {}'.format(result['email']),
                    'access_token': access_token
                }
                #return result, 200
            else:
                return {'message':'you have entered a wrong password'}, 201
        except:
            return {'message':'Login failed.. Ensure that your Email is correct'}, 400

class AllUsers(Resource):
    @jwt_required
    def get(self):
        db = DatabaseManager()
        return db.query_all()


class ManageRequests(Resource):
    @jwt_required
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
    @jwt_required
    def get(self):
        db = RequestsManager()
        return db.query_all()


class Manage(Resource):
    @jwt_required
    def put(self, id):
        data = mainreq_request_parser.parse_args()
        item = data['item']
        issue = data['issue']
        details = data['issue_details']
        mode = data['mode']
        standing = data['standing']
        db = RequestsManager()
        to_be_edited = db.query_by_id(id)

        if(to_be_edited != None):
            if to_be_edited['standing'] != None and to_be_edited['standing'] != "":
                return {'Message': 'Record cant be editted'}
            else:
                db.edit_a_record(id, item, issue, details, mode, standing)
                record = db.query_by_id(id)
                return {'Update': record}, 201

        else:
            return {"message": "request id is out of range"}, 500

    @jwt_required
    def get(self, id):
        db = RequestsManager()
        id_In_range = db.query_by_id(id)
        if (id_In_range != None):
            return db.query_by_id(id), 200
        else:
            return {"message": "request id is out of range"}, 500


class AdminDisapprove(Resource):
    @jwt_required
    def put(self, id):
        db = RequestsManager()
        to_be_disapproved = db.query_by_id(id)

        if(to_be_disapproved != None):
            if to_be_disapproved['mode'] != None and to_be_disapproved['mode'] != "":

                if to_be_disapproved['mode'] == 'Approved':
                    return {'message': 'This request was Approved'}

                else:
                    return {'message': 'This request was Disapproved'}

            else:
                to_be_disapproved['mode'] = 'Disapproved'
                new_value = to_be_disapproved['mode']
                db.disapprove_or_approve(id, new_value)
                record = db.query_by_id(id)
                return {'Update': record}, 201

        else:
            return {"message": "request doesnt exist"}, 500


class AdminApproval(Resource):
    @jwt_required
    def put(self, id):
        db = RequestsManager()
        to_be_approved = db.query_by_id(id)

        if(to_be_approved != None):
            if (to_be_approved['mode'] != None and to_be_approved['mode'] != ""):
                if to_be_approved['mode'] == 'Approved':
                    return {'message': 'This request was Approved'}

                else:
                    return {'message': 'This request was Disapproved'}
            else:
                to_be_approved['mode'] = 'Approved'
                new_value = to_be_approved['mode']
                db.disapprove_or_approve(id, new_value)
                record = db.query_by_id(id)
                return {'Update': record}, 201

        else:
            return {"message": "request doesnt exist"}, 500


class AdminResolve(Resource):
    @jwt_required
    def put(self, id):
        db = RequestsManager()
        to_be_resolved = db.query_by_id(id)

        if(to_be_resolved != None):
            if (to_be_resolved['standing'] !='Resolved'):
                if to_be_resolved['mode'] == 'Approved':

                    to_be_resolved['standing'] = 'Resolved'
                    new_value = to_be_resolved['standing']
                    db.resolve_request(id, new_value)
                    record = db.query_by_id(id)
                    return {'Update': record}, 201

                elif to_be_resolved['mode'] == 'Disapproved':
                    return {'Message': 'This request was Disapproved'}, 200

                elif to_be_resolved['mode'] == None and to_be_resolved['mode'] == "":
                    return {'Message': 'This request is pending'}, 200

                else:
                    return {'Message': 'This request is pending'}, 200

            else:
                return {'Message': 'This request was Resolved'}, 200

        else:
            return {"message": "request doesnt exist"}, 500
