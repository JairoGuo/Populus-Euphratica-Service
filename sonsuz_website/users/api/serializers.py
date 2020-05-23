import allauth
from allauth.account.adapter import get_adapter
from allauth.account import app_settings
from allauth.account.utils import setup_user_email, send_email_confirmation
from django.core import signing
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from taggit import managers
from sonsuz_website.users.models import User, Homepages
from allauth.account.models import EmailAddress

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
    homepage = HomePageSerializer(many=True)
    # skill = SkillSerializer(many=True)
    # homepage = StringRelatedField(many=True)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password', 'id', 'last_login', 'groups', 'user_permissions',
                   'is_superuser', 'is_staff', 'is_active']


        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }



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




