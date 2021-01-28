'''serializers pour manipuler du json sur l'api'''
from rest_framework import serializers
from .models import Participant,Activity,Attendance,Event

class ParticipantAttendanceSerializer(serializers.ModelSerializer):
    '''serializer utilisé pour afficher le participant d'une attendance'''

    class Meta:
        model = Participant
        fields = ['id', 'firstname','lastname']

class ParticipantSerializer(ParticipantAttendanceSerializer):
    '''serializer utilisé pour afficher un participant dans sa totalité'''

    class Meta:
        model = Participant
        fields = ['id', 'firstname','lastname', 'attendances']

class EventSerializer(serializers.ModelSerializer):
    '''serializer utilisé pour afficher evennement'''

    class Meta:
        model = Event
        fields = ['id', 'start_at','end_at', 'attendances']

class AttendanceSerializer(serializers.ModelSerializer):
    '''serializer utilisé pour afficher une attendance'''

    participant = ParticipantAttendanceSerializer()
    class Meta:
        model = Attendance
        fields = ['participant', 'was_there']

class ActivitySerializer(serializers.ModelSerializer):
    '''serializer utilisé pour afficher une activité'''

    class Meta:
        model = Activity
        fields = ['id', 'name','description', 'events']

class GenerateEventsSerializer(serializers.Serializer):
    '''serializer utilisé pour parser le json en entrée de la generation d'evennements'''

    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    weekdays = serializers.ListField(child=serializers.BooleanField())

class UpdatePostParticipantsSerializer(serializers.Serializer):
    '''serializer utilisé pour parser le json en entrée de l'update des participants en POST'''

    pk = serializers.IntegerField()

class UpdatePatchParticipantsSerializer(UpdatePostParticipantsSerializer):
    '''serializer utilisé pour parser le json en entrée de l'update des participants en PATCH'''

    was_there = serializers.BooleanField()
