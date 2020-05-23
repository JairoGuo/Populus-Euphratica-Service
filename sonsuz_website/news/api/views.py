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
from sonsuz_website.news.api.serializers import NewsSerializer, NewsImageSerializer
from sonsuz_website.news.models import News, NewsImage


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    # lookup_field = 'news_id'

    def create(self, request):

        data = request.data
        data.update({'user': request.user.pk})
        serializer = NewsSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'code': '200'})


class NewsImageViewSet(ModelViewSet):
    serializer_class = NewsImageSerializer
    queryset = NewsImage.objects.all()

    def create(self, request, *args, **kwargs):

        # if request.data  == {}:
        #     return Response(data={"data": "null"})
        self.serializer_class = NewsImageSerializer
        rlt_data =[]
        for i in request.data:

            data = {
                "image": request.data[i],
            }
            serial = NewsImageSerializer(data=data)
            if not serial.is_valid():
                return Response(serial.data, status=status.HTTP_400_BAD_REQUEST)

            serial.save()
            rlt_data.append([eval(i), 'http://localhost:8000' + serial.data['image']])

        return Response({'code': '200', 'data': rlt_data})
        # return Response(serial.data)
        # return Response({'code': '200', 'message': 'OK'})


@api_view(['POST'])
@csrf_exempt
@parser_classes((MultiPartParser,))#参数类型
# @authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def upload_file(request):
    for i in request.data:
        print(i)
    print(request.data)
    print(request.FILES.getlist('file'))



    return Response({'code': '200', 'message': 'OK'})
