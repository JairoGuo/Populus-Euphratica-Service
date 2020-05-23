from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from sonsuz_website.users.api.views import EmailViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register("email", EmailViewSet)

# router.register("verify-email", VerifyEmailView)
urlpatterns = router.urls
urlpatterns += [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path("verify-email/", VerifyEmailView.as_view()),

]
