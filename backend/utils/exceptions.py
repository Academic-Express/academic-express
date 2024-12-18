from django.conf import settings
from rest_framework import serializers, status
from rest_framework.exceptions import (APIException, ErrorDetail,
                                       ValidationError)
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '参数错误。'
    default_code = 'validation_error'

    def __init__(self, errors: dict, detail=None, code=None):
        for value in errors.values():
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, ErrorDetail):
                        value[i] = {
                            'detail': str(item),
                            'code': item.code,
                        }
                    else:
                        value[i] = {
                            'detail': str(item),
                            'code': 'invalid',
                        }

        super().__init__({
            'detail': detail or self.default_detail,
            'code': code or self.default_code,
            'fields': errors,
        })


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    fields = serializers.DictField(required=False)


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = CustomValidationError(exc.detail)

    response = exception_handler(exc, context)

    if response is None and not settings.DEBUG:
        import traceback
        traceback.print_exc()

        response = Response({
            'detail': '未知错误。',
            'code': 'error',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response is not None:
        response.data['status_code'] = response.status_code

        if 'code' not in response.data:
            if isinstance(exc, APIException) and isinstance(exc.detail, ErrorDetail):
                response.data['code'] = exc.detail.code or 'error'
            else:
                response.data['code'] = 'error'

    return response
