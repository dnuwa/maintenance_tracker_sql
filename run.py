from app.api import (AllUsers, AllRequests, Manage, ManageRequests, UserLogin,
                     UserRegistration, api, app)
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(ManageRequests, '/users/requests')
api.add_resource(AllRequests, '/requests')
api.add_resource(Manage, '/users/requests/<int:id>')


api.add_resource(AllUsers, '/users')


if __name__ == '__main__':
    app.run(debug=True)
