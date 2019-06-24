from .models import Tovar, PhotoTovara, VidArendi,Otziv, Set, Person,TovarTypeTovar, VidArendiTovars, TovarPerson,AddPaid, AddTovars, SizeTovars
import django.contrib.auth as auth
from datetime import timedelta, datetime, date
from django.db.models import Avg, Max, Min

class Obrabotka():
    def Obrkorzina(self, tovar, rent, size, kolich, nomer):
        name = tovar.name
        material = tovar.Material

        img = tovar.phototovara_set.filter(main=True)
        if len(img) >0:
            img = img[0].photo
        else:
            img = None

        rentname = rent.vidArendi.name
        rentstoimost = rent.stoimost
        rentvikup = 'Нет выкупа'
        if rent.vikup !=None:
            rentvikup = rent.vikup * rent.platej
        rentvozvrat = rent.Vozvrat * rent.platej
        rentplatej = rent.platej

        size = size.Size.name

        return {'img':img, 'id':tovar.id, 'kolich':kolich ,'name':name, 'material':material, "rentname": rentname, 'rentstoimost': rentstoimost, 'rentvikup':rentvikup, 'rentvozvrat':rentvozvrat,
                'rentplatej':rentplatej, 'size':size, 'nomer':nomer}


    def NormVidArendi(self, rent):
        rentname = rent.vidArendi.name
        rentstoimost = rent.stoimost
        rentvikup = 'Нет выкупа'
        if rent.vikup != None:
            rentvikup = rent.vikup * rent.platej
        rentvozvrat = rent.Vozvrat * rent.platej
        rentplatej = rent.platej
        return {"rentname": rentname, 'rentstoimost': rentstoimost, 'rentvikup':rentvikup, 'rentvozvrat':rentvozvrat,
                'rentplatej':rentplatej}


    def NormTovar(self, tovar):
        name = tovar.name
        material = tovar.Material

        img = tovar.phototovara_set.filter(main=True)
        if len(img) > 0:
            img = img[0].photo
        else:
            img = None
        return {'name': name, 'material': material, "img": img, "id":tovar.id}

    def NormTovarsSize(self, size):
        size = size.Size.name
        return {'size':size}





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
        Name = tvr.name

        price = tvr.vidarenditovars_set.aggregate(Min('stoimost'))['stoimost__min']

        print('цена', price)
        Main = tvr.phototovara_set.all().filter(main=True, delete=False)
        if len(Main) != 0:
            Main = Main[0].photo
        else:
            Main = ''

        return {'name': Name,'cena':price,  'foto': '/static/' + str(Main),
                'url': '/tovar/' + str(tvr.id), 'id': tvr.id}




    def miniNormTovar(self, tovar):

        size = SizeTovars.objects.filter(Tovar__id=tovar.id).values('Size__name','nalichie')
        arenda =  VidArendiTovars.objects.filter(tovar__id=tovar.id).values('vidArendi__name','stoimost','vikup','Vozvrat','platej')

        name = tovar.name
        opisanie = tovar.Opisanie
        brand = tovar.brand.name

        sex = tovar.Sex.name

        Material = tovar.Material

        Del = 'Не известно'

        if tovar.Del == True:
            Del = "Удален"
        else:
            Del = "Не удален"

        return {'size':size,'arenda':arenda, 'name':name,'opisanie':opisanie,'brand':brand,'sex':sex,'material':Material,'del':Del,'id':tovar.id}



    def miniSet(self,set):
        Name = set.name
        Cena = 'Не известно'
        cena = set.vidarendisets_set.filter(vidArendi__name="Аренда")
        if (len(cena) != 0):
            Cena = cena[0].stoimost

        Foto = ''
        photo = set.photosets_set.filter(Main=True)
        if len(photo) > 0:
            Foto =  photo[0].puth

        Foto = set.photosets_set.filter(Main=True)[0]
        opisanie = set.text
        return {'name': Name, 'cena': Cena, 'foto': '/static/' + Foto.puth, 'opisanie': opisanie}

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
        stoimostAren = 'ХЗ'
        Aren = set.vidarendisets_set.all().filter(vidArendi__name='Аренда')
        if (len(Aren ) >0):
            stoimostAren = Aren[0].stoimost

        stoimostPogon = 'ХЗ'
        Pogon = set.vidarendisets_set.all().filter(vidArendi__name='Погонять')
        if (len(Pogon ) > 0):
            stoimostPogon = Pogon[0].stoimost

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
                size.append(siz.Size.name)
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

    def TovarAdminMini(self, tvr):
        name = tvr.name

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

        zakazi = TovarPerson.objects.all().filter(VidArendiTovars__tovar__id=tvr.id).count()
        like = tvr.likeperson_set.count()
        date = tvr.DateAdd
        datelast = tvr.DateEdit

        return {'name':name, 'pricePogon':pricePogon, 'priceArenda':priceArenda, 'zakazi':zakazi, 'like':like, 'date':date,'datelast':datelast, 'id':tvr.id}


    def TovarAdminMax(self,tovar):
        foto = tovar.phototovara_set.all()
        fotomass = []

        for fot in foto:
            if fot.main != True:
                fotomass.append({"foto":fot.photo})

        main = foto.filter(main=True)

        if len(main)<1:
            main = None
        else:
            main = main[0].photo

        type = tovar.tovartypetovar_set.all()

        masstipov = []

        for ty in type:
            masstipov.append(ty.typpe.name)



        brand = tovar.brand.name

        like = tovar.likeperson_set.count()

        sets = Set.objects.filter(tovarssets__tovars__id = tovar.id)[0:10]


        mass = []

        sex = tovar.Sex

        for set in sets:
            name = set.name
            id = set.id
            mass.append({'name':name, 'id':id})

        sezon = []

        koll = tovar.sezontovar_set.all()
        if len(koll) != 0:
            for sez in tovar.sezontovar_set.all():
                nazv = sez.seaz.name
                sezon.append(nazv)

        vid = []
        koll = tovar.tovartypetovar_set.all()
        if len(koll) != 0:
            for type in tovar.tovartypetovar_set.all():
                name = type.typpe.name
                vid.append(name)

        size = self.__size_Mas(tovar.sizetovars_set.all())
        arenda = self.__rent_Mas(tovar.vidarenditovars_set.all())

        return {'size':size,'dell':tovar.Del, 'type':vid, 'name':tovar.name,'id':tovar.id, 'materia':tovar.Material, 'brand':brand ,'arenda':arenda,  'opisanie':tovar.Opisanie,  'foto':fotomass, 'main':main, 'type':masstipov,'sex':sex,'sezon':sezon, 'like':like, 'set':mass }


    def AdmMiniTovarNormExtra(self, tovar):
        name = tovar.name
        opisanie = tovar.Opisanie
        brand = tovar.brand.name

        sex = tovar.Sex.name

        Material = tovar.Material

        Del = 'Не известно'

        if tovar.Del == True:
            Del = "Удален"
        else:
            Del = "Не удален"

        return {'name': name, 'opisanie': opisanie, 'brand': brand, 'sex': sex,
                'material': Material, 'del': Del, 'id': tovar.id}

    def PhotoTovara(self, tovar):
        photomass = []

        photki = tovar.phototovara_set.all()

        if len(photki) > 0:
            for t in photki:
                photomass.append({"photo":t.photo,"main":t.main,'id':t.id, 'del':t.delete})
        return photomass


    def __size_Mas(self, size):
        mass = []
        if size != None:
            for t in size:
                name = t.Size.name
                nal = t.nalichie
                koll = 0
                tranz = t.addtovars_set.all()
                for z in tranz:
                    koll = koll + z.count
                mass.append({'name':name, 'nal':nal, 'koll':koll, 'id':t.id})
        return mass

    def __rent_Mas(self, arenda):
        mass = []
        if arenda != None:
            for t in arenda:
                name = t.vidArendi.name
                platej = t.platej
                stoimost = t.stoimost
                vikup = t.vikup
                vozvrat = t.Vozvrat
                id = t.id
                mass.append({'name': name, 'platej': platej, 'stoimost': stoimost, 'vikup': vikup, 'vozvrat':vozvrat, 'id':id})
        return mass


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

    def TovarNalichie(self,tovar,bool):
        try:
            tovar.Nalichie = bool
            tovar.save()
            return  True
        except:
            return False

    def TovarUdalen(self, tovar, bool):
        try:
            tovar.Del = bool
            tovar.save()
            return  True
        except:
            return False

    def PersonBalanse(self, person):
        minus = person.addpaid_set.filter(status=True, plusminus="False")
        plus = person.addpaid_set.filter(status=True, plusminus="True")
        Plus = 0
        for pl in plus:
            Plus = Plus + pl.money
        Minus = 0
        for mn in minus:
            Minus = Minus + mn.money
        return Plus - Minus


    def AdmMaxPerson(self, person):
        user = person.user
        sex = person.sex
        phone = person.phone
        Vk = person.Vk
        Insta = person.Insta
        Status = person.Status
        DateReg = person.DateReg
        DataLast = person.DataLast
        Zamoroz = person.Zamoroz
        Balans = self.PersonBalanse(person)
        Email = person.Email
        name = person.name
        Bird = person.Bird
        Adress = person.Adress
        id = person.id
        schmotki = person.tovarperson_set.all()

        chislo = schmotki.count()

        massvechi = []

        for ve in schmotki:
            tov = ve.VidArendiTovars.tovar
            obrve = self.TovarAdminMini(tov)
            massvechi.append(obrve)

        otz = person.otziv_set.all()

        massotz = []

        for ot in otz:
            massotz.append(self.OtziviMax(ot))

        plata = 0

        tovars = person.tovarperson_set.all().values('VidArendiTovars__stoimost')

        zakazs = []
        zakazi = person.zakaz_set.all()
        for zak in zakazi:
            elem = self.zakazMini(zak)
            zakazs.append(elem)

        for t in tovars:
            plata = plata + int(t['VidArendiTovars__stoimost'])

        return {'name':name, 'adress':Adress,'zakazi':zakazs, 'datereg':DateReg, 'datelast':DataLast, 'plata':plata, 'schchislo':chislo,'balans':Balans, 'birth':Bird, 'zamoroz':Zamoroz, 'email':Email,
                'phone':phone,'sex':sex, 'tovari':massvechi,'id':id, 'otzivi':massotz}


    def zakazMini(self, zakaz):
        nomer = zakaz.nomer
        kolich = zakaz.tovarszakaz_set.all().count()
        date = zakaz.date
        pers = zakaz.person.name
        return {'nomer':nomer,'kolich':kolich,'date':date,'pers':pers,'id':zakaz.id}

    def AdmMini(self, person):
        user = person.user
        sex = person.sex
        phone = person.phone
        Vk = person.Vk
        Insta = person.Insta
        Status = person.Status
        DateReg = person.DateReg
        DataLast = person.DataLast
        Zamoroz = person.Zamoroz
        Balans = person.Balans
        Email = person.Email
        name = person.name
        Bird = person.Bird
        Adress = person.Adress
        id = person.id


        return {'name': name, 'adress': Adress, 'datereg': DateReg, 'datelast': DataLast,
                'balans': Balans, 'birth': Bird, 'zamoroz': Zamoroz, 'email': Email,
                'phone': phone, 'sex': sex, 'id':id}


    def AdmPersZamoroz(self, client, bool):
        try:
            client.Zamoroz = bool
            client.save()
            return True
        except:
            return False




    def AdmBalance(self, client, money):
        try:
            paid = AddPaid(status=True, date=datetime.now(), person=client, money=money)
            paid.save()
            return True
        except:
            return False


    def AdmPass(self, client, password):
        try:
            u = client.user
            u.set_password(password)
            u.save()
            return True
        except:
            return False

    def AdmAddTovar(self, client, Tovar):
        try:
            tov =  TovarPerson(person=client, VidArendiTovars=Tovar)
            tov.save()
            return True
        except:
            return False

    def OtziviMax(self, otz):


        Opisanie = otz.Opisanie
        zvezdi = otz.zvezdi
        delete = otz.delete
        otvet = None
        if otz.Otvet !=None:
            otvet = otz.Otvet

        name=None
        idpers=None
        if otz.Person !=None:
            name = otz.Person.name
            idpers = otz.Person.id

        namef = None
        if otz.nameperson !=None:
            namef = otz.nameperson
            idpers=2

        date = otz.date

        dannTovar = None
        if otz.Tovar !=None:
            Tovar = otz.Tovar
            dannTovar = self.miniNormTovar(Tovar)

        dannSet = None
        if otz.Set !=None:
            Set = otz.Set
            dannSet = self.miniSet(Set)

        Status = otz.Status
        otvet = {'Opisanie':Opisanie,'delete':delete,'otvet':otvet, 'id':otz.id, 'zvezdi':zvezdi, 'name':namef, 'date':date, 'Status':Status}


        return {'otziv':otvet, 'client':{'name':name,'id':idpers}, 'tovar':dannTovar, 'set':dannSet}

    def DelOtz(self, otz, bool):
        try:
            otz.delete = bool
            otz.save()
            return True
        except:
            return False

    def Razresh(self, otz, bool):
        try:
            if bool == True:
                otz.Status = "Принят"
            if bool == False:
                otz.Status = "Отклонен"
            otz.save()
            return True
        except:
            return False

    def OtvetOtz(self,otz, txt, bool=False):
        try:
            if bool == False:
                otz.Otvet = txt
                otz.save()
            else:
                otz.Otvet = None
                otz.save()
            return True
        except:
            return False


    def MaxOper(self, oper):
        status = oper.status
        plusminus = oper.plusminus
        person = self.AdmMaxPerson(oper.person)
        date = oper.date
        money = oper.money

        tovar = None
        tovPer = None
        rent = None
        size = None
        if oper.tovPer !=None:
            tovPer = oper.tovPer
            tovar =tovPer.VidArendiTovars.tovar
            tovar = self.AdmMiniTovarNormExtra(tovar)
            if tovPer.VidArendiTovars != None:
                rent = self.__rent_Mas([tovPer.VidArendiTovars])
            if tovPer.size != None:
                size = tovPer.size

        return {'status':status,'plusminus':plusminus,'pers':person,'date':date,'money':money,'tovPer':tovPer,'arenda':rent,'size':size, 'tovar':tovar, 'id':oper.id}

    def ZakazMini(self, zakaz):
        code = zakaz.nomer
        name = zakaz.person.name
        date = zakaz.date
        tovari = None
        schmotki = zakaz.tovarszakaz_set.all()
        if len(schmotki) >0:
            tovari = []
        for sch in schmotki:
            tovari.append(sch.tovar.tovar.name)
        vid = zakaz.vidann

        return {'name':name,'vid':vid,'date':date,'code':code, 'tovari':tovari, 'id':zakaz.id, 'status':zakaz.status}