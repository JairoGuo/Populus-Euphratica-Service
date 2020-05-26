from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CharField, DateField, URLField, ManyToManyField, DateField, ImageField, \
    IntegerField, ForeignKey
from django.utils import timezone

from django.urls import reverse

from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    nickname = CharField(verbose_name="昵称", null=True, blank=True, max_length=255, default='')
    name = CharField(verbose_name="真实姓名", null=True, blank=True, max_length=255, default='')
    avatar = ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='用户头像', default='')
    sex = CharField(verbose_name="性别", choices=(("M", "男"), ("F", "女"), ("P", "不公开")), default="P", max_length=50)
    birthday = DateField(verbose_name="生日", null=True, blank=True, default=timezone.now)
    position = CharField(verbose_name="职位", null=True, blank=True, max_length=255, default='')
    company = CharField(verbose_name="公司", null=True, blank=True, max_length=255, default='')
    education = CharField(verbose_name="学历", null=True, blank=True, max_length=255, default='')
    industry = CharField(verbose_name="行业", null=True, blank=True, max_length=255, default='')
    introduction = CharField(verbose_name="简介", null=True, blank=True, max_length=255, default='')
    website = URLField(verbose_name="网站", null=True, blank=True, max_length=255, default='')
    # skill = TaggableManager(help_text='多个标签使用英文逗号(,)隔开', blank=True, verbose_name='技能')
    skill = CharField(verbose_name='技能', blank=True,null=True, default='', max_length=512)
    # homepage = ManyToManyField(Homepages, null=True, blank=True, verbose_name="个人主页")
    # medal = ForeignKey(Medal, on_delete=models.CASCADE, verbose_name="勋章")

    created_at = DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


# class Skill(Model):
#     user = ForeignKey(User,on_delete=models.CASCADE, related_name='skill')
#     name = CharField(max_length=20)



class Homepages(Model):

    user = ForeignKey(User, on_delete=models.CASCADE, related_name='homepage')
    choices = (("github", "Github"), ("weibo", "微博"),
               ("facebook", "Facebook"), ("twitter", "Twitter"),
               ("wechat", "微信"), ("WCOA", "公众号"))
    homepage_type = CharField(verbose_name="主页名称", choices=choices, max_length=255)
    homepage_url = URLField(verbose_name="主页地址", max_length=255)

    def __str__(self):
        return self.homepage_type
