import django_filters
from .models import Participant,Event,Activity

class ParticipantFilter(django_filters.FilterSet):
    
    class Meta:
        model = Participant

        fields = ['firstname','lastname']

class ActivityFilter(django_filters.FilterSet):
    
    class Meta:
        model = Activity

        fields = ['name','description']

class EventFilter(django_filters.FilterSet):
    start_between = django_filters.DateFromToRangeFilter(field_name='start_at',
                                                             label='start date (range)')
    end_between = django_filters.DateFromToRangeFilter(field_name='end_at',
                                                             label='end date (range)')
    class Meta:
        model = Event

        fields = ['start_at','end_at']