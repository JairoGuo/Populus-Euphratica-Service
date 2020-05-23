
from rest_framework.serializers import ModelSerializer

from sonsuz_website.ImageHosting.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



