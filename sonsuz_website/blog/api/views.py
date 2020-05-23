from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, setup_user_email
from dj_rest_auth.utils import JWTCookieAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlunquote
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.core import signing
from config.settings.base import APPS_DIR
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action, api_view, parser_classes, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from rest_framework import mixins
from sonsuz_website.blog.api.serializers import ArticleSerializer
from sonsuz_website.blog.models import Article


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'news_id'

    def create(self, request):

        data = request.data
        data.update({'user': request.user.pk})
        serializer = ArticleSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serial.data)
        # return Response({'code': '200', 'message': 'OK'})

