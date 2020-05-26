import re

import coreapi
import coreschema
from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation, setup_user_email
from dj_rest_auth.utils import JWTCookieAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlunquote
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.core import signing
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.schemas import ManualSchema

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
from sonsuz_website.users.models import User
from sonsuz_website.blog.api.pagination import PageLimitOffset


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'news_id'
    pagination_class = PageLimitOffset

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'status')

    def create(self, request, **kwargs):
        # print(request.data)
        data = request.data
        data.update({'user': request.user.pk})

        if data['abstract'] == None:
            content = data['content']
            print(content)
            content = re.sub('!\[.*?\]\((.*?)\)', '', content)
            print(content)

            pattern = '[\\\`\*\_\[\]\#\+\-\!\>]'
            content = re.sub(pattern, '', content)
            print(content)

            abstract = content[0: 150]
            data.update({'abstract': abstract})

        serializer = ArticleSerializer(data=data)
        if not serializer.is_valid():
            return Response({'info': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serial.data)
        # return Response({'code': '200', 'message': 'OK'})

    def list(self, request, *args, **kwargs):

        if 'username' not in request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            username = request.query_params["username"]
            user = User.objects.get(username=username).pk
            instance = Article.objects.filter(user=user)
            queryset = self.filter_queryset(instance)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
