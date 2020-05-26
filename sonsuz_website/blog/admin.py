from django.contrib import admin
from .models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    fields = ['user', 'title', 'cover', 'abstract', 'click_nums', 'content', 'tags']
admin.site.register(Article, ArticleAdmin)
