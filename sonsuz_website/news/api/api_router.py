from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from sonsuz_website.news.api.views import NewsViewSet, NewsImageViewSet, upload_file

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register("", NewsViewSet)
# router.register("upload-image", NewsImageViewSet)
urlpatterns = router.urls

