'''interface administrateur de l'api'''
from django.contrib import admin
from .models import Attendance,Participant,Event,Activity

admin.site.register(Attendance)
admin.site.register(Participant)
admin.site.register(Event)
admin.site.register(Activity)
