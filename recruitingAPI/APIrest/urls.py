'''endpoints de l'api'''
from django.urls import path
from .views import (ParticipantView,ParticipantDetailsView,EventView,
ActivityView,EventDetailsView,ActivityDetailsView,
generate_events, update_participants)


urlpatterns = [
    # route manipulant les participants par leur id
    path('participant/<int:id>/', ParticipantDetailsView.as_view()),
    # route manipulant la liste complète des participants
    path('participant/', ParticipantView.as_view()),
    # route manipulant la liste des participants à un evennement precis
    path('event/<int:id>/participants/', update_participants),
    # route manipulant un evennement à partir de son id
    path('event/<int:id>/', EventDetailsView.as_view()),
    # route manipulant la liste complète des evennements
    path('event/', EventView.as_view()),
    # route permettant de generer des evennements pour une activité
    path('activity/<int:id>/generate_events/', generate_events),
    # route permettant de manipuler une activité à partir de son id
    path('activity/<int:id>/', ActivityDetailsView.as_view()),
    # route manipulant la liste complète des activités
    path('activity/', ActivityView.as_view()),
]
