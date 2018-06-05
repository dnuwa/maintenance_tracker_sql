from app.api import*


api.add_resource(ManageRequests, '/user/request')
api.add_resource(Manage, '/user/request/<int:id>')
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
#api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')

if __name__ == '__main__':
    app.run(debug=True)