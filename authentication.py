import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from rest_framework import exceptions
from utils.response import APIResponse


class MyToken(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = str(request.META.get('HTTP_AUTHORIZATION'))
        if jwt_value is None:
            return APIResponse(code=0, msg='需要认证')

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('签名过期')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('令牌错误')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('无效令牌')

        user = self.authenticate_credentials(payload)

        return user, jwt_value
