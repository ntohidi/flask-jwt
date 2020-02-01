from app import api, jwt
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('username', help='username cannot be blank', required=True)
parser.add_argument('password', help='password cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.check_for_conflict(args={'username': data['username']})
        if user.json['user']:
            return {'status': 409, 'message': 'username {} exists'.format(data['username'])}, 409

        new_user = UserModel({
            "username": data['username'],
            "password": UserModel.generate_hash(data['password'])
        })
        try:
            new_user.save()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'status': 200,
                'message': 'User created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as err:
            print(err.args)
            return {'status': 500, 'message': 'Something went horribly wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.get_one(args={'username': data['username']})
        if not user:
            return {'status': 404, 'message': 'username {} does not exist'.format(data['username'])}, 404

        if user.verify_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoke_token = RevokedTokenModel(jti=jti)
            revoke_token.save()
            return {'message': "Access token has benn revoked"}
        except Exception as err:
            print(err.args)
        return {'status': 500, 'message': 'Something went horribly wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoke_token = RevokedTokenModel(jti=jti)
            revoke_token.save()
            return {'message': "Refresh token has benn revoked"}
        except Exception as err:
            print(err.args)
        return {'status': 500, 'message': 'Something went horribly wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/secret')
