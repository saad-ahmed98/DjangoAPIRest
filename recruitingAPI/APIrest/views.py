from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Participant,Event,Activity,Attendance
from .serializers import *
from .filters import ParticipantFilter,ActivityFilter,EventFilter

class ParticipantView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    '''vue generique manipulant une liste de participants [POST, GET]'''

    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    lookup_field = 'id'
    filterset_class = ParticipantFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)

        return self.list(request)

    def post(self, request):
        return self.create(request)

class ParticipantDetailsView(ParticipantView):
    '''vue generique manipulant un participant specifique [POST, GET, DELETE, PATCH, PUT]'''

    def put(self, request, id=None):
        return self.update(request, id)

    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

class ActivityView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    '''vue generique manipulant une liste d'activité [POST, GET]'''

    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    lookup_field = 'id'
    filterset_class = ActivityFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

class ActivityDetailsView(ActivityView):
    '''vue generique manipulant une activité specifique [POST, GET, DELETE, PATCH, PUT]'''

    def put(self, request, id=None):
        return self.update(request, id)

    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

class EventView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    '''vue generique manipulant une liste d'evennement [POST, GET]'''

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilter
    filter_backends = [filters.DjangoFilterBackend]
    lookup_field = 'id'

    def get(self, request, id = None):
        if id:
            return self.retrieve(request)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

class EventDetailsView(EventView):

    '''vue generique manipulant evennement [POST, GET, DELETE, PATCH, PUT]'''

    def put(self, request, id=None):
        return self.update(request, id)

    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


@api_view(['POST'])
def generate_events(request,id):
    """méthode correspondant à la vue specifique generant les evennements sur une periode donnée,
    la période est donnée par une query:
    start_date : date de début,
    end_date : date de fin,
    weekdays : liste de booleans, chaque boolean étant un jour de la semaine
    pour l'appeler, utiliser une requete POST en JSON
    ex : {
        "start_date": "2010-01-20T00:00:00+01:00",
        "end_date": "2010-01-22T00:00:00+01:00",
        "weekdays": [true,true,true,true,true,true,true]
    }"""

    serializer = GenerateEventsSerializer(data=request.data)
    if serializer.is_valid():
        start_date = serializer.validated_data['start_date']
        end_date =  serializer.validated_data['end_date']
        weekdays = serializer.validated_data['weekdays']
        activity = get_object_or_404(Activity,id=id)
        res = activity.generate_events(start_date,end_date,weekdays)
        if len(res)>0 :
            for event in res :
                event.save()
            return Response(status=201)
    return Response(status=400) # if no event created


@api_view(['GET', 'POST', 'PATCH'])
def update_participants(request,id):
    """
    méthode specifique correspondant à la generation de participants
    à un evennement et à leur manipulation.
    Pour POST et PATCH, on supposera que le corps des requetes sont des json correspondant à :
    POST aura pk du participant que l'on rajoutera à l'evennement
    PATCH aura pk du participant et was_there d'attendance à modifier
    pour indiquer s'il a participé ou pas
    ex : pour PATCH {"pk":1,"was_there":true} ou pour POST {"pk":1}
    """
    if request.method == 'POST':
        serializer = UpdatePostParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            participant = get_object_or_404(Participant,id=serializer.validated_data['pk'])
            event = get_object_or_404(Event,id=id)
            try :
                attendance = Attendance.objects.create(was_there=False,
                                    event=event,participant=participant)
                attendance.save()
                return  Response(AttendanceSerializer(attendance).data)
            except IntegrityError:
                return Response(status=304) # envoit une erreur si l'attendance existe déjà
                # car un participant ne peut pas avoir plusieurs attendances sur un même evennement
    if request.method == 'GET':
        event = get_object_or_404(Event,id=id)
        query_attendances = Attendance.objects.filter(event=event)
        if query_attendances.count()>0:
            return Response(AttendanceSerializer(query_attendances,many=True).data)

    if request.method == 'PATCH':
        serializer = UpdatePatchParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            participant = get_object_or_404(Participant,id=serializer.validated_data['pk'])
            event = get_object_or_404(Event,id=id)
            attendance = get_object_or_404(Attendance,participant=participant,event=event)
            attendance.was_there=serializer.validated_data['was_there']
            attendance.save()
            return  Response(AttendanceSerializer(attendance).data)
    return Response(status=400)
