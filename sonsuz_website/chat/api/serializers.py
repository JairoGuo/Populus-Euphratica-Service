
from rest_framework.serializers import ModelSerializer, StringRelatedField

from sonsuz_website.chat.models import Message


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
