from django.db import models
from django.db.models.aggregates import Count


class ArticleQuerySet(models.query.QuerySet):

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").select_related('user').order_by('-created_at')

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").select_related('user').order_by('-updated_at')

    def get_by_user(self, user):
        """返回所有的文章"""
        return self.filter(user=user).select_related('user').order_by('-updated_at')

    def get_counted_tags(self):
        """统计所有已发布的文章中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        query = self.filter(status='P').annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()
