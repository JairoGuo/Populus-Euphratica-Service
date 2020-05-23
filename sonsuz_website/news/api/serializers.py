import allauth
from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email, send_email_confirmation
from django.core import signing
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from taggit import managers
from sonsuz_website.news.models import News, Comment, Like, NewsImage
from taggit.models import Tag




class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'news']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class NewsSerializer(ModelSerializer):

    like = LikeSerializer(many=True, required=False)
    comment = CommentSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = '__all__'


    def create(self, request):
        data = dict(request)
        abstract = data['content'][0: 75]
        if 'abstract' not in dict(request):
            data.update({'abstract': abstract})
        News.objects.create(**data)

        return request


class NewsImageSerializer(ModelSerializer):
    class Meta:
        model = NewsImage
        fields = '__all__'



