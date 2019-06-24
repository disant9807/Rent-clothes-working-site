from django.shortcuts import render
from .models import Tovar, PhotoTovara, VidArendi,Otziv, PhotoOtzyv, Set, Person, VidArendiTovars, TovarPerson, opration
import django.contrib.auth as auth
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import timedelta, datetime, date
from .form import PersonForm



def FindTovars(req):
    find = Find__Tovar(req)
    if req.method == "GET" and len(req.GET)!=0:

        return render(req, "Find_tovars_v2_tovars.html",context={'Tovars':find.GetTovars(True)})
    else:
        return render(req, "Find_tovars_v2.html", context={'Tovars':find.GetTovars(False)})


def tovars(req,id=1):
    kard = KardTovar(req)
    dannye = kard.GetTovar(id=id)
    return render(req, "tovar_v2.html", context= dannye)

def Setssss (req):
    set = Find__Set(req)
    setti= set.GetSet()
    print(setti['form'])
    return render(req, "Find_set_v2.html", context={'Sets':setti['set'],'form':setti['form']})

def edit(req):
    ed = Edit(req)
    rash = Shifr()
    pers =PERSON()
    if req.method == "POST":
            ed.editPers()
            return HttpResponseRedirect('/kabinet')
    else:
        return render(req, "LK_Kabinet_v2_EditPerson.html", context=ed.getPers())


def SetOne(req, id=1):
    print(id)
    setInter = Find__Set(req)
    set = setInter.GetOneSet(id=id)

    return render(req, "tovar-set_v2.html", context={'set':set['set'],'otz':set['otz']})

def auto(req):
    if(req.method=='POST'):
        dannye =  my_view(req)
        return HttpResponseRedirect('/kabinet')
    return render(req, "Autorization_V2.html")

def kabinet(req):
    kabin = LKabinet(req)

    if req.method == 'POST':
        dannye = kabin.getGetStr()
        if req.POST.get('idlike') !=None:
            kabin.VozvratLike()
        if req.POST.get('id') != None:
            kabin.VovratTovar()
        return render(req, "LK_Kabinet_v2.html", context=dannye)
    dannye = kabin.getGetStr()
    return render(req, "LK_Kabinet_v2.html", context=dannye)



def calend(req):
    graf = Graf()
    pers = auth.get_user(req).person

    dan = graf.NormGraf(pers)
    return render(req, "Calendar.html", context={'Grafik':dan})


def my_view(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return True
        else:
            print('провал1')
    else:
        print("провал2")

class Proverka():
    def masslenStr0(self,mass):
        if(len(mass)!=0):
            return mass[0]
        return ''

class TOVAR():
    def add(self, Name, opisanie, priceArenda,VozvratArenda, pricePogon, VozvratPogon, size, Material, Sex, MainPhoto ,Photo=[]):
        tvr = Tovar(name = Name, Opisanie = opisanie, material = Material, DateAdd = datetime.datetime.now(), DateEdit = datetime.datetime.now(),sex = Sex)
        tvr.save()
        Find_Arenda = VidArendi.objects.get(name = 'Аренда')
        Arenda = VidArendiTovars(vidArendi = Find_Arenda, tovar = tvr, stoimost = priceArenda, vozvrat=VozvratArenda)
        Arenda.save()
        Find_pogon = VidArendi.objects.get(name = 'Погонять')
        Pogon = VidArendiTovars(vidArendi= Find_pogon, tovar = tvr, stoimost = pricePogon, vozrat = VozvratPogon)
        Pogon.save()
        for p in Photo:
            Ph = PhotoTovara(photo = p, tovar=tvr, Main= False)
            Ph.save()
        ph = PhotoTovara(photo = MainPhoto, Main = True, tovar = tvr)
        ph.save()

        for s in size:
            si = SizeTovars(tovar = tvr, Size = s)
            si.save()

    def dell(self, id):
        try:
            tvr = Tovar.objects.get(id=idd)
            tvr.delete()
            return True
        except:
            return False


    def GetTovarId(self, idd=0):
        tvr = Tovar.objects.get(id=idd)
        return tvr



    def GetMassTovar(self,str=0, kolich=10, sorting='DateAdd', sortingType=True, name='', Brand='', seaz=[
        'Лето','Зима','Весна','Осень'
    ], sex=[
        'Мужской','Женский','Унисекс'
    ], Size = [
        'S','M','L','XL'
    ], Price = [
        0,999999
    ]):
        tovar = Tovar.objects.all().filter(
            name__startswith=name, brand__name__startswith=Brand, seazon__in=seaz, Sex__in=sex,
            sizetovars__Size__in=Size
        )

        if (sortingType == True):
            tovar = tovar.order_by(sorting).distinct()[str * kolich: (str * kolich) + kolich]
        else:
            tovar = tovar.order_by('-' + sorting).distinct()[str * kolich: (str * kolich) + kolich]

        return tovar

    def edit(self, ID, Name, opisanie, _priceArenda,VozvratArenda, _pricePogon, VozvratPogon, size, Material, Sex, MainPhoto ,Photo=[]):
        tvr = Tovar.object.get(id = ID)
        tvr.name = Name
        tvr.opisanie = opisanie
        priceArenda = tvr.vidarenditovars_set.filter(vidArendi__name="Аренда")[0]
        priceArenda.stoimost = _priceArenda
        priceArenda.Vozvrat = VozvratArenda
        priceArenda.save()
        pricePogon = tvr.vidarenditovars_set.filter(vidArendi__name="Погонять")[0]
        pricePogon.stoimost = _pricePogon
        pricePogon.save()

class SET():

    def GetMassSet(self, str=0, kolich=10, name='', kurtka='', shapka='',shtani='',obyv='',
                   seaz=[
                       'Лето', 'Зима', 'Весна', 'Осень'
                   ],sex=[
                        'Мужской','Женский','Унисекс'
                    ], Size = [
                        'S','M','L','XL'
                    ], Price = [
                        0,999999
                    ], Type = [
                'Куртка', 'Ботинки', 'Штаны', 'Голова'
            ]):

        print(str, kolich, name, kurtka, shapka,shtani,obyv,seaz,sex, Size, Price , Type )
        set = Set.objects.all().filter(Q(tovarssets__tovars__name__startswith =shapka )| Q(tovarssets__tovars__name__startswith =shtani )|Q(tovarssets__tovars__name__startswith =kurtka )|Q(tovarssets__tovars__name__startswith =obyv ),
                                       name__startswith=name, tovarssets__tovars__type__name__in=Type, size__in=Size, seazon__in=seaz)[str * kolich: (str * kolich) + kolich]
        return set

    def GetSet(self, id=0):
        set = Set.objects.filter(id=id)[0]
        return set


    def Add(self):
        pass

    def Dell(self):
        pass

class OTZ():


    def add(self):
        pass

    def GetOtz(self,str=0,kolich=10, photo=False, set=False, id=0):
        otsyvi = Otziv.objects
        if(set ==False):
            otsyvi = otsyvi.all().filter(Tovar__id = id)[str * kolich: (str * kolich)+kolich]
        if(set == True):
            otsyvi = otsyvi.all().filter(Set__id = id)[str * kolich: (str * kolich)+kolich]
        OTZYV = []
        photomas = []
        for ot in otsyvi:
            print(ot)
            photo = ot.photootzyv_set.all();
            for t in photo:
                photomas.append(t.pyth)
            rate = ot.zvezdi
            name = ot.Person.name
            date = ot.date
            text = ot.Opisanie
            OTZYV.append({'name':name, 'rating':rate, 'date':date, 'text':text, 'photo':photomas})
        return OTZYV


    def edit(self):
        pass

    def dell(self):
        pass


    def Edit(self):
        pass

class PERSON:
    def GetPersonid(self,id):
        per = Person.objects.get(id=id);
        return per


    def GetListPerson(self,str=0,sorting='DateAdd', kolich=10, sortingType = True, sex=["Мужской","Женский"],phone=0,VK="",Insta="",Status=['Клиент','Менеджер'],Zamoroz=False,Balananse=[0,99999]):
        per = Person.objects.all().filter(sex__in=sex, phone__startswith=phone, VK__startswith=VK,Insta__startswith=Insta, Status__in=Status, Zamoroz=Zamoroz, Balans__in=Balananse)
        if (sortingType == True):
            tovar = tovar.order_by(sorting)[str * kolich: (str * kolich) + kolich]
        else:
            tovar = tovar.order_by('-' + sorting)[str * kolich: (str * kolich) + kolich]

        return per

    def EditPerson(self,id = None, sex = None, phone = None, Vk = None, Insta = None, Zamoroz = None, Balans = None, Email = None, name = None, Bird = None):
        pers = Person.objects.get(id=id);

        if sex != None:
            if (sex == 'Мужской'):
                sex = 1
            if (sex == "Женский"):
                sex = 0
            pers.sex = sex
        if Vk != None:
            pers.Vk = Vk
        if Insta != None:
            pers.Insta = Insta
        if (Zamoroz != None):
            pers.Zamoroz = Zamoroz

        if (Balans != None):
            pers.Balans = Balans

        if (Email != None):
            pers.Email = Email
        if (name != None):
            pers.name = name
        if (Bird != None):
            pers.Bird = Bird
        pers.save()
        return True

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

class Obrabotka():

    def _Proverka(self, elem, prover):
        pass
    def SpisokTovar(self, tov):
        fotoTov = tov.phototovara_set.all().filter(main=True)
        foto = ''
        if (len(fotoTov) != 0):
            foto = fotoTov[0].photo
        opisanie = tov.Opisanie
        material = tov.Material
        brand = tov.brand
        name = tov.name
        razm = tov.sizetovars_set.all()
        size = []
        for siz in razm:
            size.append(siz.Size)
        return {'photo': foto, 'opisanie': opisanie, 'material': material, 'brand': brand, 'name': name, 'size': size}

    def miniTovar(self,tvr):
        try:
            Name = tvr.name

            pricePogon = tvr.vidarenditovars_set.all().filter(vidArendi__name="Погонять")
            if len(pricePogon) != 0:
                pricePogon = tvr.vidarenditovars_set.filter(vidArendi__name="Погонять")[0].stoimost
            else:
                pricePogon = 0

            priceArenda =  tvr.vidarenditovars_set.all().filter(vidArendi__name="Аренда")
            if len( priceArenda) != 0 :
                priceArenda =  tvr.vidarenditovars_set.filter(vidArendi__name="Аренда")[0].stoimost
            else:
                priceArenda = 0

            razm = tvr.sizetovars_set.all()
            size = []
            for siz in razm:
                size.append(siz.Size)
            photo = tvr.phototovara_set.all()
            Phot = []
            for i in photo:
                Phot.append(i.photo)

            Main = tvr.phototovara_set.all().filter(main=True)
            if len(Main) != 0:
                Main = tvr.phototovara_set.all().filter(main=True)[0].photo
            else: Main = ''

            return  {'name': Name, 'cena': priceArenda, 'size': size , 'foto': '/static/' + Main, 'url':'/tovar/' + str(tvr.id)}
        except:
            return  {'name': "Не удалось загрузить товар", 'cena': 0, 'size': [''] , 'foto': '/static/'}


    def miniSet(self,set):
        Name = set.name
        Cena = set.vidarendisets_set.filter(vidArendi__name="Аренда")[0]
        Foto = set.photosets_set.filter(Main=True)[0]
        opisanie = set.text
        return {'name': Name, 'cena': Cena.stoimost, 'foto': '/static/' + Foto.puth, 'opisanie': opisanie}

    def MaxSet(self, set):
        preobraz = self.SpisokTovar
        def preobrazTovars(ttovarss):
            tovar = []
            for tov in ttovarss:
                tova = preobraz(tov)
                tovar.append(tova)
            return tovar

        tvr = set.tovarssets_set.all()
        tovari = []
        for t in tvr:
            tovari.append(t.tovars)
        tova = preobrazTovars(tovari)
        name = set.name
        stoimostAren = set.vidarendisets_set.all().filter(vidArendi__name='Аренда')[0].stoimost
        stoimostPogon = set.vidarendisets_set.all().filter(vidArendi__name='Погонять')[0].stoimost
        return {'name':name,'pricaArend':stoimostAren,'pricePogon':stoimostPogon,'tovari':tova}

    def MaxTovar(self, tvr):
        try:
            name = tvr.name
            opisanie = tvr.Opisanie
            material = tvr.Material

            pricePogon = tvr.vidarenditovars_set.all().filter(vidArendi__name="Погонять")
            if len(pricePogon) != 0:
                pricePogon = tvr.vidarenditovars_set.filter(vidArendi__name="Погонять")[0].stoimost
            else:
                pricePogon = 0

            priceArenda = tvr.vidarenditovars_set.all().filter(vidArendi__name="Аренда")
            if len(priceArenda) != 0:
                priceArenda = tvr.vidarenditovars_set.filter(vidArendi__name="Аренда")[0].stoimost
            else:
                priceArenda = 0

            razm = tvr.sizetovars_set.all()
            size = []
            for siz in razm:
                size.append(siz.Size)
            photo = tvr.phototovara_set.all()
            Phot = []
            for i in photo:
                Phot.append(i.photo)
            main = tvr.phototovara_set.filter(main=True)

            Main = tvr.phototovara_set.all().filter(main=True)
            if len(Main) != 0:
                Main = tvr.phototovara_set.all().filter(main=True)[0].photo
            else:
                Main = ''

            return {'name': name, 'opisanie': opisanie, 'priceArenda': priceArenda, 'pricePogon': pricePogon, 'size': size,
                    'photo':Phot, 'material': material, 'photMain': "/static/" + Main}
        except:
            return {'name': "Товар не загрузился", 'opisanie': "пусто", 'priceArenda': 0, 'pricePogon': 0,
                    'size': [],
                    'photo': "", 'material': "пусто", 'photMain': ""}

    def MaxPerson(self, person):
        name = person.name
        sex = person.sex

        if sex == True:
            sex = "Мужской"

        if sex == False:
            sex = "Женский"

        email = person.Email
        phone = person.phone
        vk = person.Vk
        insta = person.Insta
        date = person.Bird
        return {'name': name, 'sex': sex, 'email': email, "phone": phone, "vk": vk, "insta": insta, 'datebirth':date}



class Operations():

    def AddOper(self, text, summ, id):
        person = Person.objects.get(id=id)
        operations = opration()
        operations.person = person
        operations.type = text
        operations.summ = summ
        operations.date = datetime.now().date()
        operations.save()

    def GetListOperations(self, text = "", summ = [], str = 0, kolich = 10, sortingType=True, sorting="date"):
        oper = opration()
        oper.objects.all().filter(text__startswith = text, summ__in=summ)

        if (sortingType == True):
            oper = oper.order_by(sorting)[str * kolich: (str * kolich) + kolich]
        else:
            oper = oper.order_by('-' + sorting)[str * kolich: (str * kolich) + kolich]
        return oper



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
            print(ar.znack)
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


class Find__Tovar():
    req = None
    Obr = Obrabotka();

    def __init__(self,req):
        self.req = req

    def GetTovars(self, boolka = False):
        tvr = TOVAR()
        if boolka==True:
            dannye = self.Obrabotka()
            print(dannye)
            return self.Obrabotka_posle(tvr.GetMassTovar(str=dannye['Str'], kolich=10,  name=dannye['name'], Brand=dannye['brand'], seaz=dannye['seaz'], sex=dannye['sex'],
                      Size=dannye['size'],
                      Price=dannye['Price']))
        else:
            return self.Obrabotka_posle(tvr.GetMassTovar())


    def Obrabotka_posle(self, tovar):
        Tovars=[]
        for tvr in tovar:
            tovv = self.Obr.miniTovar(tvr)
            Tovars.append(tovv)
        return Tovars


    def Obrabotka(self):
        rash = Shifr()


        ssezon = rash.ProverZnackMass(ZnackMassDitek(zn='vesna', vl='Весна', pr='on'),
                                      ZnackMassDitek(zn='zima', vl='Зима', pr='on'),
                                      ZnackMassDitek(zn='osen', vl='Осень', pr='on'),
                                      ZnackMassDitek(zn='leto', vl='Лето', pr='on'), slov=self.req.GET)


        ssex = rash.ProverZnackMass(ZnackMassDitek(zn='man', vl='Мужской', pr='on'),
                                    ZnackMassDitek(zn='woman', vl='Женский', pr='on'),
                                    ZnackMassDitek(zn='Uni', vl='Унисекс', pr='on'), slov=self.req.GET)


        ssize = rash.ProverZnackMass(ZnackMassDitek(zn='s', vl='S', pr='on'), ZnackMassDitek(zn='l', vl='L', pr='on'),
                                     ZnackMassDitek(zn='xl', vl='XL', pr='on'), ZnackMassDitek(zn='m', vl='M', pr='on'),
                                     slov=self.req.GET)


        price = rash.ProverkaMass(ShifrDitek(val='mincena',ret=0),ShifrDitek(val='maxcena', ret=99999), Vozvrat=True, slov=self.req.GET, err=[None, ""])
        print("прайс", price)

        All = rash.ProverNone(ShifrDitek(val='Str', ret=0),ShifrDitek(val='name', ret=''), ShifrDitek(val='kurtka', ret=''),
                              ShifrDitek(val='shtani', ret=''), ShifrDitek(val='shapka', ret=''),
                              ShifrDitek(val='obyv', ret=''),ShifrDitek(val='brand', ret=''), Vozvrat=True, slov=self.req.GET)
        All.update({'sex': ssex, 'seaz': ssezon, 'size': ssize, 'Price': price})

        return All



class KardTovar():
    obr = Obrabotka()
    request = None

    def __init__(self, req):
        request = req

    def ObrabotkaPosle(self, Tvr, Otz):
        Vozvrat = self.obr.MaxTovar(Tvr)
        otzyvi = []
        for Ot in Otz:
            VozvratOtz = rash.ProverNone(ShifrDitek('name', 'Нет имени'), ShifrDitek('date', None),
                                         ShifrDitek('text', 'Пусто'), ShifrDitek('rating', 5), slov=Ot, Vozvrat=True)
            otzyvi.append(VozvratOtz)
        Reter = {'Tovar': Vozvrat, 'Otz': otzyvi}
        return Reter

    def GetTovar(self, id):
        tvr = TOVAR()
        otz = OTZ()
        return self.ObrabotkaPosle(tvr.GetTovarId(idd=id), otz.GetOtz(id=id))




class Find__Set():
    Obr = Obrabotka()
    set = SET()
    req = None
    def __init__(self, re):
        self.req = re

    def _preobraz(self, set):
        Vozvrat = []
        obr = Obrabotka()
        for t in set:
            Vozvrat.append(obr.miniSet(t))
        return Vozvrat


    def _Reashifr(self):

        rash = Shifr()


        ssezon = rash.ProverZnackMass( ZnackMassDitek(zn='vesna', vl='Весна', pr='on'),ZnackMassDitek(zn='zima', vl='Зима', pr='on'),ZnackMassDitek(zn='osen', vl='Осень', pr='on'),ZnackMassDitek(zn='leto', vl='Лето', pr='on'), slov=self.req.GET)

        ssex = rash.ProverZnackMass(ZnackMassDitek(zn='man',vl='Мужской', pr='on'), ZnackMassDitek(zn='woman',vl='Женский',pr='on'), ZnackMassDitek(zn='uni', vl='Унисекс',pr='on'), slov=self.req.GET)

        ssize = rash.ProverZnackMass(ZnackMassDitek(zn='s',vl='S',pr='on'), ZnackMassDitek(zn='l',vl='L',pr='on'), ZnackMassDitek(zn='xl',vl='XL',pr='on'), ZnackMassDitek(zn='m',vl='M',pr='on'), slov=self.req.GET)

        price = rash.ProverZnackMass(ZnackMassDitek(vl='mincena',zn='PriceMin', pr='on'), ZnackMassDitek(vl='maxcena',zn='PriceMax', pr='on'), slov=self.req.GET)

        All = rash.ProverNone (ShifrDitek(val='str',ret=0), ShifrDitek(val='name',ret=''),ShifrDitek(val='brand',ret=''), ShifrDitek(val = 'kurtka', ret=''), ShifrDitek(val='shtani',ret=''), ShifrDitek(val='shapka',ret=''),ShifrDitek(val='obyv',ret=''), slov=self.req.GET)
        All.update({'sex':ssex,'seaz':ssezon,'Size':ssize,'Price':price})

        return All

    def _createForm(self):
        rash = Shifr()
        slovar = rash.ProverNone( ShifrDitek(val='name',ret=None), ShifrDitek(val='kurtka',ret=None),ShifrDitek(val='shtani',ret=None),
                                  ShifrDitek(val='shapka',ret=None),ShifrDitek(val='obyv',ret=None),ShifrDitek(val='leto',ret=None),ShifrDitek(val='vesna',ret=None),
                                  ShifrDitek(val='osen', ret=None),ShifrDitek(val='zima', ret=None),ShifrDitek(val='woman', ret=None),ShifrDitek(val='man', ret=None),ShifrDitek(val='Uni', ret=None),
                                  ShifrDitek(val='s', ret=None),ShifrDitek(val='m', ret=None),ShifrDitek(val='l', ret=None),ShifrDitek(val='xl', ret=None),
                                  ShifrDitek(val='PriceMin', ret=0),ShifrDitek(val='PriceMax', ret=99999),Vozvrat=True,slov=self.req.GET)
        return slovar

    def GetSet(self):
        obr = self._Reashifr()
        print(obr)
        sseett = self.set.GetMassSet(name=obr['name'], kurtka=obr['kurtka'], shapka=obr['shapka'], shtani=obr['shtani'], obyv=obr['obyv'],
                                     sex=obr['sex'], seaz=obr['seaz'], Size=obr['Size'], Price=obr['Price'])
        set =  self._preobraz(sseett)
        form = self._createForm()
        return {'set': set, 'form':form}

    def GetOneSet(self,id):
        print(id)
        set = self.set.GetSet(id=id)
        vozvrat = self._preobrazOne(set)
        otz = OTZ()
        voz =  otz.GetOtz(id=id,set=True)
        return {'set':vozvrat, 'otz':voz}

    def _preobrazOne(self, set):
        return self.Obr.MaxSet(set)



class LKabinet:
    req = None
    pers = PERSON()
    Obrab = Obrabotka()
    graf = Graf()
    rash = Shifr()
    def __init__(self,reqev):
       self.req = reqev

    def __reqdelete(self ):
        id = self.req.POST.get('id')
        if id != None:
            return id
        else:
            return 0

    def getGetStr(self ):
        graf = Graf()
        if not auth.get_user(self.req).is_anonymous:
            pers = auth.get_user(self.req).person
            persDwn = self.PersonDwn(pers)
            grafik = graf.GrafikSpisania(pers)
            tovari = self.TovarsPerson(pers)
            like = self.TovarsLike(pers)
            return {'person': persDwn, 'grafik': graf.PreobraGrafik(grafik,2), 'tovari':tovari, 'like':like}
        else:
            return None

    def TovarsPerson(self, pers):
        tovari = pers.tovarperson_set.all()
        masstov = []
        for tov in tovari:
            try:
                voz = self.Obrab.SpisokTovar(tov.VidArendiTovars.tovar)
                size = tov.size
                vidaren = tov.VidArendiTovars.vidArendi.name
                price = tov.VidArendiTovars.stoimost
                id = tov.VidArendiTovars.id
                tovar = tov.VidArendiTovars.tovar.id
                voz.update({'size': size, 'vidarendi': vidaren, 'price': price, 'id': id, 'tovarid':tovar})
                masstov.append(voz)
            except:
                masstov.append({'name':'Не удалось загрузить товар'})

        return masstov

    def TovarsLike(self, pers):
        tovari = pers.likeperson_set.all()
        masstov = []
        for tov in tovari:

            voz = self.Obrab.SpisokTovar(tov.tovar)
            pogon = tov.tovar.vidarenditovars_set.all().filter(vidArendi__name="Погонять")
            if len(pogon)==0:
                pogon = 0
            else:
                pogon = pogon[0].stoimost

            arenda = tov.tovar.vidarenditovars_set.all().filter(vidArendi__name="Аренда")
            if len(arenda) == 0:
                arenda = 0
            else:
                arenda = arenda[0].stoimost
            like = tov.tovar.id
            voz.update({'pogon':pogon, 'arenda':arenda, 'tovarlike':like})
            masstov.append(voz)
        return masstov

    def EditPerson(self, pers):
        form = PersonForm()

    def PersonDwn(self, person):
        return self.Obrab.MaxPerson(person)

    def VozvratLike(self):
        if auth.get_user(self.req).is_authenticated:
            id = self.req.POST.get('idlike')
            perTov = LikePerson.objects.get(tovar_id=id)
            name = perTov.tovar.name
            perTov.delete()

            oper = Operations()
            balans = 0
            if auth.get_user(req).person.Balans != None:
                balans = auth.get_user(req).person.Balans
            if balans != None:
                oper.AddOper('Возврат лайка у вещи ' + name, balans, auth.get_user(req).person.id)
            return True
        return False

    def VovratTovar(self):
        if  auth.get_user(self.req).is_authenticated:
            id = self.__reqdelete()
            perTov = TovarPerson.objects.get(VidArendiTovars_id=id)
            name = perTov.VidArendiTovars.tovar.name
            perTov.delete()

            oper = Operations()
            balans = 0
            if auth.get_user(req).person.Balans != None:
                balans = auth.get_user(req).person.Balans
            if balans != None:
                oper.AddOper('Возврат вещи ' + name , balans, auth.get_user(req).person.id)

            return True
        return False





class Edit:
    req = None
    pers = PERSON()
    Obrab = Obrabotka()
    rash = Shifr()

    def __init__(self, req):
        self.req = req

    def _NllForm(self):
        pers = auth.get_user(self.req).person
        obrabot = self.Obrab.MaxPerson(pers)
        dannye = self.rash.ProverNone(ShifrDitek(val='name', ret='Пусто', ), ShifrDitek(val='sex', ret='Мужской'),
                                      ShifrDitek(val='datebirth', ret=date.today()),
                                      ShifrDitek(val='email', ret='Неизвестно'), ShifrDitek(val='phone', ret=0),
                                      ShifrDitek(val='vk', ret='Пусто'),
                                      ShifrDitek(val='insta', ret='Пусто'), slov=obrabot)

        persForm = PersonForm(initial={'name': dannye['name'], 'sex': dannye['sex'], 'DateAge': dannye['datebirth'],
                                       'Email': dannye['email'],
                                       'Phone': dannye['phone'], 'Vk': dannye['vk'], 'Insta': dannye['insta']})
        return persForm
    def _paramForm(self, slov):

        dannye = self.rash.ProverNone(ShifrDitek(val='name', ret=None),ShifrDitek(val='sex',ret=None), ShifrDitek(val='DateAge', ret=None),
                                      ShifrDitek(val='Email', ret=None),ShifrDitek(val='Phone',ret=None), ShifrDitek(val="VK", ret=""),
                                      ShifrDitek(val='Insta',ret=None), slov=slov, Vozvrat=True)
        return dannye

    def getPers(self):
        if not auth.get_user(self.req).is_anonymous:
                form = self._NllForm()
                return {"form": form}

    def editPers(self):
        try:
            if not auth.get_user(self.req).is_anonymous:
                if self.req.method == "POST":
                    form = PersonForm(req.POST)
                    if form.is_valid():
                        dannye = self._paramForm(form.cleaned_data)
                        itog = self.pers.EditPerson(id=auth.get_user(req).person.id, name=dannye['name'], sex=dannye['sex'],
                                               phone=dannye['Phone'], Vk=dannye['VK'],
                                               Insta=dannye['Insta'], Email=dannye['Email'], Bird=dannye['DateAge'])
                    oper = Operations()
                    balans = 0
                    if auth.get_user(req).person.Balans != None:
                        balans= auth.get_user(req).person.Balans
                    if balans != None:
                        oper.AddOper('Изменеине данных пользователя', balans, auth.get_user(req).person.id)
                    return True
                return False
            return False
        except:
            return False

