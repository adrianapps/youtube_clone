from django.db.models import Count
from django_filters import rest_framework as django_filters
from django_filters.widgets import RangeWidget

from channel.models import User, Channel


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains']
        }


class ChannelFilter(django_filters.FilterSet):
    creation_date = django_filters.DateTimeFromToRangeFilter(
        widget=RangeWidget(attrs={'type': 'date'}))
    subscribers = django_filters.RangeFilter(method='filter_by_subscriber_count')

    class Meta:
        model = Channel
        fields = {
            'name': ['icontains'],
            'user__username': ['icontains'],
        }

    def filter_by_subscriber_count(self, queryset, name, value):
        if value:
            return queryset.filter(subscriber_count__range=(value.start, value.stop))
        return queryset
