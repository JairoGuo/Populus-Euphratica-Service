import json
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.db.models import F
from django_redis import get_redis_connection
from sonsuz_website.blog.models import Article, Like

from config import celery_app

User = get_user_model()


@celery_app.task()
def commit_visited():
    con = get_redis_connection()
    visited_list = con.hgetall('visited')
    # print(visited_list)
    data = OrderedDict(visited_list)
    for key, value in data.items():
        key = str(key, encoding="utf8")
        Article.objects.filter(article_id=key).update(click_nums=F('click_nums') + int(value))
        con.hdel('visited', key)

    return True


@celery_app.task()
def commit_like():
    con = get_redis_connection()
    like = con.hgetall('like')
    data = OrderedDict(like)
    for key, value in data.items():
        data = json.loads(value)
        user = User.objects.get(pk=data['user'])
        article_instance = Article.objects.get(pk=data['blog_id'])
        Like.objects.create(blog_id=article_instance, user=user)
        con.hdel('like', key)

    return True
