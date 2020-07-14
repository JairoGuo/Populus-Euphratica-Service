from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from sonsuz_website.chat.api.views import MessageViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("articles", ArticleViewSet)
router.register("message", MessageViewSet)

urlpatterns = router.urls

