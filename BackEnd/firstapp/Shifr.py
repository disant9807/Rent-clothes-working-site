from django.shortcuts import render
from .models import Tovar, PhotoTovara, VidArendi,Otziv,  Set, Person, VidArendiTovars, TovarPerson
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import timedelta, datetime, date
from .form import PersonForm

class Shifr():
    def ProverNone(self,*args, Vozvrat = True, slov={}):

        vozvrat = {}
        if Vozvrat == True:
            for ar in args:
                vozvrat[ar.Value] = slov.get(ar.Value, ar.Ret)
        else:
            for ar in args:
                if slov.get(ar.Value) != None:
                    vozvrat[ar.Value] = slov.get(ar.Value)
        return vozvrat

    def ProverNoneZnack(self,*args, Vozvrat = True, slov={}):

        vozvrat = {}
        if Vozvrat == True:
            for ar in args:
                vozvrat[ar.name] = slov.get(ar.value, ar.voz)
        else:
            for ar in args:
                if slov.get(ar.value) != None:
                    vozvrat[ar.name] = slov.get(ar.value)
        return vozvrat

    def ProverZnackMass(self, *args, slov={}):
        mass = []
        for ar in args:
            if slov.get(ar.znack) == ar.proverka:
                mass.append(ar.value)
        return mass

    def ProverkaMass (self, *args, slov={},Vozvrat = True, err = []):
        mass = []
        for ar in args:
            test = True
            for zna in err:
                if slov.get(ar.Value) == zna:
                    test = False

            if test == True:
                mass.append(slov.get(ar.Value))

            if test == False and Vozvrat == True:
                mass.append(ar.Ret)

        return mass



class ShifrDitek():
    Value = []
    Ret = None
    def __init__(self, val, ret):
        self.Value = val
        self.Ret = ret

class ZnackMassDitek():
    znack = ""
    value = ""
    proverka = ""
    def __init__(self, zn, vl, pr):
        self.znack = zn
        self.value = vl
        self.proverka = pr

class ShDZN():
    value = None
    voz = None
    name = None
    def __init__(self,va,vo,na):
        self.value = va
        self.voz = vo
        self.name = na