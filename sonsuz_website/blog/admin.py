from django.contrib import admin
from .models import Article, ArticleCategory
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    fields = ['user', 'title', 'cover', 'category', 'abstract', 'click_nums', 'content', 'tags']

class ArticleCategoryAdmin(admin.ModelAdmin):

    fields = ['user', 'name']

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
