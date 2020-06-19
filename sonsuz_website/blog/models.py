import uuid
from django.conf import settings

from django.db import models

# Create your models here.
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import ugettext_lazy as _
from sonsuz_website.blog.managers import ArticleQuerySet

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class ArticleCategory(models.Model):
    """文章类型"""
    name = models.CharField(max_length=50, verbose_name='类别名称')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='category')

    summary = models.TextField(verbose_name='简介',blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分类'
        ordering = ['created_at']



class Article(models.Model):
    STATUS = (("D", "草稿"), ("P", "发表"))
    TYPE = (('Original', '原创'), ('Reprint', '转载'), ('Translation', '翻译'))
    article_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE, related_name='blog',
                             verbose_name='用户')
    title = models.CharField(verbose_name='标题', max_length=255)
    abstract = models.TextField(null=True, blank=True, verbose_name='摘要')
    cover = models.CharField(verbose_name='封面', max_length=512, blank=True, null=True)
    content = models.TextField(verbose_name='内容')
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='D', verbose_name='文章状态')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name="articles")
    tags = TaggableManager(through=UUIDTaggedItem, blank=True, help_text='多个标签使用英文逗号(,)隔开',
                           verbose_name='文章标签')

    type = models.CharField(verbose_name="文章类型",blank=True, null=True, choices=TYPE, max_length=15)
    original_url = models.URLField(verbose_name='原文地址', blank=True)
    # likers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liked_news",
    #                                 verbose_name='点赞用户')
    # comment = models.BooleanField(default=False, verbose_name='评论')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_index=True)

    # objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = '文章'
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='blog_comment_user')
    content = models.TextField(verbose_name='内容')
    blog_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='ID')
    reply_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='like_user')
    blog_id = models.ForeignKey(Article, on_delete=models.CASCADE,  related_name='likes', verbose_name='ID')





# 文章收藏分类
class CollectCategory(models.Model):

    TYPE = (('Public', '公开'), ('Private', '私密'))
    name = models.CharField(max_length=50, verbose_name='类别名称')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='collect_category')
    type = models.CharField(max_length=50, verbose_name='收藏类别', choices=TYPE, default='Public')
    description = models.TextField(verbose_name='描述', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '收藏分类'
        ordering = ['created_at']


# 文章收藏
class Collect(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='follow_user')

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='收藏文章', related_name="collect_article")

    category = models.ManyToManyField(CollectCategory, blank=True, related_name='collect')

    # def __str__(self):
    #     return self.article


# TODO: 关注专栏
class CategoryFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE,
                             verbose_name='用户', related_name='category_follow_user')

    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, blank=True, related_name='category_follow')

