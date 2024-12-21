from django.contrib.auth.backends import ModelBackend
from django.db.models import F, Q
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pub.models import ResourceClaim
from pub.serializers import UserResourceClaimSerializer
from utils.exceptions import CustomValidationError, ErrorSerializer

from .exceptions import PasswordNotMatch, UserDoesNotExist
from .models import User
from .serializers import (ChangePasswordSerializer, RegisterSerializer,
                          UserDetailSerializer, UserSerializer)

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request: Request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None


@extend_schema(
    operation_id='register',
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(UserDetailSerializer, description='注册成功'),
        400: OpenApiResponse(ErrorSerializer, description='参数错误'),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request):
    """
    注册用户。
    """
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        raise CustomValidationError(serializer.errors)

    serializer.save()

    response_serializer = UserDetailSerializer(serializer.instance)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='get_current_user',
        responses={
            200: OpenApiResponse(UserDetailSerializer, description='获取成功'),
            400: OpenApiResponse(ErrorSerializer, description='参数错误'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def get(self, request: Request):
        """
        获取当前登录用户信息。
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        operation_id='edit_user_profile',
        request=UserDetailSerializer,
        responses={
            200: OpenApiResponse(UserDetailSerializer, description='修改成功'),
            400: OpenApiResponse(ErrorSerializer, description='参数错误'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def patch(self, request: Request):
        """
        更新当前登录用户信息。
        """
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            raise CustomValidationError(serializer.errors)

        serializer.save()
        return Response(serializer.data)


@extend_schema(
    operation_id='get_user_by_id',
    responses={
        200: OpenApiResponse(UserSerializer, description='获取成功'),
        404: OpenApiResponse(ErrorSerializer, description='用户不存在'),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_id(request: Request, pk):
    """
    获取用户信息。
    """
    try:
        user = User.objects.get(pk=pk)
        user.view_count = F('view_count') + 1
        user.save(update_fields=['view_count'])
        user.refresh_from_db()
    except User.DoesNotExist:
        raise UserDoesNotExist()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@extend_schema(
    operation_id='change_password',
    request=ChangePasswordSerializer,
    responses={
        204: OpenApiResponse(description='修改成功'),
        400: OpenApiResponse(ErrorSerializer, description='参数错误'),
        401: OpenApiResponse(ErrorSerializer, description='未登录'),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request: Request):
    """
    修改密码。
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        raise CustomValidationError(serializer.errors)

    user: User = request.user
    if not user.check_password(serializer.data['old_password']):
        raise PasswordNotMatch()

    user.set_password(serializer.data['new_password'])
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    operation_id='upload_avatar',
    request={'multipart/form-data': {
        'type': 'object',
        'properties': {'avatar': {'type': 'string', 'format': 'binary'}}}},
    responses={
        200: OpenApiResponse(UserDetailSerializer, description='上传成功'),
        400: OpenApiResponse(ErrorSerializer, description='参数错误'),
        401: OpenApiResponse(ErrorSerializer, description='未登录'),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_avatar(request):
    """
    上传用户头像。
    """
    if 'avatar' not in request.FILES:
        raise CustomValidationError({'avatar': ['请选择要上传的图片。']})

    user = request.user
    user.avatar = request.FILES['avatar']
    user.save()

    serializer = UserDetailSerializer(user)
    return Response(serializer.data)


@extend_schema(
    operation_id='get_user_claims',
    responses={
        200: OpenApiResponse(
            response=UserResourceClaimSerializer(many=True),
            description='获取用户认领列表成功'
        ),
        404: OpenApiResponse(
            response=ErrorSerializer,
            description='用户不存在'
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_claims(request: Request, pk: int) -> Response:
    """
    获取用户的全部认领。
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise UserDoesNotExist()

    claims = ResourceClaim.objects.filter(user=user)
    serializer = UserResourceClaimSerializer(claims, many=True)
    return Response(serializer.data)
