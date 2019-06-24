from .models import Tovar, PhotoTovara, VidArendi,Otziv, Set, Person, VidArendiTovars, TovarPerson, LikePerson, AddTovars, Zakaz
import django.contrib.auth as auth
from datetime import timedelta, datetime, date
from .form import Registration, PersonForm, otzyvForm, EditTovarForm,FilterPadiForm,  AddPhotoTovar,SortOperations, FormJournal, FormOtzivi, SortClient, FindClient, SortTovars, SortOtz, SortZakaz, FindZakaz
from .BAZA import PERSON, SET, OTZ,Person,TOVAR, GetOperations, ZAKAZ, OPERATIONS
from .BAZA_bue import Obrabotka
from .grafik import Graf
from .Shifr import Shifr, ShDZN, ShifrDitek, ZnackMassDitek
from .models import OtzForm,EditOtzForm,PersonForm, SizeForm,AddSizeTov, SizeTovars, AddArendaTovars,  AddTovar, EditPerson, ZakaForm, AddZakaz,EditPersonKlient
import secrets
import pytz
from django.contrib.auth.models import User

class Find__Tovar():
    req = None
    Obr = Obrabotka();

    def __init__(self,req):
        self.req = req

    def GetTovars(self, boolka = False, type = None):
        tvr = TOVAR()
        if boolka==True:
            dannye = self.Obrabotka()
            dwn = tvr.GetMassTovar(str=dannye['Str'],dele=[False], nal=[True], sorting= dannye['sort'], sortingType=dannye['on'] , kolich=10,  name=dannye['name'], Brand=dannye['brand'], seaz=dannye['seaz'], sex=dannye['sex'],
                      Size=dannye['size'],
                      Price=dannye['Price'], type=dannye['type'])
            if (dannye['on'] == True):
                dannye['on'] = 'on'
            if (dannye['on'] == False):
                dannye['on'] = 'off'

            return {'Tovars':self.Obrabotka_posle(dwn), 'str': dannye['Str'], 'Sort_kak': dannye['on'], 'Sort':dannye['sort'], 'form':self.req.GET}
        else:
            return {'Tovars':self.Obrabotka_posle(tvr.GetMassTovar(type=type)),'str':'0'}


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
        if len (ssezon) <1:
            ssezon = None

        ssex = rash.ProverZnackMass(ZnackMassDitek(zn='man', vl='Мужской', pr='on'),
                                    ZnackMassDitek(zn='woman', vl='Женский', pr='on'),
                                    ZnackMassDitek(zn='Uni', vl='Унисекс', pr='on'), slov=self.req.GET)

        if len (ssex) <1:
            ssex = None

        ssize = rash.ProverZnackMass(ZnackMassDitek(zn='s', vl='S', pr='on'), ZnackMassDitek(zn='l', vl='L', pr='on'),
                                     ZnackMassDitek(zn='xl', vl='XL', pr='on'), ZnackMassDitek(zn='m', vl='M', pr='on'),
                                     slov=self.req.GET)

        if len (ssize) <1:
            ssize = None

        nal = rash.ProverZnackMass(ZnackMassDitek(zn='nal', vl=True, pr='on'), ZnackMassDitek(zn='nonal', vl=False, pr='on'),
                                   slov=self.req.GET)

        if len(nal) < 1:
            nal = None

        delet = rash.ProverZnackMass(ZnackMassDitek(zn='delete', vl=True, pr='on'),
                                   ZnackMassDitek(zn='nodell', vl=False, pr='on'),
                                   slov=self.req.GET)

        if len(delet) < 1:
            delet = None


        price = rash.ProverkaMass(ShifrDitek(val='mincena',ret=0),ShifrDitek(val='maxcena', ret=999999), Vozvrat=False, slov=self.req.GET, err=[None, ""])

        if len(price) < 2:
            price = None

        All = rash.ProverNone(ShifrDitek(val='Str', ret=0),ShifrDitek(val='name', ret=None), ShifrDitek(val='kurtka', ret=None),
                              ShifrDitek(val='shtani', ret=None), ShifrDitek(val='shapka', ret=None),
                              ShifrDitek(val='obyv', ret=None),ShifrDitek(val='brand', ret=None), Vozvrat=True, slov=self.req.GET)

        on = self.req.GET.get('Sort_kak','on')
        if on == 'on':
            on = True
        if on == 'off':
            on = False

        type = self.req.GET.get('type',None)
        if type == '':
            type = None

        sort = self.req.GET.get('Sort','DateAdd')
        if (sort !='DateAdd' and sort !='arenda' and sort !='like' and sort !='stoimost'):
            sort =='DateAdd'

        All.update({'sex': ssex, 'seaz': ssezon, 'size': ssize, 'Price': price, 'on':on,'sort':sort,'type':type, 'nal':nal,'delet':delet})


        if (isinstance(All['Str'], str)):
            if(All['Str'].isdigit()):
                All['Str'] = int(All['Str'])
            else:
                All['Str'] = 0
        else:
            if(isinstance(All['Str'], int) == False):
                All['Str'] = 0
        print(All['Str'])
        return All

    def GetTovarsAdm(self):
        tvr = TOVAR()
        dannye = self.Obrabotka()

        admDann = self.__VidAdmin()

        dannye.update(admDann)

        stra = self.req.GET.get('str', 1)

        if (isinstance(stra, str)):
            if (stra.isdigit()):
                stra = int(stra)
            else:
                stra = 1
        else:
            if (isinstance(stra, int) == False):
                stra = 1

        if stra < 1:
            stra = 1

        kolich = self.req.GET.get('kolich', 10)

        if (isinstance(kolich, str)):
            if (kolich.isdigit()):
                kolich = int(kolich)
            else:
                kolich = 10
        else:
            if (isinstance(kolich, int) == False):
                kolich = 10

        if kolich < 1:
            kolich = 1

        sorting = self.req.GET.get('sort', 'DateAdd')

        sortingType = self.req.GET.get('sortingType', None)
        if sortingType == None:
            sortingType = False
        if sortingType == 'on':
            sortingType = True

        print(sortingType)

        dwn = tvr.GetMassTovar(str=stra-1, nal=dannye['nal'], dele=dannye['delet'],  kolich=kolich,
                               name=dannye['name'], Brand=dannye['brand'], seaz=dannye['seaz'], sex=dannye['sex'],
                               Size=dannye['size'],
                               Price=dannye['Price'], vid=dannye['vid'],sorting= sorting, sortingType=sortingType)




        if (dannye['on'] == True):
            dannye['on'] = 'on'
        if (dannye['on'] == False):
            dannye['on'] = 'off'


        formsort = SortTovars(self.req.GET)


        return {'Tovars': self.__ObrPosleAdm(dwn),'formsort':formsort, 'str': dannye['Str'], 'Sort_kak': dannye['on'],
                'Sort': dannye['sort'], 'form': self.req.GET, 'zapros':self.req.GET}

    def __VidAdmin(self):
        rash = Shifr()
        dann = rash.ProverZnackMass(ZnackMassDitek(zn='Kurtka', vl='Куртки', pr='on'), ZnackMassDitek(zn='Puhovik', vl='Пуховики', pr='on'),
                                    ZnackMassDitek(zn='Palto', vl='Пальто', pr='on'), ZnackMassDitek(zn='Vetrovka', vl='Ветровки', pr='on'),
                                    ZnackMassDitek(zn='Hudi', vl='Худи', pr='on'), ZnackMassDitek(zn='Jaket', vl='Жакеты', pr='on'),ZnackMassDitek(zn='Maika', vl='Майки', pr='on'),
                                    ZnackMassDitek(zn='Maika', vl='Майка', pr='on'), ZnackMassDitek(zn='Rubashki', vl='Рубашки', pr='on'),
                                    ZnackMassDitek(zn='Jeans', vl='Джинсы', pr='on'), ZnackMassDitek(zn='Triko', vl='Трико', pr='on'),
                                        ZnackMassDitek(zn='Djoggers', vl='Джоггеры', pr='on'),  ZnackMassDitek(zn='Classic', vl='Классика', pr='on'),
                                    ZnackMassDitek(zn='Krossy', vl='Кроссовки ', pr='on'),  ZnackMassDitek(zn='Kedi', vl='Кеды', pr='on'),
                                    ZnackMassDitek(zn='Botinki', vl='Ботинки', pr='on'),  ZnackMassDitek(zn='Tufli', vl='Туфли', pr='on'),slov=self.req.GET);

        if len(dann) <1:
            dann = None

        priceAren = rash.ProverkaMass(ShifrDitek(val='mincenaAren', ret=0), ShifrDitek(val='maxcenaAren', ret=99999), Vozvrat=True,
                                  slov=self.req.GET, err=[None, ""])
        pricePogon = rash.ProverkaMass(ShifrDitek(val='mincenaPogon',ret=0),ShifrDitek(val='maxcenaPogon', ret=99999), Vozvrat=True, slov=self.req.GET, err=[None, ""])

        return {'vid':dann, 'dann':dann, 'priceAren': priceAren, 'pricePogon':pricePogon}

    def __ObrPosleAdm(self, tovar):
        Tovars = []
        for tvr in tovar:
            tovv = self.Obr.TovarAdminMini(tvr)
            Tovars.append(tovv)
        return Tovars


class Main:
    req = None;
    Obr = Obrabotka();

    def __init__(self,req):
        self.req = req

    def GetTovar(self):
        tvr = TOVAR()

        dwn = tvr.GetMassTovar(str=0, dele=[False], sorting='arenda', sortingType=False,
                               kolich=10)

        return {'Tovars': self.Obrabotka_posle(dwn)}

    def Obrabotka_posle(self, tovar):
        Tovars=[]
        for tvr in tovar:
            tovv = self.Obr.miniTovar(tvr)
            Tovars.append(tovv)
        return Tovars

class KardTovar():
    obr = Obrabotka()
    request = None
    rash = Shifr()

    def __init__(self, req):
        self.request = req

    def ObrabotkaPosle(self, Tvr):
        Vozvrat = self.obr.TovarAdminMax(Tvr)
        otz = Tvr.otziv_set.filter(Status="Принят")

        otzivi = []

        for ot in otz:
            otzivi.append(self.obr.OtziviMax(ot))

        return {'Tovar':Vozvrat, 'Otzivi':otzivi}

    def GetTovar(self, id):
        tvr = TOVAR()

        return self.ObrabotkaPosle(tvr.GetTovarId(idd=id))

    def ObraborkaRent(self,id):

        tovar = id
        rent = self.request.POST.get('arenda', None)
        size = self.request.POST.get('size', None)

        kolich = int(self.request.POST.get('kolich',1))


        korz = self.request.session.get('Korzina',None)
        if korz == None:
            self.request.session['Korzina'] = []

        if isinstance(korz, list) == False:
            self.request.session['Korzina'] = []

        if (tovar != None, rent != None, size != None):
            mass = self.request.session['Korzina']
            nomer = secrets.token_hex(2)
            mass.append({'nomer':nomer,'tovar': tovar, 'rent': rent, 'size': size, 'kolich':kolich})
            self.request.session['Korzina'] = mass

        return True






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

        Price = rash.ProverNone(ShifrDitek(val='PriceMin',ret=0), ShifrDitek(val='PriceMax',ret=99999), Vozvrat=True)
        price = [Price['PriceMin'], Price['PriceMax']]

        All = rash.ProverNone (ShifrDitek(val='Str',ret=0), ShifrDitek(val='name',ret=''),ShifrDitek(val='brand',ret=''), ShifrDitek(val = 'kurtka', ret=''), ShifrDitek(val='shtani',ret=''), ShifrDitek(val='shapka',ret=''),ShifrDitek(val='obyv',ret=''), slov=self.req.GET)

        on = self.req.GET.get('Sort_kak', 'on')
        if on == 'on':
            on = True
        if on == 'off':
            on = False

        sort = self.req.GET.get('Sort', 'DateAdd')
        if (sort != 'DateAdd' and sort != 'arenda' and sort != 'like' and sort != 'stoimost'):
            sort == 'DateAdd'

        if (isinstance(All['Str'], str)):
            if(All['Str'].isdigit()):
                All['Str'] = int(All['Str'])
            else:
                All['Str'] = 0
        else:
            if(isinstance(All['Str'], int) == False):
                All['Str'] = 0

        All.update({'sex':ssex,'seaz':ssezon,'Size':ssize,'Price':price, 'Sort':sort, 'Sort_kak':on})

        return All

    def _createForm(self):
        rash = Shifr()
        slovar = rash.ProverNone( ShifrDitek(val='name',ret=None), ShifrDitek(val='kurtka',ret=None),ShifrDitek(val='shtani',ret=None),
                                  ShifrDitek(val='shapka',ret=None),ShifrDitek(val='obyv',ret=None),ShifrDitek(val='leto',ret=None),ShifrDitek(val='vesna',ret=None),
                                  ShifrDitek(val='osen', ret=None),ShifrDitek(val='zima', ret=None),ShifrDitek(val='woman', ret=None),ShifrDitek(val='man', ret=None),ShifrDitek(val='uni', ret=None),
                                  ShifrDitek(val='s', ret=None),ShifrDitek(val='m', ret=None),ShifrDitek(val='l', ret=None),ShifrDitek(val='xl', ret=None),
                                  ShifrDitek(val='PriceMin', ret=0),ShifrDitek(val='PriceMax', ret=99999), ShifrDitek(val='Str',ret=0), ShifrDitek(val='Sort', ret='DateAdd'), ShifrDitek(val='Sort_kak', ret='off'), Vozvrat=True,slov=self.req.GET)
        return slovar

    def GetSet(self):
        obr = self._Reashifr()
        sseett = self.set.GetMassSet(name=obr['name'], kurtka=obr['kurtka'], shapka=obr['shapka'], shtani=obr['shtani'], obyv=obr['obyv'],
                                     sex=obr['sex'], seaz=obr['seaz'], Size=obr['Size'], Price=obr['Price'], str= obr['Str'], sorting=obr['Sort'], sortingType=obr['Sort_kak'])
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

    def LKzakazi(self, pers):
        zaka = pers.zakaz_set.filter(status=True)

        massZak = []

        for zakaz in zaka:
            tovars = zakaz.tovarszakaz_set.all()

            dann = {'date': zakaz.date, 'nomer': zakaz.nomer, 'id': zakaz.id,
                    'status': zakaz.status, 'vid':zakaz.vidann}

            Tovari = []

            for tov in tovars:
                normrent = self.Obrab.NormVidArendi(tov.tovar)
                normsize = self.Obrab.NormTovarsSize(tov.size)
                normtovar = self.Obrab.NormTovar(tov.tovar.tovar)

                tovari = {}
                tovari.update(normrent)
                tovari.update(normsize)
                tovari.update(normtovar)

                Tovari.append(tovari)

            massZak.append({'zakaz': dann, 'tovars': Tovari})

        return massZak

    def getGetStr(self ):
        graf = Graf()
        if not auth.get_user(self.req).is_anonymous:
            pers = auth.get_user(self.req).person
            persDwn = self.PersonDwn(pers)
            grafik = graf.GrafikSpisania(pers)
            tovari = self.TovarsPerson(pers)
            zaki = self.LKzakazi(pers)

            adm= None
            if auth.get_user(self.req).person.Status=="Админ":
                adm = True

            return {'person': persDwn, 'grafik': graf.PreobraGrafik(grafik,2), 'tovari':tovari, 'zakazi':zaki, 'adminka':adm}
        else:
            return None

    def TovarsPerson(self, pers):
        tovari = pers.tovarperson_set.all()
        masstov = []
        for tov in tovari:
            normrent = self.Obrab.NormVidArendi(tov.VidArendiTovars)
            normsize = {'size': tov.size}
            normtovar = self.Obrab.NormTovar(tov.VidArendiTovars.tovar)

            tovari = {}
            tovari.update(normrent)
            tovari.update(normsize)
            tovari.update(normtovar)

            masstov.append(tovari)



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
            if auth.get_user(self.req).person.Balans != None:
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
            if auth.get_user(self.req).person.Balans != None:
                balans = auth.get_user(self.req).person.Balans
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
            if auth.get_user(self.req).is_authenticated:
                    pers =  auth.get_user(self.req).person
                    form = EditPersonKlient(instance=pers)
                    return {"form": form}

    def editPers(self):
        try:
            if auth.get_user(self.req).is_authenticated:
                if not auth.get_user(self.req).is_anonymous:
                    if self.req.method == "POST":
                        pers = auth.get_user(self.req).person
                        form = EditPersonKlient(self.req.POST,instance=pers)
                        if form.is_valid():
                            form.save()
                        return True
                    return False
            return False
        except:
            return False




class NewOtzyv():
    req = None;
    tvr = TOVAR()
    otz = OTZ()
    obr = Obrabotka()
    rash = Shifr()

    kard = None
    def __init__(self, req):
        self.kard = KardTovar(req)
        self.req = req

    def ProverkaPerson(self, id, Tovar):
        pers = PERSON();
        proverka = pers.ProverkaPerson(id, Tovar)
        return proverka

    def getOtz(self, id):
        try:
            if  auth.get_user(self.req).is_authenticated:
                if not auth.get_user(self.req).is_anonymous:
                    if self.ProverkaPerson(auth.get_user(self.req).person.id, id) == True:
                            form = otzyvForm()
                            tovar = self.kard.GetTovar(id)
                            return {"form":form, 'tovar':tovar }
                    return None
        except:
            return None

    def editPers(self,id):
        try:
            if auth.get_user(self.req).is_authenticated:
                if self.ProverkaPerson(auth.get_user(self.req).person.id, id) == True:
                    if self.req.method == "POST":
                        form = otzyvForm(self.req.POST)
                        if form.is_valid():
                            dannye = form.cleaned_data

                            idPers = auth.get_user(self.req).person.id
                            tovarid = id
                            text = dannye['text']
                            rating = dannye['rating']

                            itog = self.otz.add(text, idPers, rating, tovarid)
                        return True
                return False
            return False
        except:
            return False



    def ObrabotkaPosle(self, Tvr, Otz):
        Vozvrat = self.obr.MaxTovar(Tvr)
        otzyvi = []
        for Ot in Otz:
            VozvratOtz = self.rash.ProverNone(ShifrDitek('name', 'Нет имени'), ShifrDitek('date', None),
                                         ShifrDitek('text', 'Пусто'), ShifrDitek('rating', 5), slov=Ot, Vozvrat=True)
            otzyvi.append(VozvratOtz)
        pogon = 0
        tvrp = Tvr.vidarenditovars_set.filter(vidArendi__name="Погонять")
        if (len(tvrp) > 0):
            pogon = tvrp[0].id

        arenda = 0
        tvra = Tvr.vidarenditovars_set.filter(vidArendi__name="Аренда")

        if (len(tvra) > 0):
            arenda = tvra[0].id

        id = Tvr.id
        Vozvrat.update({'Pogon': pogon, 'Arenda': arenda, 'id': id})
        Reter = {'Tovar': Vozvrat, 'Otz': otzyvi}
        return Reter




class Korrrzz:
    req = None
    Obr = Obrabotka()
    Tovar = TOVAR()
    zak = ZAKAZ()
    def __init__(self, req):
        self.req = req


    def DellSize(self, _nomer):
        try:
            korzina = self.req.session['Korzina']
            if korzina != None:
                for tov in range(len(korzina)):
                    nom = korzina[tov].get('nomer',None)
                    print(nom)
                    if nom != None:
                        if nom == _nomer:
                            del korzina[tov]
                            self.req.session['Korzina'] = korzina
                            return True

                return False
            return False
        except:
            return False


    def editkolich (self,_nomer,bool):
        try:
            korzina = self.req.session['Korzina']
            if korzina != None:
                for tov in range(len(korzina)):
                    nom = korzina[tov].get('nomer',None)
                    if nom !=None:
                        if nom == _nomer:
                            kolich = korzina[tov]['kolich']
                            kolich = int(kolich)
                            if bool == True:
                                kolich = kolich + 1
                            else:
                                if kolich > 1:
                                    kolich = kolich - 1
                            korzina[tov]['kolich'] = kolich
                            self.req.session['Korzina'] = korzina
                            return True

                return False
            return False
        except:
            return False


    def GetDannye(self):
        try:

            korzina = self.req.session['Korzina']
            print(korzina)
            mass = []

            summ = 0;

            if korzina != None:
                for tov in korzina:

                    tovar = tov['tovar']
                    if isinstance(tovar,int) == False:
                        if tovar.isdigit == True:
                            tovar = int(tovar)

                    size = tov['size']
                    if isinstance(size,int) == False:
                        if size.isdigit == True:
                            size = int(size)

                    rent = tov['rent']
                    if isinstance(rent,int) == False:
                        if rent.isdigit == True:
                            rent = int(rent)

                    Kolich  = int(tov.get('kolich',1))
                    Tovar = self.Tovar.GetTovarId(idd=tovar)
                    Size = SizeTovars.objects.get(id=size)
                    Rent = VidArendiTovars.objects.get(id=rent)

                    nomer = tov.get('nomer',None)

                    obj = self.Obr.Obrkorzina(Tovar,Rent,Size,Kolich,nomer)
                    mass.append(obj)

                    summ = summ + (Rent.stoimost * Kolich)


            return {"tovars": mass, 'sum':summ}
        except:
            return {}

    def AddZakaz(self):
        zakaz = Zakazi(self.req)
        korzina = self.req.session.get('Korzina',None)

        if not auth.get_user(self.req).is_anonymous:
            if auth.get_user(self.req).is_authenticated:
                id = auth.get_user(self.req).person.id
                if korzina !=None and id !=None:
                    itog = self.zak.AddZakaz(idpers=id, date=datetime.now())
                    print(itog)
                    if itog != False:
                        for tov in korzina:
                            tovar = tov.get('tovar')
                            if isinstance(tovar, int) == False:
                                if tovar.isdigit == True:
                                    tovar = int(tovar)

                            size = tov.get('size')
                            if isinstance(size, int) == False:
                                if size.isdigit == True:
                                    size = int(size)

                            rent = tov.get('rent')
                            if isinstance(rent, int) == False:
                                if rent.isdigit == True:
                                    rent = int(rent)

                            Kolich = int(tov.get('kolich', 1))

                            if rent != None and size !=None and rent !=None:
                                for koli in range(Kolich):
                                    result = self.zak.AddTovars(itog,rent,size)
                                    if result != False:
                                        self.req.session['Korzina'] = []
                                        return itog
                                    else:
                                        return False
                                return False
        return  False



class KardTovarFull:
    req = None
    tovar = TOVAR()
    obr = Obrabotka()

    def __init__(self, req):
        self.req = req

    def DellTovar(self,id, bool):
        try:
            tovar = self.tovar.GetTovarId(id)
            tovar.Del = bool
            tovar.save()
            return True
        except:
            return False

    def GetTovar(self, id):
        tovar = self.tovar.GetTovarId(id)
        dannye = self.obr.TovarAdminMax(tovar)
        form = SizeForm(id)
        formAdd = AddSizeTov(id)
        formRent = AddArendaTovars(id)
        dannye.update({'form':form, 'formAdd':formAdd, "formRent":formRent})
        return dannye

    def AddSize(self, id):
        pers = auth.get_user(self.req).person

        dannye = self.req.POST.copy()
        dannye.__setitem__('tovar',str(id))
        dannye.__setitem__('client', str(pers.id))

        dannye.__setitem__('PlusMinus', True)
        print(dannye)

        form = SizeForm(id,dannye)
        if form.is_valid():
            form.save()
            return True
        return False

    def AddSizeTovar(self,id):
        print(self.req.POST)
        dannye = self.req.POST.copy()
        dannye.__setitem__('Tovar', str(id))
        dannye.__setitem__('nalichie', '0')
        form = AddSizeTov(None,dannye)
        if form.is_valid():
            form.save()
            return True
        return False

    def AddRent(self,id):
        dannye = self.req.POST.copy()
        dannye.__setitem__('tovar', str(id))
        form = AddArendaTovars(None,dannye)
        if form.is_valid():
            form.save()
            return True
        return False

    def SaveAddSize(self,id):
        tovar = self.tovar.GetTovarId(id)

        dannye = self.req.POST.copy()
        dannye.__setitem__('nalichie', False)
        form = SizeForm(dannye)
        if form.is_valid():
            form.save()
            return True
        return False

    def DellSize (self,id):
        delsize = SizeTovars.objects.get(id=id)
        dele = delsize.addtovars_set.all()
        if len(dele) < 1:
            delsize.delete()
            return True
        return False

    def DellRent(self,id):
        try:
            rent = VidArendiTovars.objects.get(id=id)
            rent.delete()
            return True
        except:
            return False

    def NallSize (self,id, bool):
        delsize = SizeTovars.objects.get(id=id)
        if bool == True:
            koll = 0
            tranz = delsize.addtovars_set.all()
            for z in tranz:
                koll = koll + z.count
            if koll > 0:
                delsize.nalichie = True
                delsize.save()
                return True
            return False
        if bool == False:
            delsize.nalichie = False
            delsize.save()
            return True
        return False




class AddFile:
    def handle_uploaded_file(self,f, name):
        print(name)
        with open(name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

class EditTovar:
    req = None
    tovar = TOVAR()
    obr = Obrabotka()
    add = AddFile()
    rash = Shifr()

    addfile = AddFile()

    def __init__(self, req):
        self.req = req

    def addTovar(self):
        forms = EditTovarForm()
        return {'form':forms}

    def ProverkaAdd(self):
        formm = EditTovarForm(self.req.POST,self.req.FILES)

        if formm.is_valid():
            element = formm.process()

            add = self.tovar.add(name=element['name'], opisanie=element["opisanie"], material=element["material"], sex=element["sex"], brand=element['brand'], type = element['vidtovars'], seaz=element['seaz'],
                                 MainPhoto=self.req.FILES['main'])
            return add
        return False

    def Nalichie(self, id, bool):
        try:
            tov = self.tovar.GetTovarId(id)
            itog = self.obr.TovarNalichie(tov,bool)
            return True
        except:
            return False


    def EditForm(self, id):
        dannye = self.tovar.GetTovarId(id)
        dannyeObr = self.obr.TovarAdminMax(dannye)


        forma =  AddTovar(instance=dannye)
        return {'form':forma, 'id':id}


    def AddEditForm(self,id):
        try:
            tovar = self.tovar.GetTovarId(id)

            dannye = self.req.POST.copy()
            dannye.__setitem__('DateAdd', datetime.now())
            dannye.__setitem__('DateEdit', datetime.now())

            forma = AddTovar(dannye, instance=tovar)
            if forma.is_valid():
                forma.save()
                return True
            return False
        except:
            return False

    def PhotoTovar(self,id):
        tovar = self.tovar.GetTovarId(id)
        photki = self.obr.PhotoTovara(tovar)
        form = AddPhotoTovar()
        return {"photo": photki, 'form': form, 'id': id}




    def AddPhotoTovar(self, files,id,bool):
        itog = self.tovar.UploadPhoto(files, id, bool)
        return itog


    def MainPhoto(self, id_photo, id_tovara):
        try:
            photos = PhotoTovara.objects.filter(tovar_id=id_tovara)
            itog = False
            for ph in photos:
                if ph.id == id_photo:
                    ph.main = True
                    itog = True
                else:
                    ph.main = False
                ph.save()
            return itog
        except:
            return False

    def DellPhoto(self, id, bool):
        try:

            pohot = PhotoTovara.objects.get(id=id)
            if bool:
                pohot.delete = True
            else:
                pohot.delete = False
            pohot.save()

            return True
        except:
            return False


class adminClident:
    req = None
    person = PERSON()
    obr = Obrabotka()
    rash = Shifr()
    def __init__(self, req):
        self.req = req

    def GetClient(self):

        paramets = self.ObrParam()
        stranica = paramets.get('str', 1) - 1
        dannye = self.person.GetListPerson(str=stranica, kolich=paramets.get('kolich',10), sorting=paramets.get('sorting','bird'), sortingType=paramets.get('sortingType',True),  sex = paramets['sex'],name= paramets.get('name',None), phone = paramets['phone'], Zamoroz= paramets['type'], Balananse=paramets['balance'])

        massPers = []
        for dann in dannye:
            personi = self.obr.AdmMaxPerson(dann)
            massPers.append(personi)

        form = SortClient(self.req.GET)

        formMain = FindClient(self.req.GET)

        return {'person': massPers,'mmaiinn': formMain, 'formsort':form, "zapros":self.req.GET}

    def ObrParam(self):
        slov = self.req.GET
        slovar = self.rash.ProverNone(ShifrDitek(val='name', ret=None), ShifrDitek(val='phone', ret=None), Vozvrat=True, slov=slov)

        age = self.rash.ProverkaMass(ShifrDitek(val='agemin', ret=0), ShifrDitek(val='agemax', ret=999999), Vozvrat=True,
                          slov=slov, err=[None, ""])

        balance = self.rash.ProverkaMass(ShifrDitek(val='minprice', ret=0), ShifrDitek(val='maxprice', ret=999999), Vozvrat=True,
                          slov=slov, err=[None, ""])


        schmot = self.rash.ProverkaMass(ShifrDitek(val='minvesh', ret=0), ShifrDitek(val='maxvesh', ret=999999), Vozvrat=True,
                          slov=slov, err=[None, ""])


        monthprice = self.rash.ProverkaMass(ShifrDitek(val='monmin', ret=0), ShifrDitek(val='monma', ret=999999), Vozvrat=True,
                          slov=slov, err=[None, ""])


        sex = self.rash.ProverZnackMass( ZnackMassDitek(zn='man', vl=True, pr='on'),ZnackMassDitek(zn='woman', vl=False, pr='on'), slov=slov)

        if len(sex) <1:
            sex = None

        type = self.rash.ProverZnackMass(ZnackMassDitek(zn='moroz', vl=True, pr='on'),
                                   ZnackMassDitek(zn='razmoroz', vl=False, pr='on'), slov=slov)
        if len(type) < 1:
            type = None

        sorting = self.req.GET.get('sort','bird')

        sortingType = self.req.GET.get('sortingType',None)
        if sortingType == None:
            sortingType = False
        if sortingType == 'on':
            sortingType = True

        stra = self.req.GET.get('str',1)

        if (isinstance(stra, str)):
            if (stra.isdigit()):
                stra = int(stra)
            else:
                stra = 1
        else:
            if (isinstance(stra, int) == False):
                stra = 1

        if stra <1:
            stra = 1

        kolich = self.req.GET.get('kolich',10)

        if (isinstance(kolich, str)):
            if (kolich.isdigit()):
                kolich = int(kolich)
            else:
                kolich = 10
        else:
            if (isinstance(kolich, int) == False):
                kolich = 10

        if kolich <1:
            kolich = 1

        slovar.update({'age':age,'str':stra,'kolich':kolich,'sorting':sorting,'sortingType':sortingType,'balance':balance, "schmot":schmot, 'monthprice':monthprice,'sex':sex,'type':type})
        return slovar

class adminikardclient:
    req = None
    person = PERSON()
    obr = Obrabotka()
    tovar = TOVAR()
    def __init__(self, req):
        self.req = req

    def GetKardClientMax(self,id):
        findeclient = self.person.GetPersonid(id)
        maxPerson = self.obr.AdmMaxPerson(findeclient)
        return maxPerson

    def Zamorozka(self, id, boolka):
        client = self.person.GetPersonid(id)
        itog = self.obr.AdmPersZamoroz(client,boolka)
        return itog

    def Balance(self, id):

        def ObrBalace():
            money = self.req.POST.get("money","0")
            if money.isdigit():
                return int(money)
            return 0
        money = ObrBalace()
        client = self.person.GetPersonid(id)
        itog = self.obr.AdmBalance(client,money)
        return itog

    def EditPassword(self,id):
        def ObrPass():
            passw = self.req.POST.get("password")
            return passw
        passw = ObrPass()
        client = self.person.GetPersonid(id)
        itog = self.obr.AdmPass(client,passw)
        return itog

    def EditPerson(self, id):

        pers = Person.objects.get(id=id)
        form = EditPerson(instance=pers)

        return {'form':form}


    def AddTovar(self,id, idtovar):
        client = self.person.GetPersonid(id)
        tovar = self.tovar.GetTovarId(idtovar)
        itog = self.obr.AdmAddTovar(client,tovar)
        return itog
    def EditPerson(self,id):
        client = self.person.GetPersonid(id)
        form = PersonForm(instance=client)
        return {"form":form}

    def SavePerson(self,id):
        client = self.person.GetPersonid(id)
        form = PersonForm(self.req.POST,instance=client)
        if form.is_valid():
            form.save()
            return True
        return False


class EditPassClient:
    req = None
    obr = Obrabotka()

    def __init__(self, req):
        self.req = req

    def EditPass(self, password):
        if not auth.get_user(self.req).is_anonymous:
            if auth.get_user(self.req).is_authenticated:
                pers = auth.get_user(self.req).person
                itog = self.obr.AdmPass(pers,password)
                return itog
        return False

class adminOtzivi:
    req = None
    otz = OTZ()
    obr = Obrabotka()
    rash = Shifr()
    tovar = TOVAR()
    def __init__(self, req):
        self.req = req

    def GetOtz(self):

        dann = self.FilterOtziyvi()


        if dann['str'] > 0:
            dann['str'] = dann['str']-1

        spisok = self.otz.GetOtz(value=True, str=dann['str'], kolich=dann.get('kolich',10), delete=dann.get('delete',None), sorting=dann['Sort'], sortingType=dann["Sort_kak"], rating=dann['rating'], status=dann['status'], personName=dann['Client'], tovarName=dann['Vesh'])

        form = FormOtzivi(self.req.GET)

        formsort = SortOtz(self.req.GET)

        return {'otzivi':spisok, 'form': form, 'formsort':formsort, 'zapros':self.req.GET}

    def OneOtz(self, id):
        otz = self.otz.GetOneOtz(id)
        dann = self.obr.OtziviMax(otz)
        return dann

    def DeleteOtz(self, id, bool):
        otz = self.otz.GetOneOtz(id)
        delete = self.obr.DelOtz(otz,bool)
        return delete

    def Razresh(self,id, bool):
        otz = self.otz.GetOneOtz(id)
        izm = self.obr.Razresh(otz,bool)
        return izm

    def OtvetOtz(self, id, text):
        otz = self.otz.GetOneOtz(id)
        izm = self.obr.OtvetOtz(otz,text)
        return izm

    def DellOtvetOtz(self, id):
        otz = self.otz.GetOneOtz(id)
        izm = self.obr.OtvetOtz(otz,'',bool=True)
        return izm

    def FilterOtziyvi(self):



        dannye = self.rash.ProverNone(ShifrDitek(val='Client', ret=None), ShifrDitek(val='Vesh', ret=None), Vozvrat=True,slov=self.req.GET)
        massStatus = self.rash.ProverZnackMass(ZnackMassDitek(zn='ok',vl="Принят",pr='on'), ZnackMassDitek(zn='no',vl="Отклонен",pr='on'), ZnackMassDitek(zn='wtf',vl="Смотр",pr='on'),slov=self.req.GET)
        if len(massStatus) <1:
            massStatus=None

        rating = self.rash.ProverZnackMass(ZnackMassDitek(zn='one',vl=1,pr='on'), ZnackMassDitek(zn='two',vl=2,pr='on'), ZnackMassDitek(zn='three',vl=3,pr='on'), ZnackMassDitek(zn='fo',vl=4,pr='on'),
                                           ZnackMassDitek(zn='five', vl=5, pr='on'), slov=self.req.GET)


        delete = self.req.GET.get('delete',None)
        if delete != None:
            if delete == 'on':
                delete = True
            else:
                delete = False


        if len(rating) <1:
            rating=None

        sorting = self.req.GET.get('sort', 'date')

        sortingType = self.req.GET.get('sortingType', None)
        if sortingType == None:
            sortingType = False
        if sortingType == 'on':
            sortingType = True

        stra = self.req.GET.get('str', 1)

        if (isinstance(stra, str)):
            if (stra.isdigit()):
                stra = int(stra)
            else:
                stra = 1
        else:
            if (isinstance(stra, int) == False):
                stra = 1

        if stra < 1:
            stra = 1

        kolich = self.req.GET.get('kolich', 10)

        if (isinstance(kolich, str)):
            if (kolich.isdigit()):
                kolich = int(kolich)
            else:
                kolich = 10
        else:
            if (isinstance(kolich, int) == False):
                kolich = 10

        if kolich < 1:
            kolich = 1




        dannye.update({'rating':rating,'delete':delete, 'status':massStatus, 'Sort':sorting, 'str':stra, 'kolich':kolich , 'Sort_kak':sortingType})

        return dannye

    def addOtz(self, id):

        tovar = self.tovar.GetTovarId(id)
        form = OtzForm(initial={'Tovar':tovar, "Status":'Принят'})
        tovar = self.obr.TovarAdminMini(tovar)
        return {'form':form, 'Tovar':tovar}

    def saveOtz(self):
        form = OtzForm(self.req.POST)
        if form.is_valid():
                form.save()
                return  True
        return False

    def editOtz(self,id):
        otz = self.otz.GetOneOtz(id)
        tovar = None
        person = None
        if otz !=None:
            tovar = self.obr.TovarAdminMini(otz.Tovar)
            person = self.obr.AdmMini(otz.Person)
        form = EditOtzForm(instance=otz)
        return {'form':form,'Tovar':tovar, 'Person':person, 'id':otz.id}

    def saveEditOtz(self,id):
        otz = self.otz.GetOneOtz(id)
        form = EditOtzForm(self.req.POST,instance=otz)
        if form.is_valid():
                form.save()
                return  True
        return False


class journal():
    journ = GetOperations()
    req = None


    def __init__(self, req):
        self.req = req

    def GetTranz(self):
        dannye = self.ObrForms()


        itog = self.journ.GetMassOperations(value=True,str=int(dannye.get('str',1)),kolich=int(dannye.get('kolich',10)), personName=dannye.get('person',None),tovarName=dannye.get('tovar',None),date=dannye.get('date',None),
                                            sizeName=dannye.get('size',None),count=dannye.get('count',None),PlusMinus=dannye.get('plusminus',None))
        form = FormJournal(self.req.GET)

        formMain = FindClient(self.req.GET)
        return {"Tovars":itog,"form":form}


    def ObrForms(self):
        rash = Shifr()


        plusminus = rash.ProverZnackMass(ZnackMassDitek(zn='plus', vl=True, pr='on'),
                                    ZnackMassDitek(zn='minus', vl=False, pr='on'), slov=self.req.GET)

        if len(plusminus) < 1:
            plusminus = None

        ssize = rash.ProverZnackMass(ZnackMassDitek(zn='size', vl='S', pr='S'), ZnackMassDitek(zn='size', vl='L', pr='L'),
                                     ZnackMassDitek(zn='size', vl='XL', pr='XL'), ZnackMassDitek(zn='size', vl='M', pr='M'),
                                     slov=self.req.GET)

        print(self.req.GET.get('size'))

        if len(ssize) < 1:
            ssize = None

        Date = rash.ProverkaMass(ShifrDitek(val='DateMin', ret=None), ShifrDitek(val='DateMax', ret=None), Vozvrat=False,
                                  slov=self.req.GET, err=[None, ""])
        if len(Date)<2:
            Date = None

        count = rash.ProverkaMass(ShifrDitek(val='minCena', ret=None), ShifrDitek(val='MaxCena', ret=None),
                                 Vozvrat=False,
                                 slov=self.req.GET, err=[None, ""])
        if len(count) < 2:
            count = None
        All = rash.ProverNone(ShifrDitek(val='tovar', ret=None),ShifrDitek(val='kolich', ret=10),ShifrDitek(val='str', ret=0), ShifrDitek(val='person', ret=None), Vozvrat=True,
                              slov=self.req.GET)

        All.update({'plusminus':plusminus,'date':Date, 'count':count, 'size':ssize})

        return All

    def Edit(self, id):
        tranz = AddTovars.objects.get(id=id)
        form = SizeForm(instance=tranz)
        return {'form':form,'id':id}

    def SaveEdit(self,id):
        tranz = AddTovars.objects.get(id=id)
        form = SizeForm(self.req.POST, instance=tranz)
        if form.is_valid():
            form.save()
            return True
        return False


class Paid():
    req = None
    obr = Obrabotka()
    tovar = TOVAR()
    person = PERSON()
    oper = OPERATIONS()
    rash = Shifr()
    def __init__(self, req):
        self.req = req

    def GetPaid(self):



        form = FilterPadiForm(self.req.GET)

        sotrForm = SortOperations(self.req.GET)

        dann = self.ObrParamets()

        paid = self.oper.GetOperationsMinus(str=dann.get('str',1)-1, kolich=dann.get('kolich',10), sorting=dann.get('sorting','date'), sortingType=dann.get('sorttype',False),
                                            status=dann.get('status',None), plusminus=dann.get('plusminus',None), date=dann.get('date',None),
                                            tovar=dann.get('tovar',None), person=dann.get('client',None), money=dann.get('money',None), slovar=True)

        return {"form": form, "paid": paid, 'formsort':sotrForm, 'zapros':self.req.GET}


    def GetOnePaid(self,id):
        oper = self.oper.getOperId(id)
        dann = self.obr.MaxOper(oper)
        return dann


    def Block(self,id, bool):
        try:
            print(bool)
            oper = self.oper.getOperId(id)
            oper.status = bool
            oper.save()
            print('ok')
            return True
        except:
            return False



    def ObrParamets(self):

        stra = self.req.GET.get('str', 1)

        sorting = self.req.GET.get('sort', 'date')

        sortingType = self.req.GET.get('sortingType', None)
        if sortingType == None:
            sortingType = False
        if sortingType == 'on':
            sortingType = True

        if (isinstance(stra, str)):
            if (stra.isdigit()):
                stra = int(stra)
            else:
                stra = 1
        else:
            if (isinstance(stra, int) == False):
                stra = 1

        if stra < 1:
            stra = 1

        kolich = self.req.GET.get('kolich', 10)

        if (isinstance(kolich, str)):
            if (kolich.isdigit()):
                kolich = int(kolich)
            else:
                kolich = 10
        else:
            if (isinstance(kolich, int) == False):
                kolich = 10

        if kolich < 1:
            kolich = 1



        plusminus = self.req.GET.get("plusminus", None)

        Date = self.rash.ProverkaMass(ShifrDitek(val='datemin', ret=datetime.now()-timedelta(days=36500)), ShifrDitek(val='datemax', ret=datetime.now()+timedelta(days=36500)),
                                      Vozvrat=True,
                                      slov=self.req.GET, err=[None, ""])
        if len(Date) < 2:
            Date = None

        Money = self.rash.ProverkaMass(ShifrDitek(val='moneymin', ret=0), ShifrDitek(val='moneymax', ret=99999999),
                                      Vozvrat=True,
                                      slov=self.req.GET, err=[None, ""])
        if len(Money) < 2:
            Money = None

        tovar = self.req.GET.get("tovar", None)

        if tovar=="":
            tovar = None

        massStatus = self.rash.ProverZnackMass(ZnackMassDitek(zn='prynatie', vl=True, pr='on'),
                                               ZnackMassDitek(zn='neprynatie', vl=False, pr='on'),
                                               slov=self.req.GET)
        if len(massStatus) < 1:
            massStatus=None


        client = self.req.GET.get("client", None)

        if client == "":
            client = None

        return {'str': stra,"date":Date,'money':Money, 'sort': sorting, 'sorttype': sortingType, 'kolich': kolich, 'tovar':tovar, 'client':client, 'status':massStatus,'plusminus':plusminus }

class Zakazi():

    rash = Shifr()
    zak = ZAKAZ()
    tovars = None
    req = None
    obrabot = Obrabotka()
    pers = PERSON()
    kardtov = None

    def __init__(self, req):
        self.req = req
        self.tovars = Find__Tovar(req)
        self.kardtov = KardTovarFull(req)

    def TovarZakaz(self, id):
        zakaz = Zakaz.objects.get(id=id)
        tovars = self.__tovarszakaz(zakaz)
        dann = self.tovars.GetTovarsAdm()
        dann.update({'tovars':tovars,'id':id})
        print(dann)
        return  dann

    def otmenazakaz(self,id,bool):
        zakaz = Zakaz.objects.get(id=id)
        zakaz.status = bool
        zakaz.save()
        return True

    def AddZakaz(self,idperson, date):

        idperson = self.__proverkaInt(idperson)
        if idperson !=None:
            itpot = self.zak.AddZakaz(idpers=idperson, date=date)
            return itpot
        return False

    def __tovarszakaz(self, zakaz):
        tovars = zakaz.tovarszakaz_set.all().values('tovar__tovar__name', 'tovar__stoimost', 'tovar__vikup',
                                                    'tovar__Vozvrat', 'tovar__platej', 'tovar__vidArendi__name','tovar__tovar__id' ,'id')
        return tovars

    def GetZakaz(self, id):

        zakaz = Zakaz.objects.get(id=id)

        dann = {'date':zakaz.date,'nomer':zakaz.nomer,'vid':zakaz.vidann, 'name':zakaz.person.name,'id':zakaz.id , 'status':zakaz.status}

        tovars =self.__tovarszakaz(zakaz)

        return {'zakaz':dann,'tovars':tovars}

    def vidacha(self,id):
        try:
            zakaz = Zakaz.objects.get(id=id)

            person = zakaz.person

            tovari = zakaz.tovarszakaz_set.all()

            for tov in tovari:

                ewe = TovarPerson(VidArendiTovars=tov.tovar, person=person, Data=datetime.now(), size=tov.size.Size.name)
                ewe.save()

            zakaz.vidann = True
            zakaz.save()
            return True
        except:
            return False

    def GetZakazKlient(self,id):
        zakaz = Zakaz.objects.get(id=id)

        dann = {'date': zakaz.date, 'nomer': zakaz.nomer, 'name': zakaz.person.name, 'id': zakaz.id,
                'status': zakaz.status}

        tovars = zakaz.tovarszakaz_set.all()

        Tovari = []


        for tov in tovars:

            normrent = self.obrabot.NormVidArendi(tov.tovar)
            normsize = self.obrabot.NormTovarsSize(tov.size)
            normtovar = self.obrabot.NormTovar(tov.tovar.tovar)


            tovari = {}
            tovari.update(normrent)
            tovari.update(normsize)
            tovari.update(normtovar)

            Tovari.append(tovari)

        return {'zakaz': dann, 'tovars': Tovari}


    def SizeTovar(self,id, idzakaz):
        dannye = self.kardtov.GetTovar(id)

        dannye.update({'idzakaz':idzakaz})
        return dannye

    def AddZakazTovar(self, idarendi, idzakaz, idsize):
        idarendi = int(idarendi)
        idzakaz = int(idzakaz)
        idsize = int(idsize)
        itog = self.zak.AddTovars(idzakaz, idarendi, idsize)
        return itog

    def getmassZakaz(self):
        dann = self.obr()

        zakazs = self.zak.getMassZakaz(str=dann.get('str',1)-1, zak= dann.get('zakaz',None), code=dann.get('code',None), otm=dann.get('param',None), schmotki=True, kolich=dann.get('kolich',10),date=dann.get('date',None),values=False,person=dann.get('person'),
                                       sorting=dann.get('sort','date'),sortingType=dann.get('sorttype',True))

        dann = []

        for zak in zakazs:
            dann.append(self.obrabot.ZakazMini(zak))

        form = SortZakaz(self.req.GET)

        main = FindZakaz(self.req.GET)


        return {'zakazi':dann,'main':main, 'formsort':form, 'zapros':self.req.GET}


    def __proverkaInt(self,cifra):
        if (isinstance(cifra, str)):
            if (cifra.isdigit()):
                cifra = int(cifra)
            else:
                cifra = None
        else:
            if (isinstance(cifra, int) == False):
                cifra = None
        return cifra

    def DellZakaz(self,idzakaz):
        idzakaz = self.__proverkaInt(idzakaz)
        if idzakaz != None:
            zakaz = self.zak.dellzakaz(idzakaz)
            return zakaz
        return False



    def obr(self):

        stra = self.req.GET.get('str', 1)

        sorting = self.req.GET.get('sort', 'date')

        sortingType = self.req.GET.get('sortingType', None)
        if sortingType == None:
            sortingType = False
        if sortingType == 'on':
            sortingType = True

        if (isinstance(stra, str)):
            if (stra.isdigit()):
                stra = int(stra)
            else:
                stra = 1
        else:
            if (isinstance(stra, int) == False):
                stra = 1

        if stra < 1:
            stra = 1

        kolich = self.req.GET.get('kolich', 10)

        if (isinstance(kolich, str)):
            if (kolich.isdigit()):
                kolich = int(kolich)
            else:
                kolich = 10
        else:
            if (isinstance(kolich, int) == False):
                kolich = 10

        if kolich < 1:
            kolich = 1


        Date = self.rash.ProverkaMass(ShifrDitek(val='datemin', ret=datetime.now()-timedelta(days=36500)), ShifrDitek(val='datemax', ret=datetime.now()+timedelta(days=36500)),
                                      Vozvrat=True,
                                      slov=self.req.GET, err=[None, ""])

        zakaz = self.rash.ProverZnackMass(ZnackMassDitek(zn='vidan', vl=True, pr='on'),
                                           ZnackMassDitek(zn='noVidan', vl=False, pr='on'), slov=self.req.GET)

        if len(Date) < 2:
            Date = None

        if len(zakaz) <1:
            zakaz= None

        pers = self.req.GET.get('person', None)

        if pers == "":
            pers = None

        code = self.req.GET.get('code',None)

        if code == "":
            code = None

        massStatus = self.rash.ProverZnackMass(ZnackMassDitek(zn='raz', vl=True, pr='on'),
                                               ZnackMassDitek(zn='unraz', vl=False, pr='on'),
                                               slov=self.req.GET)
        if len(massStatus) < 1:
            massStatus = None



        return {'str':stra,'sort':sorting,'code':code, 'zakaz':zakaz, 'sorttype':sortingType, "param":massStatus, 'kolich':kolich, 'date':Date, 'person':pers}

class Reg:
    req = None
    obr = Obrabotka()

    def __init__(self,req):
        self.req = req

    def GetReg(self):
        form = Registration()
        return {'form':form}

    def RegGo(self):
        PerS = None
        try:
            form = Registration(self.req.POST)
            print(self.req.POST)
            if form.is_valid():
                print('Я валидная')
                dannye = form.cleaned_data
                pers = Person(name=dannye['name'], sex=dannye['sex'], Bird=dannye['Bird'], Email=dannye['Email'],
                              phone=dannye['phone'], Zamoroz=False, DateReg=datetime.now(),
                              DataLast=datetime.now())
                pers.save()
                PerS = pers

                user = User.objects.create_user(dannye['login'], dannye['Email'], dannye['password'])
                user.save()

                pers.user = user
                pers.save()
                return True
            return False
        except:
            if PerS != None:
                PerS.delete()
            return False

