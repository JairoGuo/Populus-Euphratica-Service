import uuid

from django.db import models

# Create your models here.


class Image(models.Model):

    def image_upload_to(instance, filename):
        return 'images/{uuid}{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)

    image = models.ImageField(verbose_name='图片', upload_to=image_upload_to, blank=True, null=True)
