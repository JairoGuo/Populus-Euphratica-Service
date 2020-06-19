import allauth
from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email, send_email_confirmation
from django.core import signing
from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from rest_framework import serializers
from taggit import managers
from sonsuz_website.users.models import User, Homepages
from allauth.account.models import EmailAddress
from sonsuz_website.blog.api.serializers import CategorySerializer, CollectSerializer
from sonsuz_website.blog.models import Article, CollectCategory

class HomePageSerializer(ModelSerializer):

    class Meta:
        model = Homepages
        fields = ['homepage_type', 'homepage_url']

# class SkillSerializer(ModelSerializer):
#
#     class Meta:
#         model = Skill
#         fields = ['name']




class UserSerializer(ModelSerializer):
    homepage = HomePageSerializer(many=True, required=False)
    category = CategorySerializer(many=True, required=False)

    # skill = SkillSerializer(many=True)
    # homepage = StringRelatedField(many=True)

    articles_num = SerializerMethodField()
    category_num = SerializerMethodField()
    collect_num = SerializerMethodField()
    article_by_all = SerializerMethodField()
    article_by_p = SerializerMethodField()
    article_by_d = SerializerMethodField()
    collect_category_by_all = SerializerMethodField()
    collect_category_by_public = SerializerMethodField()
    collect_category_by_private = SerializerMethodField()

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password', 'id', 'last_login', 'groups', 'user_permissions',
                   'is_superuser', 'is_staff', 'is_active']


        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
        read_only_fields = ('email',)

    def get_articles_num(self, obj):
        user = User.objects.get(username=obj).pk
        return Article.objects.filter(user=user).all().count()

    def get_category_num(self, obj):
        return obj.category.count()

    def get_collect_num(self, obj):
        user = User.objects.get(username=obj).pk
        return CollectCategory.objects.filter(user=user).all().count()

    def get_article_by_all(self, obj):
        user = User.objects.get(username=obj).pk
        return Article.objects.filter(user=user).all().count()

    def get_article_by_p(self, obj):
        user = User.objects.get(username=obj).pk
        return Article.objects.filter(user=user, status='P').all().count()

    def get_article_by_d(self, obj):
        user = User.objects.get(username=obj).pk
        return Article.objects.filter(user=user, status='D').all().count()

    def get_collect_category_by_all(self, obj):
        user = User.objects.get(username=obj).pk
        return CollectCategory.objects.filter(user=user).all().count()

    def get_collect_category_by_public(self, obj):
        user = User.objects.get(username=obj).pk
        return CollectCategory.objects.filter(user=user, type='Public').all().count()

    def get_collect_category_by_private(self, obj):
        user = User.objects.get(username=obj).pk
        return CollectCategory.objects.filter(user=user, type='Private').all().count()



class EmailSerializer(ModelSerializer):

    class  Meta:
        model = EmailAddress
        fields = '__all__'

    def create(self, request):
        print(request)
        EmailAddress.objects.create(user=request['user'], email=request['email'])
        self.email_address = EmailAddress.objects.get(email=request['email'])
        # print(signing.dumps(
        #     obj=self.email_address.pk,
        #     salt=app_settings.SALT))

        EmailAddress.send_confirmation(self.email_address)
        return request




