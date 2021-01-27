from django.shortcuts import render, get_object_or_404
from .models import Participant,Activity,Attendance,Event
from django.http import HttpResponse
from django.db import IntegrityError
from .serializers import ParticipantSerializer,ActivitySerializer,EventSerializer, AttendanceSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework import filters
from datetime import datetime
import ast
import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from json.decoder import JSONDecodeError

# vue generique manipulant une liste de participants [POST, GET]
class ParticipantView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstname', 'lastname']

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)

        else:
           return self.list(request)

    def post(self, request):
        return self.create(request)

# vue generique manipulant un participant specifique [POST, GET, DELETE, PATCH, PUT]
class ParticipantDetailsView(ParticipantView):
    
    def put(self, request, id=None):
        return self.update(request, id)
    
    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

# vue generique manipulant une liste d'activité [POST, GET]
class ActivityView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)

        else:
           return self.list(request)

    def post(self, request):
        return self.create(request)

# vue generique manipulant une activité specifique [POST, GET, DELETE, PATCH, PUT]
class ActivityDetailsView(ActivityView):

    def put(self, request, id=None):
        return self.update(request, id)
    
    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

# vue generique manipulant une liste d'evennement [POST, GET]
class EventView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['start_at', 'end_at']
    lookup_field = 'id'

    """
    méthode de récupération des événements sur une période donnée
    prend en paramètres 2 chaines de caractères, chacune correspondant à une date au format dd/mm/aa
    renvoit la liste des evennements trouvés ou une reponse HTTP d'erreur
    pour l'appeler, utiliser une query avec GET sur le url, ex : .../?query_start=01/01/01&query_end=02/02/02
    """
    def filter_events(self,query_start_str,query_end_str):
        try:
            query_start = datetime.strptime(query_start_str, '%d/%m/%y')
            query_end = datetime.strptime(query_end_str, '%d/%m/%y')
        except ValueError as ve:
            return HttpResponse(status=400) # si erreur dans le format
        events = Event.objects.filter(end_at__gte=query_start).filter(start_at__lte=query_end)
        
        if(events.count()>0):
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        return HttpResponse(status=404) # si aucun evennement trouvé
    
    def get(self, request, id = None):
        query_start_str = request.GET.get('query_start')
        query_end_str = request.GET.get('query_end')
        if(query_start_str and query_end_str):
            return self.filter_events(query_start_str,query_end_str)
            
        if id:
            return self.retrieve(request)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

# vue generique manipulant evennement [POST, GET, DELETE, PATCH, PUT]
class EventDetailsView(EventView):
    
    def put(self, request, id=None):
        return self.update(request, id)
    
    def patch(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

"""
méthode correspondant à la vue specifique generant les evennements sur une periode donnée,
la période est donnée par une query:
start_date : date de début, end_date : date de fin, weekdays : liste de booleans, chaque boolean étant un jour de la semaine
chaque date correspondant au format dd/mm/yy
pour l'appeler, utiliser une query avec GET sur le url, ex : .../generate_events/?query_start=01/01/01&query_end=02/02/02&weekdays=[True,True,True,True,True,True,True]
"""
@api_view(['GET'])
def generate_events(request,id):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    weekdays_str = request.GET.get('weekdays')
    if(start_date_str and end_date_str and weekdays_str) :
        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%y')
            weekdays = ast.literal_eval(weekdays_str)
        except ValueError as ve:
            return HttpResponse(status=400) # if error in format
        activity = Activity.objects.get(id=id)
        res = activity.generate_events(start_date,end_date,weekdays)
        if len(res)>0 :
            for event in res :
                event.save()
            return HttpResponse(status=201)
    return HttpResponse(status=400) # if no event created

"""
méthode specifique correspondant à la generation de participants à un evennement et à leur manipulation
pour POST et PATCH, on supposera que le corps des requetes sont des json correspondant à :
POST aura pk du participant que l'on rajoutera à l'evennement
PATCH aura pk du participant et was_there d'attendance à modifier pour indiquer s'il a participé ou pas
ex : pour PATCH {"pk":1,"was_there":true} ou pour POST {"pk":1}
"""
@api_view(['GET', 'POST', 'PATCH'])
def update_participants(request,id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try :
            pk = json.loads(body_unicode)['pk']
        except JSONDecodeError as jde :
            return HttpResponse(status=400)
        if(not pk) :
            return HttpResponse(status=404)
        participant = get_object_or_404(Participant,id=pk)
        event = get_object_or_404(Event,id=id)
        try :
            attendance = Attendance.objects.create(was_there=False,event=event,participant=participant)
            attendance.save()
            return  Response(AttendanceSerializer(attendance).data)
        except IntegrityError as ie : 
             return HttpResponse(status=304) # envoit une erreur si l'attendance existe déjà
                                             # car un participant ne peut pas avoir plusieurs attendances sur un même evennement
    if request.method == 'GET':
        event = get_object_or_404(Event,id=id)
        query_attendances = Attendance.objects.filter(event=event)
        if(query_attendances.count()>0):
            return Response(AttendanceSerializer(query_attendances,many=True).data)

    if request.method == 'PATCH':
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except JSONDecodeError as jde :
            return HttpResponse(status=400)
        pk = body['pk']
        was_there = body['was_there']
        if(not pk) or (not was_there) :
            return HttpResponse(status=404)
        participant = get_object_or_404(Participant,id=pk)
        event = get_object_or_404(Event,id=id)
        attendance = get_object_or_404(Attendance,participant = participant,event=event)
        attendance.was_there=was_there
        attendance.save()
        return  Response(AttendanceSerializer(attendance).data)
    return HttpResponse(status=400)
