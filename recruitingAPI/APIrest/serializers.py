from rest_framework import serializers
from .models import Participant,Activity,Attendance,Event

# serializer utilisé pour afficher le participant à une attendance
class ParticipantAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'firstname','lastname']

class ParticipantSerializer(ParticipantAttendanceSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'firstname','lastname', 'attendances']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'start_at','end_at', 'attendances']

class AttendanceSerializer(serializers.ModelSerializer):
    participant = ParticipantAttendanceSerializer()
    class Meta:
        model = Attendance
        fields = ['participant', 'was_there']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name','description', 'events']
