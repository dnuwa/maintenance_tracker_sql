from app.api import (AllUsers, AllRequests, Manage, ManageRequests, UserLogin,
                     UserRegistration, api, app, AdminApproval, AdminDisapprove, AdminResolve)
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(UserRegistration, '/auth/signup')  # user registration
api.add_resource(UserLogin, '/auth/login')  # user login
api.add_resource(ManageRequests, '/users/requests')  # creating a request
api.add_resource(AllRequests, '/requests')  # view all requests
# put and get for a single record
api.add_resource(Manage, '/users/requests/<int:id>')
# approve a request
api.add_resource(AdminApproval, '/requests/<int:id>/approve')
# disapprove a request
api.add_resource(AdminDisapprove, '/requests/<int:id>/disapprove')
# resolve approved requests
api.add_resource(AdminResolve, '/requests/<int:id>/resolve')


api.add_resource(AllUsers, '/users')


if __name__ == '__main__':
    app.run(debug=True)
