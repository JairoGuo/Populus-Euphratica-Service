from django.contrib import admin
from .models import News, Like, Comment
# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'cover', 'abstract', 'click_nums', 'content', 'tags']


class LikeAdmin(admin.ModelAdmin):
    fields = ['user', 'news']



class CommentAdmin(admin.ModelAdmin):
    fields = ['content', 'news', 'user']



admin.site.register(News, NewsAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
