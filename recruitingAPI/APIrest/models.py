from django.db import models
from datetime import datetime, timedelta

class Participant(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)


class Activity(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    """
    méthode de generation des evennements
    prend en parametre 2 datetime correspondants à la date de début et la date de fin sur lequels on genere
    prend en paramtre aussi une liste de booleans correspondants aux jours de la semaine
    renvoit une liste des evennements generés
    """
    def generate_events(self, start_date, end_date, weekdays):
        counter = start_date
        res = []
        if(len(weekdays) < 7): # si liste incomplete, on annule la generation
            return res
        while counter <= end_date:
            if(weekdays[counter.weekday()]):
                res.append(
                    Event(start_at=counter, end_at=counter, activity=self))
            counter = counter + timedelta(days=1)
        return res


class Event(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    activity = models.ForeignKey(
        Activity, related_name='events', on_delete=models.CASCADE)


class Attendance(models.Model):
    class Meta:
        unique_together = ('event', 'participant')
    was_there = models.BooleanField(default=False)
    event = models.ForeignKey(
        Event, related_name='attendances', on_delete=models.CASCADE)
    participant = models.ForeignKey(
        Participant, related_name='attendances', on_delete=models.CASCADE)
