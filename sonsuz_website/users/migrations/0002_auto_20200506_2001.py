# Generated by Django 3.0.5 on 2020-05-06 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='skill',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='技能'),
        ),
    ]