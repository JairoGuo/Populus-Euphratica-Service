import allauth
from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email, send_email_confirmation
from django.core import signing
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from taggit import managers
from sonsuz_website.blog.models import Article, Comment, Like
from taggit.models import Tag
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog_id']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'




class ArticleSerializer(TaggitSerializer, ModelSerializer):

    blog_like = LikeSerializer(many=True, required=False)
    blog_comment = CommentSerializer(many=True, required=False)
    # blog_tags = TagSerializer(many=True, required=False)
    tags = TagListSerializerField(required=False)
    class Meta:
        model = Article
        fields = '__all__'

    # def create(self, request):
    #     data = dict(request)
    #     if 'abstract' not in dict(request):
    #         abstract = data['content'][0: 100]
    #         data.update({'abstract': abstract})
    #     instance = Article.objects.create(**data)
    #
    #     return instance




