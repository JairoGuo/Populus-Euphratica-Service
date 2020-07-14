import allauth
from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email, send_email_confirmation
from django.core import signing
from django.db.models.aggregates import Count
from django_redis import get_redis_connection

from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from taggit import managers
from sonsuz_website.blog.models import Article, Comment, Like, ArticleCategory, Collect, CollectCategory, CategoryFollow
from taggit.models import Tag
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog_id']



class CommentListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(reply_comment=None)
        return super(CommentListSerializer, self).to_representation(data)


class ReplyCommentSerializer(ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username', required=False)
    avatar = serializers.ImageField(source='user.avatar', required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    replies = ReplyCommentSerializer(read_only=True, many=True)
    username = serializers.ReadOnlyField(source='user.username', required=False)
    avatar = serializers.ImageField(source='user.avatar', required=False)

    class Meta:
        model = Comment
        list_serializer_class = CommentListSerializer

        fields = '__all__'


class ArticleSerializer(TaggitSerializer, ModelSerializer):

    # likes = LikeSerializer(many=True, required=False)
    tags = TagListSerializerField(required=False)
    username = serializers.ReadOnlyField(source='user.username', required=False)
    avatar = serializers.ImageField(source='user.avatar', required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class CollectSerializer(ModelSerializer):

    class Meta:
        model = Collect
        fields = '__all__'

    title = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.article.title

    def get_cover(self, obj):
        return obj.article.cover

    def get_created_at(self, obj):
        return obj.article.created_at

    def get_abstract(self, obj):
        return obj.article.abstract



class ArticleViewSerializer(TaggitSerializer, ModelSerializer):

    # likes = LikeSerializer(many=True, required=False)
    tags = TagListSerializerField(required=False)
    username = serializers.ReadOnlyField(source='user.username', required=False)
    avatar = serializers.ImageField(source='user.avatar', required=False)
    comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = Article
        # fields = '__all__'
        # fields = ['title', 'content', 'abstract', 'cover', 'status', 'category', 'tags', 'type', 'original_url']
        exclude = ['user',]

    comment_num = serializers.SerializerMethodField()
    like_num = serializers.SerializerMethodField()
    collect_num = serializers.SerializerMethodField()

    def get_comment_num(self, obj):
        return obj.comments.count()

    def get_like_num(self, obj):
        return obj.likes.count()

    def get_collect_num(self, obj):
        return obj.collect_article.count()



class ArticleListSerializer(ModelSerializer):


    username = serializers.ReadOnlyField(source='user.username', required=False)
    avatar = serializers.ImageField(source='user.avatar', required=False)
    # comments = CommentSerializer(many=True, read_only=True)
    comment_num = serializers.SerializerMethodField()
    like_num = serializers.SerializerMethodField()
    click_num = serializers.SerializerMethodField()


    class Meta:
        model = Article
        # fields = '__all__'
        # fields = ['article_id', 'abstract', 'cover', 'status', 'click_nums', 'created_at']
        exclude = ['content', 'original_url', 'updated_at', 'user']

    def get_comment_num(self, obj):
        return obj.comments.count()

    def get_like_num(self, obj):
        return obj.likes.count()

    def get_click_num(self, obj):
        con = get_redis_connection()
        click_nums = obj.click_nums
        visited_args = ("blog:visited:list", "article.id:{id}:num".format_map({'id': str(obj.article_id)}))

        if con.hget(*visited_args):

            click_nums += int(con.hget(*visited_args))
        return click_nums


class CategorySerializer(ModelSerializer):
    # articles = ArticleListSerializer(many=True)

    class Meta:
        model = ArticleCategory
        fields = ['id', 'name', 'summary', 'user', 'article_num', 'category_follow_num']  # 'articles'

    article_num = serializers.SerializerMethodField()
    category_follow_num = serializers.SerializerMethodField()

    def get_article_num(self, obj):

        return obj.articles.count()

    def get_category_follow_num(self, obj):
        return obj.category_follow.count()


class CollectCategorySerializer(ModelSerializer):
    # collect = CollectSerializer(many=True, required=False)

    class Meta:
        model = CollectCategory
        fields = '__all__'
        # fields = ['id', 'name', 'user', 'description', 'collect']
    #
    collect_num = serializers.SerializerMethodField()

    def get_collect_num(self, obj):

        return obj.collect.count()


class CategoryFollowSerializer(ModelSerializer):
    category_info = CategorySerializer(many=True, required=False)

    class Meta:
        model = CategoryFollow
        fields = '__all__'
    category_name = serializers.SerializerMethodField()
    category_summary = serializers.SerializerMethodField()

    def get_category_name(self, obj):

        return obj.category.name

    def get_category_summary(self, obj):

        return obj.category.summary











