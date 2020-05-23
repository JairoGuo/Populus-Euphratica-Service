import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)



    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class NewsImage(models.Model):

    def image_upload_to(instance, filename):
        return 'image-hosting/{uuid}{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)

    image = models.ImageField(verbose_name='图片', upload_to=image_upload_to, blank=True, null=True)



class News(models.Model):


    def image_upload_to(instance, filename):
        return 'news/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


    news_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="资讯id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE, related_name='news',
                             verbose_name='用户')
    title = models.CharField(verbose_name='标题', max_length=255)
    abstract = models.TextField(null=True, blank=True, verbose_name='摘要')
    # cover = models.ImageField(verbose_name='封面', upload_to=image_upload_to, blank=True, null=True)
    cover = models.CharField(verbose_name='封面', max_length=512, blank=True, null=True)
    content = models.TextField(verbose_name='资讯内容')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    # tags = models.ManyToManyField(Tags, verbose_name=u'文章标签')
    # tags = TaggableManager(through=UUIDTaggedItem, blank=True, help_text='多个标签使用英文逗号(,)隔开', verbose_name='文章标签')
    tags = TaggableManager(through=UUIDTaggedItem, blank=True, help_text='多个标签使用英文逗号(,)隔开', verbose_name='文章标签', related_name='tags')

    # likers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liked_news",
    #                                 verbose_name='点赞用户')
    # comment = models.BooleanField(default=False, verbose_name='评论')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_index=True)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    content = models.TextField(verbose_name='内容')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comment', verbose_name='资讯ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    news = models.ForeignKey(News, on_delete=models.CASCADE,  related_name='like', verbose_name='资讯ID')
