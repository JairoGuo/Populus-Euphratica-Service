from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from sonsuz_website.blog.api.views import CategoryViewSet, CommentsViewSet, ArticleListView, \
    ArticleView, LikeViewSet, CollectViewSet, CollectCategoryViewSet, CategoryFollowViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("articles", ArticleViewSet)
router.register("articles-list", ArticleListView)
router.register("articles", ArticleView)
router.register("category", CategoryViewSet)
router.register("comments", CommentsViewSet)
router.register("likes", LikeViewSet)
router.register("collects", CollectViewSet)
router.register("collects-category", CollectCategoryViewSet)
router.register("category-follow", CategoryFollowViewSet)


urlpatterns = router.urls

