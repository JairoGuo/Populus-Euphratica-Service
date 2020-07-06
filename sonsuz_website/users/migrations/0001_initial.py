# Generated by Django 3.0.5 on 2020-06-29 13:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='昵称')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='真实姓名')),
                ('avatar', models.ImageField(blank=True, default='', null=True, upload_to='users/avatars/', verbose_name='用户头像')),
                ('sex', models.CharField(choices=[('M', '男'), ('F', '女'), ('P', '不公开')], default='P', max_length=50, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='生日')),
                ('position', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='职位')),
                ('company', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='公司')),
                ('education', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='学历')),
                ('industry', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='行业')),
                ('introduction', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='简介')),
                ('website', models.URLField(blank=True, default='', max_length=255, null=True, verbose_name='网站')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('skill', taggit.managers.TaggableManager(blank=True, help_text='多个标签使用英文逗号(,)隔开', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='技能')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow', to=settings.AUTH_USER_MODEL, verbose_name='关注')),
                ('follow_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_to', to=settings.AUTH_USER_MODEL, verbose_name='粉丝')),
            ],
        ),
        migrations.CreateModel(
            name='Homepages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homepage_type', models.CharField(choices=[('github', 'Github'), ('weibo', '微博'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('wechat', '微信'), ('WCOA', '公众号')], max_length=255, verbose_name='主页名称')),
                ('homepage_url', models.URLField(max_length=255, verbose_name='主页地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homepage', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
