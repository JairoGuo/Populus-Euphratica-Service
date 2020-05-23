from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, setup_user_email
from dj_rest_auth.utils import JWTCookieAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core import signing

from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, EmailSerializer
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account import app_settings
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


