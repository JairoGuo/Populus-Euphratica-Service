from django_filters import rest_framework as filters
from sonsuz_website.users.models import User


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username')

    class Meta:
        model = User
        fields = ('username', )  # 允许精准查询的字段
        search_fields = ('name',)  # 允许模糊查询的字段
