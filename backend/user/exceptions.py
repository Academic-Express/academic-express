from rest_framework import status
from rest_framework.exceptions import APIException


class UserDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '用户不存在。'
    default_code = 'user_does_not_exist'


class PasswordNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '密码错误。'
    default_code = 'password_not_match'
