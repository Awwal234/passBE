from flask_restx import Namespace, Resource, fields
from ..model.authmodel import User
from flask import request
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token

auth_namespace = Namespace(
    'auth', description='authenticate users')

auth_model = auth_namespace.model('Auth', {
    'id': fields.Integer(),
    'fullName': fields.String(required=True, unique=True, description='Full name'),
    'password': fields.String(required=True, unique=True, description='password'),
    'businessEmail': fields.String(required=True, unique=True, description='Business email'),
    'businessName': fields.String(required=True, unique=True, description='Business name'),
    'typeBusiness': fields.String(required=True, description='Business type'),
    'phoneNo': fields.String(required=True, unique=True, description='Business mobile'),
})

login_model = auth_namespace.model('Login', {
    'password': fields.String(required=True, description='password'),
    'businessEmail': fields.String(required=True, description='Business email')
})


@auth_namespace.route('/signup')
class CREATEUSER(Resource):
    @auth_namespace.expect(auth_model)
    @auth_namespace.marshal_with(auth_model)
    def post(self):
        '''
            Create new user
        '''
        data = request.get_json()
        fullName = data['fullName']
        password = data['password']
        businessEmail = data['businessEmail']
        businessName = data['businessName']
        typeBusiness = data['typeBusiness']
        phoneNo = data['phoneNo']

        new_user = User(fullName=fullName, businessEmail=businessEmail, password=password, businessName=businessName,
                        typeBusiness=typeBusiness, phoneNo=phoneNo)
        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class LOGINUSER(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        '''
            Login users
        '''
        data = request.get_json()
        password = data['password']
        businessEmail = data['businessEmail']

        user = User.query.filter_by(businessEmail=businessEmail).first()
        print(user)

        if (user is not None) and (user.password == password):
            access_token = create_access_token(identity=businessEmail)
            refresh_token = create_refresh_token(identity=businessEmail)
            response = {
                'access': access_token,
                'refresh': refresh_token,
                'user_email': user.businessEmail,
                'fullname': user.fullName
            }
            return response, HTTPStatus.ACCEPTED
        else:
            response = {
                'message': 'Invalid credentials',
            }
            return response, HTTPStatus.UNAUTHORIZED
