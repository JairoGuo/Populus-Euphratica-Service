# Generated by Django 3.0.5 on 2020-05-30 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_at'], 'verbose_name': '文章'},
        ),
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'ordering': ['created_at'], 'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='多个标签使用英文逗号(,)隔开', through='blog.UUIDTaggedItem', to='taggit.Tag', verbose_name='文章标签'),
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.CharField(blank=True, choices=[('Original', '原创'), ('Reprint', '转载'), ('Translation', '翻译')], max_length=15, null=True, verbose_name='文章类型'),
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
