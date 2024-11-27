from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions import CustomValidationError, ErrorSerializer

from .models import ScholarSubscription, TopicSubscription
from .serializers import (ScholarSubscriptionSerializer,
                          TopicSubscriptionSerializer)


class TopicSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='get_topic_subscriptions',
        responses={
            200: OpenApiResponse(
                TopicSubscriptionSerializer(many=True),
                description='获取话题订阅成功',
            ),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def get(self, request: Request):
        """
        获取用户订阅的所有话题。
        """
        user = request.user
        subscriptions = TopicSubscription.objects.filter(subscriber=user)
        serializer = TopicSubscriptionSerializer(subscriptions, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        operation_id='subscribe_topic',
        request=TopicSubscriptionSerializer,
        responses={
            201: OpenApiResponse(TopicSubscriptionSerializer, description='订阅话题成功'),
            400: OpenApiResponse(ErrorSerializer, description='参数错误'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def post(self, request: Request):
        """
        订阅话题。
        """
        serializer = TopicSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomValidationError(serializer.errors)

        topic = serializer.validated_data['topic']
        subscription, _ = TopicSubscription.objects.get_or_create(
            subscriber=request.user,
            topic=topic,
        )

        serializer = TopicSubscriptionSerializer(subscription)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TopicSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='unsubscribe_topic',
        responses={
            204: OpenApiResponse(None, description='取消订阅话题成功'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
            404: OpenApiResponse(ErrorSerializer, description='未找到该订阅'),
        },
    )
    def delete(self, request: Request, pk: int):
        """
        取消订阅话题。
        """
        subscription = TopicSubscription.objects.filter(
            subscriber=request.user,
            id=pk,
        ).first()
        if subscription is None:
            raise NotFound('未找到该订阅。')

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScholarSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='get_scholar_subscriptions',
        responses={
            200: OpenApiResponse(
                ScholarSubscriptionSerializer(many=True),
                description='获取学者订阅成功',
            ),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def get(self, request: Request):
        """
        获取用户订阅的所有学者。
        """
        user = request.user
        subscriptions = ScholarSubscription.objects.filter(subscriber=user)
        serializer = ScholarSubscriptionSerializer(subscriptions, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        operation_id='subscribe_scholar',
        request=ScholarSubscriptionSerializer,
        responses={
            201: OpenApiResponse(ScholarSubscriptionSerializer, description='订阅学者成功'),
            400: OpenApiResponse(ErrorSerializer, description='参数错误'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
        },
    )
    def post(self, request: Request):
        """
        订阅学者。
        """
        serializer = ScholarSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomValidationError(serializer.errors)

        scholar_name = serializer.validated_data['scholar_name']
        subscription, _ = ScholarSubscription.objects.get_or_create(
            subscriber=request.user,
            scholar_name=scholar_name,
        )

        serializer = ScholarSubscriptionSerializer(subscription)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ScholarSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='unsubscribe_scholar',
        responses={
            204: OpenApiResponse(None, description='取消订阅学者成功'),
            401: OpenApiResponse(ErrorSerializer, description='未登录'),
            404: OpenApiResponse(ErrorSerializer, description='未找到该订阅'),
        },
    )
    def delete(self, request: Request, pk: int):
        """
        取消订阅学者。
        """
        subscription = ScholarSubscription.objects.filter(
            subscriber=request.user,
            id=pk,
        ).first()
        if subscription is None:
            raise NotFound('未找到该订阅。')

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
