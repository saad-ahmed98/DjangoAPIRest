'''filtres utilisés par les vues'''
import django_filters
from .models import Participant,Event,Activity

class ParticipantFilter(django_filters.FilterSet):
    '''filtres de participant sur le nom et prenom'''
    class Meta:
        model = Participant

        fields = ['firstname','lastname']

class ActivityFilter(django_filters.FilterSet):
    '''filtres de l'activité sur le nom et description'''
    class Meta:
        model = Activity

        fields = ['name','description']

class EventFilter(django_filters.FilterSet):
    '''filtres d'evennement sur les dates'''
    start_between = django_filters.DateFromToRangeFilter(field_name='start_at',
                                                             label='start date (range)')
    end_between = django_filters.DateFromToRangeFilter(field_name='end_at',
                                                             label='end date (range)')
    class Meta:
        model = Event

        fields = ['start_at','end_at']
