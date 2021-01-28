from datetime import datetime, timedelta
from .models import Activity

def test_generate_events_tous_les_jours():
    # initialisation de l'activité
    activity = Activity(name="jeu",description="jeu")
    start_date = datetime(2020, 12, 26)
    end_date = start_date+timedelta(days=7)

    weekdays = [True,True,True,True,True,True,True] # tous les jours un evennement
    res = activity.generate_events(start_date,end_date,weekdays)
    assert len(res) == 8 # on suppose qu'on aura generé 8 evennements en une semaine

def test_generate_events_aucun_jour():
    # initialisation de l'activité
    activity = Activity(name="jeu",description="jeu")
    start_date = datetime(2020, 12, 26)
    end_date = start_date+timedelta(days=7)

    weekdays = [False,False,False,False,False,False,False] # aucun evennement tous les jours

    res = activity.generate_events(start_date,end_date,weekdays)
    assert len(res) == 0 # on suppose qu'on aura generé aucun evennement

def test_generate_events_un_seul_jour():
    # initialisation de l'activité
    activity = Activity(name="jeu",description="jeu")
    start_date = datetime(2020, 12, 26)
    end_date = start_date+timedelta(days=7)

    # evennement uniquement le jour de depart, donc on en aura 2 si on met en intervalle 1 semaine
    weekdays = [False,False,False,False,False,True,False]

    res = activity.generate_events(start_date,end_date,weekdays)
    assert len(res) == 2 # on suppose qu'on aura generé 2 evennements

    # on verifie qu'ils sont le même jour de la semaine
    assert res[0].start_at.weekday()==5
    assert res[1].start_at.weekday()==5

    # on verifie que les evennements sont à 2 dates à une semaine de distance
    assert res[0].start_at+timedelta(days=7)==res[1].start_at

def test_generate_events_weekdays_invalide():
    # initialisation de l'activité
    activity = Activity(name="jeu",description="jeu")
    start_date = datetime(2020, 12, 26)
    end_date = start_date+timedelta(days=7)

    # initialisation de weekdays avec un nombre d'elements inferieur à 7
    weekdays = [True,True,True,True,True,True]

    res = activity.generate_events(start_date,end_date,weekdays)
    # on suppose qu'on aura generé 0 evennements à cause d'une fin prematurée de la méthode
    assert len(res) == 0