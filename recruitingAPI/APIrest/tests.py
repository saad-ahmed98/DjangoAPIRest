from django.test import TestCase
import pytest
from .models import Activity
from datetime import datetime, timedelta

@pytest.mark.django_db
def test_generate_events():
    # initialisation de l'activité
    a = Activity(name="jeu",description="jeu")
    a.save()
    start_date = datetime(2020, 12, 26)
    end_date = start_date+timedelta(days=7)

    weekdays = [True,True,True,True,True,True,True] # tous les jours un evennement
    res = a.generate_events(start_date,end_date,weekdays)
    assert(len(res) == 8) # on suppose qu'on aura generé 8 evennements en une semaine

    weekdays = [False,False,False,False,False,False,False] # aucun evennement tous les jours

    res = a.generate_events(start_date,end_date,weekdays)
    assert(len(res) == 0) # on suppose qu'on aura generé aucun evennement

    weekdays = [False,False,False,False,False,True,False] # evennement uniquement le jour de depart, donc on en aura 2 si on met en intervalle 1 semaine

    res = a.generate_events(start_date,end_date,weekdays)
    assert(len(res) == 2) # on suppose qu'on aura generé 2 evennements

    # on verifie qu'ils sont le même jour de la semaine
    assert(res[0].start_at.weekday()==5) 
    assert(res[1].start_at.weekday()==5)

    assert(res[0].start_at+timedelta(days=7)==res[1].start_at) # on verifie que les evennements sont à 2 dates à une semaine de distance

    weekdays = [True,True,True,True,True,True] # initialisation de weekdays avec un nombre d'elements inferieur à 7

    res = a.generate_events(start_date,end_date,weekdays)
    assert(len(res) == 0) # on suppose qu'on aura generé 0 evennements à cause d'une fin prematurée de la méthode
