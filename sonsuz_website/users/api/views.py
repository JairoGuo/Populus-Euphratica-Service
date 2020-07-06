from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, setup_user_email, user_email
from dj_rest_auth.registration.views import RegisterView as _RegisterView
from dj_rest_auth.utils import JWTCookieAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.views.generic import DetailView
from django.core import signing
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from django.conf import settings
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.app_settings import (JWTSerializer, TokenSerializer,
                                       create_token)

from allauth.account import app_settings as allauth_settings
from allauth.socialaccount import signals
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, EmailSerializer, UserFollowSerializer, UserFansSerializer
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account import app_settings

from ..models import UserFollow

User = get_user_model()

# RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [JWTCookieAuthentication]
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

    # def get_queryset(self, *args, **kwargs):
    #     return self.queryset.filter(id=self.request.user.id)


    def retrieve(self, request, *args, **kwargs):
        follow_instance = UserFollow.objects.filter(follow=request.user.pk, follow_to=self.get_object().pk)
        if follow_instance:
            is_follow = True
        else:
            is_follow = False

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data.update({'is_follow': is_follow})
        return Response(data)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})

        return Response(status=status.HTTP_200_OK, data=serializer.data)


    @action(detail=False, methods=["GET"])
    def login_status(self, request):
        if request.user.is_authenticated:
            s = {"status": True}
        else:
            s = {"status": False}

        return Response(status=status.HTTP_200_OK, data=s)


    @action(detail=False, methods=["GET"])
    def email_key(self, request):

        # EmailAddress.objects.create(user=request['user'], email=request['email'])
        # self.email_address = EmailAddress.objects.get(email=request['email'])
        # print(signing.dumps(
        #     obj=self.email_address.pk,
        #     salt=app_settings.SALT))

        return Response(status=status.HTTP_200_OK, data={"D": "OK"})


class  EmailViewSet(ModelViewSet):
    serializer_class = EmailSerializer
    queryset = EmailAddress.objects.all()
    lookup_field = 'user'


# class UserDetailViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = [SessionAuthentication]
#
#
#     @action(detail=False, methods=["GET"])
#     def me(self, request):
#         serializer = UserSerializer(request.user, context={"request": request})
#
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#
#     #
#     # @action(detail=False, methods=["GET"])
#     # def login_status(self, request):
#     #     if request.user.is_authenticated:
#     #         s = {"status": True}
#     #     else:
#     #         s = {"status": False}
#     #
#     #     return Response(status=status.HTTP_200_OK, data=s)
#     #
#     #
#     # @action(detail=False, methods=["GET"])
#     # def email_key(self, request):
#     #
#     #     # EmailAddress.objects.create(user=request['user'], email=request['email'])
#     #     # self.email_address = EmailAddress.objects.get(email=request['email'])
#     #     # print(signing.dumps(
#     #     #     obj=self.email_address.pk,
#     #     #     salt=app_settings.SALT))
#     #
#     #     return Response(status=status.HTTP_200_OK, data={"D": "OK"})


class UserFollowViewSet(ModelViewSet):
    serializer_class = UserFollowSerializer
    queryset = UserFollow.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('follow',)

    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_queryset().filter(follow=request.user.pk, follow_to=data['follow_to'])
        if instance:
            instance.delete()
            return Response(status=status.HTTP_200_OK, data={"is_follow": False})

        data.update({'follow': request.user.pk})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance1 = UserFollow.objects.filter(follow=request.user.pk, follow_to=data['follow_to'])
        instance2 = UserFollow.objects.filter(follow=data['follow_to'], follow_to=request.user.pk)
        mutual_follow = instance1.count() == instance2.count()
        return Response(data={"is_follow": True, 'mutual_follow': mutual_follow}, status=status.HTTP_201_CREATED,
                        headers=headers)


class UserFansView(ListModelMixin, GenericViewSet):
    serializer_class = UserFansSerializer
    queryset = UserFollow.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('follow_to',)


class RegisterView(_RegisterView):

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        self.get_key(request)
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_key(self, request):

        self.email_address = EmailAddress.objects.get(email=request.data['email'])
        print(signing.dumps(
            obj=self.email_address.pk,
            salt=app_settings.SALT))


