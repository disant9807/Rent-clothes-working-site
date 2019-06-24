from .models import Sex, Tovar, PhotoTovara, VidArendi,Otziv,TovarTypeTovar, Set,Zakaz,TovarsZakaz, Person, VidArendiTovars, TovarPerson,SezonTovar, Seaz, TypeTovars, Brand,SizeTovars, AddPaid, AddTovars
import django.contrib.auth as auth
from django.db.models import Count, Min, Sum
from datetime import timedelta, datetime, date
from django.db.models import F
from django.db.models import Q
from django.db.models import Value as V
from django.http import HttpResponse
import secrets

class GetOperations():

    def GetMassOperations(self,value= None, person = None, personName = None, date=None, tovarName =None, tovar= None, sizeName = None, count=None, PlusMinus=None, sorting = None, sortingtype=None,  str=0, kolich=10 ):

        tranzak = AddTovars.objects

        if personName!=None:
            tranzak = tranzak.filter(client__name__startswith=personName)

        if person !=None:
            tranzak = tranzak.filter(client__id=person)

        if date !=None:
            tranzak = tranzak.filter(date__range=date)

        if tovarName !=None:
            tranzak = tranzak.filter(tovar__name__startswith=tovarName)

        if tovar !=None:
            tranzak = tranzak.filter(tovar__name__id=tovar)

        if sizeName !=None:
            tranzak = tranzak.filter(size__Size__name__in=sizeName)

        if count !=None:
            tranzak = tranzak.filter(count__range=count)

        if PlusMinus !=None:
            tranzak = tranzak.filter(PlusMinus__in=PlusMinus)

        if sortingtype == True:
            if sorting!=None:
                tovar = tovar.order_by(sorting).distinct()
        if sortingtype == False:
            if sorting!=None:
                tovar = tovar.order_by('-' + sorting).distinct()

        print(str, kolich)

        if value ==True:
            tranzak = tranzak.values('date','tovar__name','client__name','size__Size__name','count','PlusMinus','id')[str * kolich: (str * kolich) + kolich]

        else:
            tranzak = tranzak [str * kolich: (str * kolich) + kolich]

        return tranzak



class TOVAR():

    def handle_uploaded_file(self, f, name):
        with open('static/IMG_TOVARI/' + name + f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def add(self, name='', opisanie='', size=[], material='', sex='', nal=False, brand='', type='', seaz=[], MainPhoto= None, Photos = None):

        try:
            SEX = Sex.objects.get(id=int(sex))

            tvr = Tovar(name=name, Opisanie=opisanie, Material=material, DateAdd=datetime.now(),
                        DateEdit=datetime.now(), Sex=SEX)

            if (brand != '' and brand != None):
                bran = Brand.objects.filter(name=brand)
                if (len(bran) < 1):
                    br = Brand(name=brand)
                    br.save()
                    tvr.brand = br
                else:
                    tvr.brand = bran[0]

            tvr.Del = False;
            tvr.save()

            for tt in type:
                findtype = TypeTovars.objects.filter(name=tt)
                if (len(findtype) < 1):
                    br = TypeTovars(name=tt)
                    br.save()
                    sv = TovarTypeTovar(typpe=br, tovar=tvr)
                    sv.save()
                else:
                    sv = TovarTypeTovar(typpe=findtype[0], tovar=tvr)
                    sv.save()

            for s in size:
                si = SizeTovars(Tovar=tvr, Size=s)
                si.save()

            for t in seaz:
                print(t)
                se = Seaz.objects.filter(name=t)
                if (len(se) > 0):
                    print('добавляю сезон')
                    add = SezonTovar(seaz=se.first(), tovar=tvr)
                    add.save()

            if MainPhoto != None:
                self.handle_uploaded_file(MainPhoto, str(tvr.id))
                phot = PhotoTovara(photo='IMG_TOVARI/'+str(tvr.id)+MainPhoto.name, main=True, tovar=tvr, delete=False)
                phot.save()

            return tvr.id
        except:
            return False


    def UploadPhoto(self, photo, id, bool):

        if bool == True:
            photos = PhotoTovara.objects.filter(tovar_id=id)
            for ph in photos:
                ph.main = False
                ph.save()

        self.handle_uploaded_file(photo, str(id))
        phot = PhotoTovara(photo='IMG_TOVARI/' + str(id) + photo.name, main=bool, tovar_id=id, delete=False)
        phot.save()



    def dell(self, id):
        try:
            tvr = Tovar.objects.get(id=idd)
            tvr.delete()
            return True
        except:
            return False

    def GetTovarId(self, idd):
        tvr = Tovar.objects.get(id=idd)
        return tvr

    def GetMassTovar(self, str=0, nal=True, dele=None, kolich=10, type=None, sorting='DateAdd', sortingType=True, name=None, Brand=None, seaz= None, sex=None, Size=None, Price=None, vid=None):
        tovar = Tovar.objects.all()


        if dele != None:
            tovar = tovar.filter(Del__in=dele)


        if name != None:
            tovar = tovar.filter(name__startswith=name)

        if Brand != None:
            tovar = tovar.filter(brand__name__startswith=Brand)

        if seaz !=None:
            tovar = tovar.filter(sezontovar__seaz__name__in=seaz)

        if sex !=None:
            tovar = tovar.filter(Sex__name__in=sex)

        if Size !=None:
            tovar = tovar.filter(sizetovars__Size__name__in=Size)

        if Price != None:
            tovar = tovar.annotate(minimum=Min('vidarenditovars__stoimost')).filter(minimum__range=Price)

        if type != None:
            tovar = tovar.filter(tovartypetovar__typpe__name=type)

        if  vid!=None:
            tovar = tovar.filter(tovartypetovar__typpe__name__in=vid)

        if nal != None:
            tovar = tovar.filter(sizetovars__nalichie=True)

        if (sortingType == True):
            if sorting =='arenda':
                tovar = tovar.annotate(zakazi__count=Count('vidarenditovars__tovarperson')).order_by('zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'like':
                tovar = tovar.annotate(zakazi__count=Count('likeperson')).order_by('zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'stoimost':
                tovar = tovar.annotate(zakazi__price=Min('vidarenditovars__stoimost')).order_by('zakazi__price').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'DateAdd':
                tovar = tovar.order_by('DateAdd').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting !='arenda' and sorting!='like' and sorting!='stoimost' and sorting!='DateAdd':
                tovar = tovar.order_by('DateAdd').distinct()[str * kolich: (str * kolich) + kolich]

        else:
            if sorting =='arenda':
                tovar = tovar.annotate(zakazi__count=Count('vidarenditovars__tovarperson')).order_by('-zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'like':
                tovar = tovar.annotate(zakazi__count=Count('likeperson')).order_by('-zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'stoimost':
                tovar = tovar.annotate(zakazi__price=Min('vidarenditovars__stoimost')).order_by('-zakazi__price').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'DateAdd':
                tovar = tovar.order_by('-DateAdd').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting !='arenda' and sorting!='like' and sorting!='stoimost' and sorting!='DateAdd':
                tovar = tovar.order_by('-DateAdd').distinct()[str * kolich: (str * kolich) + kolich]
        return tovar

    def edit(self, ID, Name = None, nalich = None, opisanie = None,brand = None, _priceArenda = None, VozvratArenda = None, _pricePogon = None, Material = None, Sex = None,
             type = None, MainPhoto = None, Photo=None, size=None, sezon=None):

        tvr = Tovar.objects.get(id=ID)
        if Name != None:
            tvr.name = Name

        if opisanie != None:
            tvr.opisanie = opisanie
        if Material != None:
            tvr.Material = Material
        if Sex != None:
            tvr.sex = Sex
        if brand != None:
            brandd = Brand.objects.filter(name=brand).all()
            if len(brandd) > 0:
                tvr.brand = brandd[0]
            else:
                brandnew = Brand(name=brand)
                brandnew.save()
                tvr.brand = brandnew

        if type!=None:

            deltype = tvr.tovartypetovar_set.all()
            for t in deltype:
                t.delete()

            for tt in type:
                findtype = TypeTovars.objects.filter(name=tt)
                if (len(findtype) < 1):
                    br = TypeTovars(name=tt)
                    br.save()
                    sv = TovarTypeTovar(typpe=br, tovar=tvr)
                    sv.save()
                else:
                    sv = TovarTypeTovar(typpe=findtype[0], tovar=tvr)
                    sv.save()

        if size != None:
            starSize = tvr.sizetovars_set.all()

            for star in starSize:
                star.delete()

            for s in size:
                si = SizeTovars(Tovar=tvr, Size=s)
                si.save()



        if sezon != None:
            starSezon = tvr.sezontovar_set.all()

            for star in starSezon:
                star.delete()

            for t in sezon:
                se = Seaz.objects.filter(name=t)
                if (len(se) > 0):
                    add = SezonTovar(seaz=se.first(), tovar=tvr)
                    add.save()
        if _priceArenda!=None:
            priceArenda = tvr.vidarenditovars_set.filter(vidArendi__name="Аренда")[0]
            priceArenda.stoimost = _priceArenda
            priceArenda.Vozvrat = VozvratArenda
            priceArenda.save()

        if _pricePogon !=None:
            pricePogon = tvr.vidarenditovars_set.filter(vidArendi__name="Погонять")[0]
            pricePogon.stoimost = _pricePogon
            pricePogon.save()



        if Photo != None:
            pho = tvr.phototovara_set.all()
            for phot in pho:
                if phot.main ==False:
                    phot.delete()
            t = 0
            for file in Photo:
                self.handle_uploaded_file(file, str(tvr.id)+str(t))
                phot = PhotoTovara(photo='IMG_TOVARI/'+str(tvr.id)+str(t)+file.name, main=False, tovar=tvr)
                phot.save()
                t = t + 1

        if MainPhoto!=None:
            phoo = tvr.phototovara_set.all()
            for photo in phoo:
                if photo.main == True:
                    photo.delete()

            self.handle_uploaded_file(MainPhoto, str(tvr.id))
            phot = PhotoTovara(photo='IMG_TOVARI/' + str(tvr.id) + MainPhoto.name, main=True, tovar=tvr)
            phot.save()












class SET():

    def GetMassSet(self, str=0, kolich=10, name='', kurtka='', shapka='', shtani='', obyv='',
                   seaz=[
                       'Лето', 'Зима', 'Весна', 'Осень'
                   ], sex=[
                'Мужской', 'Женский', 'Унисекс'
            ], Size=[
                'S', 'M', 'L', 'XL'
            ], Price=[
                0, 999999
            ], Type=[
                'Куртка', 'Ботинки', 'Штаны', 'Голова'
            ], sortingType=True,sorting='DateAdd' ):
        set = Set.objects.all().filter(
            Q(tovarssets__tovars__name__startswith=shapka) | Q(tovarssets__tovars__name__startswith=shtani) | Q(
                tovarssets__tovars__name__startswith=kurtka) | Q(tovarssets__tovars__name__startswith=obyv),
            name__startswith=name, sizetovars__Size__in=Size, seaztovar__name__in=seaz)

        print(sorting, sortingType, str, kolich)

        if (sortingType == True):
            if sorting =='arenda':
                set = set.annotate(zakazi__count=Count('vidarendisets__setsperson')).order_by('zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'like':
                set = set.annotate(zakazi__count=Count('likeperson')).order_by('zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'stoimost':
                set = set.annotate(zakazi__price=Min('vidarendisets__stoimost')).order_by('zakazi__price').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'DateAdd':
                set = set.order_by('DateAdd').distinct()[str * kolich: (str * kolich) + kolich]
        else:
            if sorting =='arenda':
                set = set.annotate(zakazi__count=Count('vidarendisets__setsperson')).order_by('-zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'like':
                set = set.annotate(zakazi__count=Count('likeperson')).order_by('-zakazi__count').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'stoimost':
                set = set.annotate(zakazi__price=Min('vidarendisets__stoimost')).order_by('-zakazi__price').distinct()[str * kolich: (str * kolich) + kolich]
            if sorting == 'DateAdd':
                set = set.order_by('-DateAdd').distinct()[str * kolich: (str * kolich) + kolich]
        return set

    def GetSet(self, id=0):
        set = Set.objects.filter(id=id)[0]
        return set

    def Add(self):
        pass

    def Dell(self):
        pass


class OTZ():

    def add(self, text, idpers, rating, idtovar = None,idset = None):
        try:
            otz = Otziv()
            if (idtovar != None):
                tovar = TOVAR()
                otz.Tovar = tovar.GetTovarId(idtovar)
            if (idset != None):
                set = SET()
                otz.Set = set.GetSet(idset)
            otz.Opisanie = text
            otz.date = datetime.now()
            otz.delete=False

            pers = PERSON()
            otz.Person = pers.GetPersonid(idpers)
            otz.zvezdi = rating

            otz.save()
            return True
        except:
            return False

    def GetOneOtz(self ,id):
        otziv = Otziv.objects.get(id=id)
        return otziv

    def GetOtz(self, value=False, delete=None, str=0, kolich=10, set=False, id=None , status=None, rating=None, clientid = None,personName= None, tovarName = None, sorting='date', sortingType=True):
        otsyvi = Otziv.objects.all()

        print( str, kolich, set, id , status, rating, clientid,personName, tovarName, sorting, sortingType)

        if (set == False):
            if id !=None:
                otsyvi = otsyvi.filter(Tovar__id=id)
            if status != None:
                otsyvi = otsyvi.filter(Status__in=status)
            if clientid  !=None:
                otsyvi = otsyvi.filter(Person__id=clientid)
            if rating !=None:
                otsyvi = otsyvi.filter(zvezdi__in=rating)
            if personName !=None:
                otsyvi = otsyvi.filter(Q(Person__name__startswith=personName)|Q(nameperson__startswith=personName))
            if tovarName !=None:
                otsyvi = otsyvi.filter(Tovar__name__startswith=tovarName)
            if delete != None:
                otsyvi = otsyvi.filter(delete=delete)

        if (set == True):
            if id !=None:
                otsyvi = otsyvi.filter(Set__id=id)
            if status != None:
                otsyvi = otsyvi.filter(Status__in=status)
            if clientid  !=None:
                otsyvi = otsyvi.filter(Person__id=clientid)
            if rating !=None:
                otsyvi = otsyvi.filter(zvezdi__in=rating)
            if personName !=None:
                otsyvi = otsyvi.filter(Q(Person__name__startswith=personName)|Q(nameperson__startswith=personName))
            if tovarName !=None:
                otsyvi = otsyvi.filter(Set__name__startswith=tovarName)
            if delete != None:
                otsyvi = otsyvi.filter(delete=delete)


        if (sortingType == True):
            otsyvi = otsyvi.order_by(sorting)
        else:
            otsyvi = otsyvi.order_by('-'+sorting)

        if value == False:
            otsyvi = otsyvi[str * kolich: (str * kolich) + kolich]
        if value == True:
            otsyvi = otsyvi.values('Person__name','Opisanie','zvezdi','Tovar__name','date','Status','delete','Otvet','nameperson','id')[str * kolich: (str * kolich) + kolich]

        return otsyvi

    def edit(self):
        pass

    def dell(self):
        pass

    def Edit(self):
        pass


class PERSON:
    def GetPersonid(self, id):
        per = Person.objects.get(id=id);
        return per

    def GetListPerson(self, str=0, sorting='DateReg', kolich=10, sortingType=True, sex=None, phone=None,
                      VK=None, Insta=None, Status=None, Zamoroz=None, Balananse=None, name=None):

        per = Person.objects.all()

        if (sex != None):
            per = per.filter(sex__in=sex)

        if (phone != None):
            per = per.filter(phone__startswith=phone)

        if (name !=None):
            per = per.filter(name__startswith=name)

        if (VK != None):
            per = per.filter(Vk__startswith=VK)

        if (Insta !=None):
            per = per.filter(Insta__startswith=Insta)

        if (Status != None):
            per = per.filter(Status__in=Status)

        if (Zamoroz !=None):
            per = per.filter(Zamoroz__in=Zamoroz)



        if (sortingType == True):
            if(sorting=='bird'):
                per = per.order_by('Bird')[str * kolich: (str * kolich) + kolich]
            if (sorting=='balance'):
                per = per.order_by('balance')[str * kolich: (str * kolich) + kolich]
            if (sorting=="schmotki"):
                per = per.annotate(schmper = Count('tovarperson')).order_by('schmper').distinct()[str * kolich: (str * kolich) + kolich]
            if (sorting=="paid"):
                per = per.annotate(schmper = Sum('tovarperson__VidArendiTovars__stoimost')).order_by('schmper').distinct()[str * kolich: (str * kolich) + kolich]
        else:
            if (sorting == 'bird'):
                per = per.order_by('-Bird')[str * kolich: (str * kolich) + kolich]
            if (sorting == 'balance'):
                per = per.order_by('-balance')[str * kolich: (str * kolich) + kolich]
            if (sorting == "schmotki"):
                per = per.annotate(schmper=Count('tovarperson')).order_by('-schmper').distinct()[
                      str * kolich: (str * kolich) + kolich]
            if (sorting == "paid"):
                per = per.annotate(schmper=Sum('tovarperson__VidArendiTovars__stoimost')).order_by(
                    '-schmper').distinct()[str * kolich: (str * kolich) + kolich]

        return per



    def EditPerson(self, id=None, sex=None, phone=None, Vk=None, Insta=None, Zamoroz=None, Balans=None, Email=None,
                   name=None, Bird=None):
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

    def ProverkaPerson(self, id, tovar):
        try:
            tovari = TovarPerson.objects.filter(VidArendiTovars__tovar_id = tovar, person_id=id)
            print('поиск', tovari[0].id)
            if(len(tovari) >0):
                return True
            else:
                return False
        except:
            return False

class OPERATIONS():

    def GetOperationsMinus(self, str=0, kolich=10, slovar=False, sorting=None, sortingType=True, status=None,plusminus= None, date=None,
                           tovar=None, person=None, money = None):
        paid = AddPaid.objects.all()

        print( str, kolich, slovar, sorting, sortingType, status,plusminus, date,
                           tovar, person, money)

        if money !=None:
            paid = paid.filter(money__range=money)
        if plusminus != None:
            paid = paid.filter(plusminus__in = plusminus)
        if status != None:
            paid = paid.filter(status__in=status)
        if date != None:
            paid = paid.filter(date__range=date)
        if tovar != None:
            paid = paid.filter(tovPer__VidArendiTovars__tovar__name__startswith=tovar)
        if person != None:
            paid = paid.filter(person__name__startswith=person)
        if sorting != None:
            if sortingType == True:
                paid = paid.order_by(sorting)[str * kolich: (str * kolich) + kolich]
            if sortingType == False:
                paid = paid.order_by('-' + sorting)[str * kolich: (str * kolich) + kolich]
        else:
            paid = paid.order_by('date')[str * kolich: (str * kolich) + kolich]

        if slovar != True:
            return paid
        else:
            return paid.values('status','plusminus','person__name','date','money','tovPer__VidArendiTovars__tovar__name','id')

    def getOperId(self, id):
        oper = AddPaid.objects.get(id=id)
        return oper

    def AddOper(self, text, summ, id):
        try:
            person = Person.objects.get(id=id)
            operations = opration()
            operations.person = person
            operations.type = text
            operations.summ = summ
            operations.date = datetime.now().date()
            operations.save()
        except:
            return False

    def GetListOperations(self,id = 0, text="", str=0, kolich=10, sortingType=True, sorting="date"):
        try:
            oper = opration.objects.all().filter( type__startswith = text , person__id=id)

            voz = None
            if (sortingType == True):
                voz = oper.order_by(sorting)[str * kolich: (str * kolich) + kolich]
            else:
                voz = oper.order_by('-' + sorting)[str * kolich: (str * kolich) + kolich]
            return oper
        except:
            return None

class  ZAKAZ:


    def AddZakaz(self,idpers, date):
        try:
            nomer = secrets.token_hex(3)
            nomer = nomer + str(idpers) + str(datetime.now().day + datetime.now().minute + datetime.now().year)
            zak = Zakaz(nomer = nomer, date=date,person_id=idpers, status=True, vidann=False)
            zak.save()
            return zak.id
        except:
            return False

    def getzakaz(self, id):
        try:
            zak = Zakaz.objects.get(id=id)
            return zak
        except:
            return None

    def AddTovars(self,idzakaz, idtovars, idsize):

        zak = TovarsZakaz(zakaz_id=idzakaz, tovar_id=idtovars, size_id=idsize)
        zak.save()
        return True

    def getMassZakaz(self, zak = None, schmotki=None,code=None, otm=None, values= None, tovar=None, date=None, person=None, person_id=None, sorting=None, sortingType=False, str=0, kolich=10):
        zaka = Zakaz.objects

        if code !=None:
            zaka = zaka.filter(nomer__startswith=code)
        if date !=None:
            zaka = zaka.filter(date__range=date)
        if person !=None:
            zaka = zaka.filter(person__name__startswith=person)
        if person_id !=None:
            zaka = zaka.filter(person__id=person_id)

        if otm !=None:
            zaka = zaka.filter(status__in=otm)

        if zak !=None:
            zaka = zaka.filter(vidann__in=zak)

        if sortingType ==True:
            if sorting=="date":
                if schmotki == True:
                    zaka = zaka.annotate(sch=Count('tovarszakaz')).order_by('date').distinct()[str * kolich: (str * kolich) + kolich]
                else:
                    zaka = zaka.order_by('date').distinct()[str * kolich: (str * kolich) + kolich]
            else:
                zaka = zaka.order_by('date').distinct()[str * kolich: (str * kolich) + kolich]

        if sortingType == False:
            if sorting=="date":
                if schmotki == True:
                    zaka = zaka.annotate(sch=Count('tovarszakaz')).order_by('-date').distinct()[str * kolich: (str * kolich) + kolich]
                else:
                    zaka = zaka.order_by('-date').distinct()[str * kolich: (str * kolich) + kolich]
            else:
                zaka = zaka.order_by('-date').distinct()[str * kolich: (str * kolich) + kolich]

        if values ==True:
            if schmotki ==True:
                zaka = zaka.values('date','person__name','id','sch')
            else:
                zaka = zaka.values('date','person__name','id')

        return zaka

    def dellzakaz(self,id):
        zak = TovarsZakaz.objects.get(id=id)
        zak.delete()
        return True




