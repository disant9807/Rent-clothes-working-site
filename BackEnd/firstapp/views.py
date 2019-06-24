from django.shortcuts import render
from .models import Tovar, PhotoTovara, VidArendi,Otziv, Set, Person, VidArendiTovars, TovarPerson, AddSizeTov
import django.contrib.auth as auth
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .views_Obr import Main, Reg, Find__Set,EditPassClient, Find__Tovar, KardTovar, LKabinet,Edit,Korrrzz, NewOtzyv, KardTovarFull, EditTovar,adminClident,adminikardclient,adminOtzivi, Paid, journal, Zakazi
from .grafik import Graf
from django.http import HttpResponse
import django.contrib.auth as auth
from django.contrib.auth.models import User

def sory(text):
    return HttpResponse("<h2>Sorry Babe, i crash, becouse:"+ text +"</h2>")


def FindTovars(req):
    find = Find__Tovar(req)
    if req.method == "GET" and len(req.GET)!=0:
        return render(req, "Find_tovars_v2.html",context=find.GetTovars(True))
    else:
        return render(req, "Find_tovars_v2.html", context=find.GetTovars(False))

def tovars(req,id):
    kard = KardTovar(req=req)

    if req.method == "POST":
        if req.POST.get("addrent", None) !=None:
            itog = kard.ObraborkaRent(id)
            if itog == True:
                return render(req, "Message.html", context={"message":'Данные успешно внесены!'})
            else:
                return render(req, "Message.html",  context={"message":'Не удалось внести данные'})

    dannye = kard.GetTovar(id=id)
    return render(req, "tovar_v2.html", context=dannye)

def tovarAddOT(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    idd = id
    edit = NewOtzyv(req)
    if req.method=='POST':
        itog = edit.editPers(idd)
        if(itog == False):
            sory(req, 'Не удалось добавить отзыв')
        return HttpResponseRedirect('/tovar/' + str(id))
    dannye = edit.getOtz(idd)
    dannye.update({'id':id})
    return render(req, "tovar_v2Otz.html", context=dannye)


def Setssss (req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    set = Find__Set(req)
    setti= set.GetSet()
    print(setti['form'])
    return render(req, "Find_set_v2.html", context={'Sets':setti['set'],'form':setti['form']})

def edit(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    ed = Edit(req)
    if req.method == "POST":
            ed.editPers()
            return HttpResponseRedirect('/kabinet')
    else:
        return render(req, "LK_Kabinet_v2_EditPerson.html", context=ed.getPers())

def editPass(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    edit = EditPassClient(req)

    if req.method == "POST":
        password = req.POST.get('password',None)
        if password != None:
            itoh = edit.EditPass(password)
            if itoh == True:
                return HttpResponseRedirect('/kabinet')
            else:
                return render(req, "LK_Kabinet_v2_EditPass.html", context={'message': 'Извините, не удалось изменить пароль :('})

    return render(req, "LK_Kabinet_v2_EditPass.html", context={'message':'Ожидается отправки'})

def SetOne(req, id=1):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    print(id)
    setInter = Find__Set(req)
    set = setInter.GetOneSet(id=id)

    return render(req, "tovar-set_v2.html", context={'set':set['set'],'otz':set['otz']})

def main(req):
    ma = Main(req)
    dann = ma.GetTovar()
    return render(req,"Main.html",context=dann)

def auto(req):
    if req.user.is_authenticated:
        return HttpResponseRedirect('/kabinet/')

    if(req.method=='POST'):
        dannye =  my_view(req)
        return HttpResponseRedirect('/kabinet')
    return render(req, "Autorization_V2.html")

def kabinet(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

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
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

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
            return HttpResponseRedirect('/auto/')
    else:
        return HttpResponseRedirect('/auto/')

class Proverka():

    def masslenStr0(self,mass):
        if(len(mass)!=0):
            return mass[0]
        return ''

def HistOper(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    oper =  HistoryOperation(req)
    dannye = oper.GetOperations()
    return render(req,"History__v2.html", context={"mass":dannye})

def Korz(req):

    korz = Korrrzz(req)
    if req.method == "POST":
        if req.POST.get('dell',None) == "1":
            id = req.POST.get('dellid',None)
            if id !=None:
                itog = korz.DellSize(id)
                if itog == True:
                    dannye = korz.GetDannye()
                    return render(req, "korzina_success.html", context=dannye)
        if req.POST.get('minus',None) == "1":
            id = req.POST.get('minid',None)
            if id !=None:
                itog = korz.editkolich(id, False)
                if itog == True:
                    dannye = korz.GetDannye()
                    return render(req, "korzina_success.html", context=dannye)

        if req.POST.get('plus',None) == "1":
            id = req.POST.get('plusid',None)
            if id !=None:
                itog = korz.editkolich(id, True)
                if itog == True:
                    dannye = korz.GetDannye()
                    return render(req, "korzina_success.html", context=dannye)

        if req.POST.get('addzakaz',None) == "1":
            itog = korz.AddZakaz()
            if itog !=False:
                return HttpResponseRedirect('/zakaz/' + str(itog))

    dannye = korz.GetDannye()
    return render(req, "korzina_v2.html",context=dannye)

def AdmTovar(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    find = Find__Tovar(req)

    return render(req, "Bot_spispok-TVR.html", context=find.GetTovarsAdm())

def AdmKardTovar(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    find = KardTovarFull(req=req)

    if req.method == "POST":
        if req.POST.get("addsize") == '1':
            itog = find.AddSize(id)
            if itog == True:
                return  render(req, "Bot_message.html", context={"text":"Данные успешно внесены!"})
            else:
                return render(req, "Bot_messageBad.html", context={"text": "Не удалось добавить данные"})
        if req.POST.get('addsizetov') =='1':
            itog = find.AddSizeTovar(id)
            if itog == True:
                return  render(req, "Bot_message.html", context={"text":"Данные успешно внесены!"})
            else:
                return render(req, "Bot_messageBad.html", context={"text": "Не удалось добавить данные. Возможно такой размер уже имеется у товара"})
        if req.POST.get('dellsize') == '1':
            id = req.POST.get('iddell',None)
            if id !=None:
                itog = find.DellSize(int(id))
                if itog == True:
                    return render(req, "Bot_message.html", context={"text": "Размер удален!"})
                else:
                    return render(req, "Bot_messageBad.html", context={
                        "text": "Не удалось удалить данные. Возможно все дело в том, что количество размеры не равны 0"})

        if req.POST.get('delltovar') == "1":
            itog = find.DellTovar(id, True)
            dannye = find.GetTovar(id)
            return render(req, "Bot_Card-Tovars.html", context=dannye)

        if req.POST.get('undell') == "1":
            itog = find.DellTovar(id, False)
            dannye = find.GetTovar(id)
            return render(req, "Bot_Card-Tovars.html", context=dannye)

        if req.POST.get('nalsize') == '1':
            print("1e")
            id = req.POST.get('iddnal', None)
            boolka = req.POST.get('naldel',None)
            if id != None:
                print("2e" ,boolka)
                reashenir = None
                if boolka == 'on':
                    reashenir = True
                if boolka == None:
                    reashenir = False
                if reashenir != None:
                    print("3e", boolka)
                    itog = find.NallSize(int(id), reashenir)
                    if itog == True:
                        return render(req, "Bot_message.html", context={"text": "Наличие изменено"})
                    else:
                        return render(req, "Bot_messageBad.html", context={
                            "text": "Не удалось изменить наличие !"})
        if req.POST.get('addrent') == '1':
            itog = find.AddRent(id)
            if itog == True:
                return render(req, "Bot_message.html", context={"text": "Аренда добавлена"})
            else:
                return render(req, "Bot_message.html", context={"text": "Аренда не добавлена"})
        if req.POST.get('dellrent') == '1':
            id = req.POST.get('iddellrent',None)
            if id !=None:
                itog = find.DellRent(int(id))
                if itog == True:
                    return render(req, "Bot_message.html", context={"text": "Аренла удалена!"})
                else:
                    return render(req, "Bot_messageBad.html", context={
                        "text": "Не удалось удалить данные."})

    else:
        dannye = find.GetTovar(id)
        return  render(req, "Bot_Card-Tovars.html", context=dannye)

def NalichieTovar(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    try:
        ed = EditTovar(req)
        itog = ed.Nalichie(id,True)
        if itog == False:
            return sory('Не удалось произвести операцию "В наличии/Не в наличии"')
        return HttpResponseRedirect('/admtovar/' + str(id))
    except:
        return sory('Не удалось произвести операцию "В наличии/Не в наличии"')

def NenalichieTovar(req,id):

    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    try:
        ed = EditTovar(req)
        itog = ed.Nalichie(id,False)
        if itog == False:
            return sory('Не удалось произвести операцию "В наличии/Не в наличии"')
        return HttpResponseRedirect('/admtovar/' + str(id))
    except:
        return sory('Не удалось произвести операцию "В наличии/Не в наличии"')



def AdmEdTov(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    edit =  EditTovar(req)
    if(req.method=="POST"):
        add = edit.ProverkaAdd()
        if add != False:
            return HttpResponseRedirect('/admtovar/' + str(add))
    dannye = edit.addTovar()
    return  render(req, "Bot_Add_tovar.html", context=dannye)

def EditTov(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    edit =  EditTovar(req)
    if(req.method=="POST"):
        itog = edit.AddEditForm(id)
        if itog==True:
            return HttpResponseRedirect('/admtovar/' + str(id))
        else:
            dannye = edit.EditForm(id)
            return render(req, "Bot_Edit_tovar.html", context=dannye)
    dannye = edit.EditForm(id)
    return  render(req, "Bot_Edit_tovar.html", context=dannye)

def EditTovPhoto(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')


    edit= EditTovar(req)
    if req.method == "POST":
        if req.POST.get('add', None) == "1":
            file = req.FILES.get('photo', None)
            bool = req.POST.get('main', None)
            if bool == "on":
                bool = True
            else:
                bool = False
            if file != None and bool != None:
                itog = edit.AddPhotoTovar(file, id, bool)
                if itog:
                    return HttpResponseRedirect('/admtovar/' + str(id))
                else:
                    pass
        if req.POST.get('maine', None) != None:
            idpho = int(req.POST.get('maine'))
            itog = edit.MainPhoto(idpho, id)

        if req.POST.get('delet', None) != None:
            idpho = int(req.POST.get('delet'))
            itog = edit.DellPhoto(idpho, True)

        if req.POST.get('Nodelet', None) != None:
            idpho = int(req.POST.get('Nodelet'))
            itog = edit.DellPhoto(idpho, False)




    dannye = edit.PhotoTovar(id)
    return render(req, "Bot_Edit_tovar_Photo.html", context=dannye)


def GetPerson(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    adm = adminClident(req)
    dannye = adm.GetClient()
    return render(req, "Bot_spispok-clientov.html", context=dannye)

def AdmMaxPerson(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    client = adminikardclient(req)
    if req.method=="POST":
        itog = False
        if req.POST.get('Moroz') == '1':
            itog = client.Zamorozka(id,True)
        if req.POST.get('Moroz') == '0':
            itog = client.Zamorozka(id,False)
        if req.POST.get('Add') =='on':
            itog = client.Balance(id)
        if req.POST.get('Password') == '1':
            itog = client.EditPassword(id)
        if req.POST.get('Zakaz') == '1':
            zak = Zakazi(req)
            ide = req.POST.get('id',None)
            date = req.POST.get('date',None)
            itog = zak.AddZakaz(idperson=ide, date=date)
            if itog!=False:
                return HttpResponseRedirect('/admzakaz/' + str(itog))


        if itog==False:
            return sory('Не удалось провести операцию')


    dannye = client.GetKardClientMax(id)
    return render(req, "Bot_Card-klient.html", context=dannye)

def AdminspisokOtz(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')
    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    otz = adminOtzivi(req)
    dannye = otz.GetOtz()
    return render (req,"Bot_spispok-otz.html", context=dannye )

def AdmOtz(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    otz = adminOtzivi(req)
    if req.method == "POST":
        print(req.POST)
        if req.POST.get('Delete') == '1':
            otz.DeleteOtz(id,True)
        if req.POST.get('Delete') == '0':
            otz.DeleteOtz(id,False)
        if req.POST.get('Razresh') == '1':
            otz.Razresh(id,True)
        if req.POST.get('Razresh') == '0':
            otz.Razresh(id,False)
        if req.POST.get('textotvet') !=None:
            otz.OtvetOtz(id, req.POST.get('textotvet'))
        if req.POST.get('DellOtvet') !=None:
            otz.DellOtvetOtz(id)

    dann = otz.OneOtz(id)
    return render(req, "Bot_Card-Otz.html", context=dann)

def AdmAddOtz(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    obr = adminOtzivi(req)
    if req.method == 'POST':
        save = obr.saveOtz()
        if save==True:
            return HttpResponseRedirect('/admnotzivi/')
        if save==False:
            return sory("Не удалось добавить отзыв (")
    form = obr.addOtz(id)
    return  render(req,"Bot_Add_Otz.html", context=form)

def AdmEditOtz(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    obr = adminOtzivi(req)
    if req.method == 'POST':
        save = obr.saveEditOtz(id)
        if save==True:
            return HttpResponseRedirect('/admnotziv/'+ str(id))
        if save==False:
            return sory("Не удалось добавить отзыв (")
    form = obr.editOtz(id)
    return  render(req,"Bot_Edit_Otz.html", context=form)

def AdmAddSize(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    obr = KardTovarFull(req)
    if req.method == "POST":
        result = obr.SaveAddSize(id)
        if result:
            return HttpResponseRedirect("/admnkardperson/" + str(id))
        return sory("Не удалось добавить размер")
    dann = obr.AddSize(id)
    return render(req,"Bot_Edit_Size.html", context=dann)

def AdmEditPerson(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    obr = adminikardclient(req)
    if req.method == "POST":
        result = obr.SavePerson(id)
        if result:
            return HttpResponseRedirect("/admnkardperson/" + str(id))
        return sory("Не удалось редактировать пользователя")
    dann = obr.EditPerson(id)
    dann.update({'id':id})
    return render(req,"Bot_Edit_Person.html", context=dann)

def AdmPaid(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    obr = Paid(req)

    dann = obr.GetPaid()
    return  render(req,"Bot_spispok-paid.html", context=dann)

def GetJournal(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    journ = journal(req)
    dann = journ.GetTranz()
    return  render(req, "Bot_spispok-journal.html", context=dann)

def EditJournal(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    journ = journal(req)

    if req.method == "POST":
        itog = journ.SaveEdit(id)

    dann = journ.Edit(id)
    return render(req, "Bot_edit-journal.html", context=dann)


def zakaz(req, id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    zak = Zakazi(req)



    if req.method == "POST":
        if req.POST.get('delltovar',None) == '1':
            ide = req.POST.get('id',None)
            if ide !=None:
                itog = zak.DellZakaz(ide)

        if req.POST.get('otmena', None) == '1':
            itog = zak.otmenazakaz(id,False)

        if req.POST.get('nootmena', None) == '1':
            itog = zak.otmenazakaz(id, True)

        if req.POST.get('vidacha', None) == '1':
            itog = zak.vidacha(id)

        if itog == False:
            return sory('Не удалось удалить товар из заказа. Пожалуйста обратитесь к системному администратору')

    dann = zak.GetZakaz(id)
    return  render(req,'Bot_Card-zakaza.html', context=dann)

def TovarZakaz(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    zak = Zakazi(req)
    if req.method == 'POST':
        if req.POST.get('tovar',None) !=None:
            tovar = req.POST.get('tovar',None)
            dann = zak.SizeTovar(int(tovar),id)
            return render(req, 'Bot_ZakazAddSize.html', context=dann)
        if req.POST.get('addtov',None) == "1":
            zakaz = id;
            tovarid = req.POST.get('rent',None)
            size = req.POST.get('size',None)
            itog = zak.AddZakazTovar(tovarid,zakaz,size)
            if itog== False:
                return sory("Не удалось добавить товар в заказ (")

    dann = zak.TovarZakaz(id)
    return render(req, 'Bot_AddTovarZakaz.html', context=dann)

def GetZakazi(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status != "Админ":
        return HttpResponseRedirect('/main/')

    zak = Zakazi(req)
    dannye = zak.getmassZakaz()
    return render(req, 'Bot_spispok-Zakazov.html', context=dannye)

def GetPaid(req,id):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')

    if req.user.person.Status !="Админ":
        return HttpResponseRedirect('/main/')

    pa = Paid(req)
    if req.method == "POST":
        itog = False
        if req.POST.get('block', None) == '1':
            itog = pa.Block(id, False)
        if req.POST.get('unblock', None) == '1':
            itog = pa.Block(id, True)
        if itog == False:
            return sory('Не удалось заблокировать/разблокировать :(')

    danney = pa.GetOnePaid(id)
    return render(req,'Bot_Card-paid.html', context=danney)

def ZakazClient(req,id):

    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')


    zak = Zakazi(req)
    if req.method == "POST":
        if req.POST.get('delltovar',None) == '1':
            ide = req.POST.get('id',None)
            if ide !=None:
                itog = zak.DellZakaz(ide)

        if req.POST.get('otmena', None) == '1':
            itog = zak.otmenazakaz(id,False)

        if req.POST.get('nootmena', None) == '1':
            itog = zak.otmenazakaz(id, True)

    dannye = zak.GetZakazKlient(id)
    return render(req, 'Dostavka_v2.html', context=dannye)

def Registr(req):
    zareg = Reg(req)
    if req.method == "POST":
        itog = zareg.RegGo()
        if itog:
            return HttpResponseRedirect('/auto/')
        else:
            return  sory('Извините, такой логин или такая почта уже имеются в базе ( !')
    dannye = zareg.GetReg()
    return render(req, 'Registration.html', context=dannye)

def Vihod(req):
    if not req.user.is_authenticated:
        return HttpResponseRedirect('/auto/')
    logout(req)
    return HttpResponseRedirect('/auto/')
