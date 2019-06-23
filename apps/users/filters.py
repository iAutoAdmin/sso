import django_filters

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserFilter(django_filters.rest_framework.FilterSet):
    """
    用户过滤类
    """
    # username = django_filters.CharFilter(method='search_username')
    # name = django_filters.CharFilter(method='search_username')
    # is_active = django_filters.CharFilter(method='search_username')
    #
    # def search_username(self, queryset, name, value):
    #     return queryset.filter(Q(name__icontains=value) | Q(username__icontains=value) | Q(is_active=value))

    username = django_filters.CharFilter(lookup_expr='icontains', help_text='请输入用户名')
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='请输入中文名')
    is_active = django_filters.CharFilter(lookup_expr='icontains', help_text='状态')

    class Meta:
        model = User
        fields = ['username', 'name', 'is_active']