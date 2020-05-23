from django.conf import settings
from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.documentation import include_docs_urls

from sonsuz_website.news.api.views import NewsImageViewSet, upload_file
from sonsuz_website.users.api.views import UserViewSet
from sonsuz_website import users
app_name = "api"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('accounts/', include('sonsuz_website.users.api.api_router')),
    path('news/', include('sonsuz_website.news.api.api_router')),
    path('blog/', include('sonsuz_website.blog.api.api_router')),
    path('upload-image/', include('sonsuz_website.ImageHosting.api.api_router')),


]

