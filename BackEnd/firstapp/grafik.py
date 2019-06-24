from django.shortcuts import render
from .models import Tovar, PhotoTovara, VidArendi,Otziv, Set, Person, VidArendiTovars, TovarPerson
import django.contrib.auth as auth
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import timedelta, datetime, date
from .form import PersonForm

class Graf():
    def GrafikSpisania(self, person):
        try:
            tovars = person.tovarperson_set.all();
            Grafik = {}
            for tov in tovars:
                if tov.VidArendiTovars.vidArendi.name == "Аренда":
                    start = tov.Data
                    price = tov.VidArendiTovars.stoimost
                    oplatVik = tov.VidArendiTovars.vikup
                    ostalos = oplatVik
                    if (tov.oplata_set.count() > 0):
                        oplata = tov.oplata_set.count()
                        ostalos =  oplatVik - oplata
                        start = tov.oplata_set.order_by('-Data')[0].Date
                    if datetime.now().year == start.year:
                        if datetime.now().month == start.month:
                            if datetime.now().day > start.day:
                                start = start + timedelta(days=30)
                    Vozvrat = []
                    summ = 0;
                    while summ < ostalos:
                        Vozvrat.append({'time':start, 'Summ':price})
                        summ = summ + price
                        start = start + timedelta(days=30)

                    name = tov.VidArendiTovars.tovar.name
                    tip = tov.VidArendiTovars.vidArendi.name
                    Grafik[tov.id] = {'type': tip, 'grafik':Vozvrat}

                if tov.VidArendiTovars.vidArendi.name == "Погонять":

                    start = tov.Data
                    price = tov.VidArendiTovars.stoimost
                    Vozvrat = []
                    Vozvrat.append({'time': start, 'Summ': price})

                    name = tov.VidArendiTovars.tovar.name
                    tip = tov.VidArendiTovars.vidArendi.name
                    Grafik[tov.id] = {'type': tip, 'grafik': Vozvrat, 'Pogon': True}

            return Grafik
        except:
            Grafik = {}

    def PreobraGrafik(self, Dannye , dni):
        try:
            dateMin = datetime.now() - timedelta(days=dni)
            dateMax = datetime.now() + timedelta(days=dni)
            dni = []
            start = dateMin
            while start <= dateMax:
                dni.append(start)
                start = start + timedelta(days=1)

            Vozvrat = []

            itogoA = 0
            itogoP = 0

            if dni != 0:
                start = datetime(dni[0].year, dni[0].month, 1)
                cikl = start
                while start.month == cikl.month:

                    for tovari in Dannye:
                        if (Dannye[tovari]['type'] == 'Аренда'):
                            for dann in Dannye[tovari]['grafik']:
                                if (dann['time'].day == start.day and dann['time'].month == start.month and dann[
                                    'time'].year == start.year):
                                    itogoA = itogoA + dann['Summ']

                        if (Dannye[tovari]['type'] == 'Погонять'):
                            for dann in Dannye[tovari]['grafik']:
                                if (dann['time'].day == start.day and dann['time'].month == start.month and dann[
                                    'time'].year == start.year):
                                    itogoP = itogoP + dann['Summ']

                    start = start + timedelta(days=1)



            for date in dni:
                Arenda = 0
                Pogon = 0
                for tovari in Dannye:

                    if (Dannye[tovari]['type'] == 'Аренда'):
                        for  dann in Dannye[tovari]['grafik']:
                            if ( dann['time'].day == date.day and dann['time'].month == date.month and dann['time'].year == date.year ):
                                Arenda = Arenda + dann['Summ']

                    if (Dannye[tovari]['type'] == 'Погонять'):
                        for  dann in Dannye[tovari]['grafik']:
                            if ( dann['time'].day == date.day and dann['time'].month == date.month and dann['time'].year == date.year ):
                                Pogon = Pogon + dann['Summ']


                moth = ''
                if (date.month == 1):
                    moth = 'Январь'
                if (date.month == 2):
                    moth = 'Февраль'
                if (date.month == 3):
                    moth = 'Март'
                if (date.month == 4):
                    moth = 'Апрель'
                if (date.month == 5):
                    moth = 'Май'
                if (date.month == 6):
                    moth = 'Июнь'
                if (date.month == 7):
                    moth = 'Июль'
                if (date.month == 8):
                    moth = 'Август'
                if (date.month == 9):
                    moth = 'Сентябрь'
                if (date.month == 10):
                    moth = 'Октябрь'
                if (date.month == 11):
                    moth = 'Ноябрь'
                if (date.month == 12):
                    moth = 'Декабрь'

                Vozvrat.append({'Day': date.day, 'Motnh':moth, 'Arenda': Arenda, 'Pogon': Pogon})

            return {'itogoA':itogoA, 'itogoP':itogoP, 'spis':Vozvrat}
        except:
            return {'itogoA':0, 'itogoP':0, 'spis':{}}

    def NormGraf(self, pers):
        try:
            tovar = TOVAR()
            dannye = self.GrafikSpisania(person=pers)
            itogo = []
            for d in dannye:
                vozvrat = {}
                vozvrat['name'] = tovar.GetTovarId(d).name
                mass = []
                for graf in dannye[d]['grafik']:
                    if graf.get('Pogon') != None:
                        mass.append({'Summ': graf['Summ'], 'time': self._normdate(graf['time']), 'Pogon':True})
                    else:
                        mass.append({'Summ':graf['Summ'], 'time':self._normdate(graf['time'])})
                vozvrat['graf'] = mass
                itogo.append(vozvrat)
            return itogo
        except:
            return []

    def _normdate(self, date):
        try:
            day = date.strftime("%d")
            month =  date.strftime("%m")
            year = date.strftime("%y")

            moth = ''
            if (month == "01"):
                moth = 'Января'
            if (month == "02"):
                moth = 'Февраля'
            if (month == "03"):
                moth = 'Марта'
            if (month == "04"):
                moth = 'Апреля'
            if (month == "05"):
                moth = 'Мая'
            if (month == "06"):
                moth = 'Июня'
            if (month == "07"):
                moth = 'Июля'
            if (month == "08"):
                moth = 'Августа'
            if (month == "09"):
                moth = 'Сентября'
            if (month == "10"):
                moth = 'Октября'
            if (month == "11"):
                moth = 'Ноября'
            if (month == "12"):
                moth = 'Декабря'

            return day + " "+ moth+ " " +year ;
        except:
            return 'Не удалось загрузить дату'
