from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from sonsuz_website.users.api.views import EmailViewSet, UserFollowViewSet, UserFansView, RegisterView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register("email", EmailViewSet)
router.register("user-follow", UserFollowViewSet)
router.register("user-fans", UserFansView)
# router.register("verify-email", VerifyEmailView)
urlpatterns = router.urls
urlpatterns += [
    path('', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),

    path('signup/', include('dj_rest_auth.registration.urls')),
    path("verify-email/", VerifyEmailView.as_view()),

]
