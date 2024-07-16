from django.db.models import Count
from django_filters import rest_framework as django_filters
from django_filters.widgets import RangeWidget

from video.models import Tag, Video, WatchLater, Channel


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = {
            'name': ['icontains']
        }


class VideoFilter(django_filters.FilterSet):
    upload_date = django_filters.DateTimeFromToRangeFilter(
        widget=RangeWidget(attrs={'type': 'date'}))
    likes = django_filters.RangeFilter(method='filter_by_likes_count')
    dislikes = django_filters.RangeFilter(method='filter_by_dislikes_count')
    views = django_filters.RangeFilter()

    class Meta:
        model = Video
        fields = {
            'title': ['icontains'],
            'user__username': ['icontains'],
            'channel__name': ['icontains'],
            'description': ['icontains']
        }

    def filter_by_likes_count(self, queryset, name, value):
        if value:
            return queryset.filter(likes_count__range=(value.start, value.stop))
        return queryset

    def filter_by_dislikes_count(self, queryset, name, value):
        if value:
            return queryset.filter(dislikes_count__range=(value.start, value.stop))
        return queryset
