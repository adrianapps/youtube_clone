from django_filters import rest_framework as django_filters
from django_filters.widgets import RangeWidget

from channel.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains']
        }
