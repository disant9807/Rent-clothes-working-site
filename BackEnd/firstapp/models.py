from django.db import models
from django.db.models import Q
from django.forms import ModelForm,Textarea,Select, SelectDateWidget,DateTimeInput, inlineformset_factory, CheckboxInput, FileInput, NumberInput
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date




class Brand (models.Model):
    name = models.CharField(db_index=True,max_length=100)
    def __str__(self):
        return u'{0}'.format(self.name)

class TypeTovars (models.Model):
    name = models.TextField(db_index=True)
    def __str__(self):
        return u'{0}'.format(self.name)

class Sex (models.Model):
    name = models.TextField()
    def __str__(self):
        return u'{0}'.format(self.name)

class Tovar (models.Model):
    name = models.CharField(db_index=True,max_length=100)
    Opisanie = models.TextField()
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL, null=True)
    DateAdd = models.DateTimeField()
    DateEdit = models.DateTimeField()
    Sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    Material = models.TextField(null=True)
    Del = models.BooleanField()
    def __str__(self):
        return u'{0}'.format(self.name)

class Set(models.Model):
    name = models.CharField(db_index=True,max_length=100)
    text = models.TextField()
    DateAdd = models.DateTimeField()
    DateEdit = models.DateTimeField()
    Sex = models.BooleanField(null=True)

class TovarTypeTovar(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    typpe = models.ForeignKey(TypeTovars, on_delete=models.CASCADE)



class VidArendi (models.Model):
    name = models.CharField(max_length=50)
    vikup = models.BooleanField()
    opisanie = models.TextField()
    def __str__(self):
        return u'{0}'.format(self.name)

class Person(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, null=True)
    sex = models.BooleanField(null=True)
    phone = models.IntegerField(null=True)
    Vk = models.TextField(null=True);
    Insta = models.TextField(null=True);
    Status = models.CharField(max_length=20,null=True)
    DateReg = models.DateField(null=True);
    DataLast = models.DateTimeField(null=True);
    Zamoroz = models.BooleanField(null=True);
    Email = models.TextField(null=True)
    name = models.CharField(db_index=True,max_length=300)
    PhotoPerson = models.TextField(null=True)
    Bird = models.DateField(null=True)
    Adress = models.TextField(null=True)
    balance = models.FloatField(null=True)

    class Meta:
        unique_together = ( 'Email',)

    objects = models.Manager()
    def __str__(self):
        return u'{0}'.format(self.name)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    DateReg = models.DateField(null=True);
    DataLast = models.DateTimeField(null=True);
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField()

class VidArendiTovars (models.Model):
    set = models.ForeignKey(Set,on_delete = models.CASCADE, null=True)
    tovar = models.ForeignKey(Tovar,on_delete = models.CASCADE, null= True)
    vidArendi = models.ForeignKey(VidArendi, on_delete=models.CASCADE)
    stoimost = models.FloatField();
    vikup = models.IntegerField(null=True);
    Vozvrat = models.IntegerField();
    platej = models.IntegerField();
    def __str__(self):
        return u'{0}'.format(self.vidArendi.name)



class PhotoTovara (models.Model):
    photo = models.FileField()
    tovar = models.ForeignKey(Tovar,on_delete = models.CASCADE, null=True)
    set = models.ForeignKey(Set, on_delete= models.CASCADE, null=True)
    main = models.BooleanField(null=True)
    delete = models.BooleanField()


class TovarsSets(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    tovars = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    skidka = models.FloatField()


class LikePerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.SET_NULL, null=True)
    sets = models.ForeignKey(Set, on_delete=models.SET_NULL, null=True)


class Otziv (models.Model):
    Opisanie = models.TextField(db_index=True)
    zvezdi = models.IntegerField()
    Person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    Tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    Set = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)
    Status = models.TextField()
    delete = models.BooleanField(null=True)
    Otvet = models.TextField(null=True)
    nameperson = models.TextField(null=True)


class Size(models.Model):
    name = models.TextField()
    def __str__(self):
        return u'{0}'.format(self.name)


class SizeTovars(models.Model):
    Size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    Tovar = models.ForeignKey(Tovar,on_delete = models.CASCADE, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)
    nalichie = models.BooleanField()

    def __str__(self):
        return u'{0}'.format(self.Size.name)

class TovarPerson(models.Model):
    VidArendiTovars = models.ForeignKey(VidArendiTovars, on_delete=models.CASCADE)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    Data = models.DateTimeField();
    size = models.TextField();

class AddTovars(models.Model):
    date = models.DateTimeField()
    client = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    tovar = models.ForeignKey(Tovar, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(SizeTovars, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField()
    PlusMinus = models.BooleanField()

class AddPaid(models.Model):
    status = models.BooleanField()
    plusminus = models.BooleanField()
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    date = models.DateTimeField()
    money = models.FloatField()
    tovPer = models.ForeignKey(TovarPerson, on_delete=models.SET_NULL, null=True)


class Seaz(models.Model):
    name = models.TextField()


class SezonTovar(models.Model):
    seaz = models.ForeignKey(Seaz,on_delete = models.CASCADE, null=True)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)

class Korzina(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class TovarsKorzine(models.Model):
    tovar = models.ForeignKey(VidArendiTovars, on_delete=models.CASCADE)
    korzina = models.ForeignKey(Korzina, on_delete=models.CASCADE)

class Zakaz(models.Model):
    status = models.BooleanField()
    nomer = models.TextField()
    date = models.DateTimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    vidann = models.BooleanField()

    class Meta:
        unique_together = ('nomer',)

class TovarsZakaz(models.Model):
    zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE)
    tovar = models.ForeignKey(VidArendiTovars, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeTovars, on_delete=models.CASCADE)

class Vidacha(models.Model):
    client = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateTimeField()
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    status = models.BooleanField()
    comment = models.TextField(null=True)
    zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE)

class AddVidachaForm(ModelForm):
    class Meta:
        model = Vidacha
        fields = ['client','date','manager','status','comment','zakaz']

class ZakaForm(ModelForm):
    class Meta:
        model = Zakaz
        fields = ['date','person']


class OtzForm(ModelForm):
    class Meta:
        model = Otziv
        fields = ['Opisanie', 'zvezdi', 'date', 'nameperson','Tovar','Status']
        widgets = {
            'nameperson': Textarea(attrs={'cols': 80, 'rows': 1}),
            'zvezdi': Select(choices=((1,'1 звезда'),(2,'2 звезды'),(3,'3 звезды'),(4,'4 звезды'),(5,'5 звезд'))),
            'date': SelectDateWidget(years=range(datetime.today().year-50,datetime.today().year+50)),
        }

class EditOtzForm(ModelForm):
    class Meta:
        model = Otziv
        fields = ['Opisanie', 'zvezdi', 'date','Tovar','Status']
        widgets = {
            'zvezdi': Select(choices=((1,'1 звезда'),(2,'2 звезды'),(3,'3 звезды'),(4,'4 звезды'),(5,'5 звезд'))),
            'date': SelectDateWidget(years=range(datetime.today().year-50,datetime.today().year+50)),
        }

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['sex','phone','Email','name','Bird','Adress']

class SizeForm(ModelForm):

    def __init__(self,idd, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)
        size = []

        if idd != None:
            tovar = Tovar.objects.filter(id=idd)
            if len(tovar)>0:
                sizetovar = tovar[0].sizetovars_set.all()
            self.fields['size'].queryset = tovar[0].sizetovars_set.all()

    class Meta:
        model = AddTovars
        fields = ['count','size','tovar','date', 'client','PlusMinus']
        widgets = {
            'date':DateTimeInput(attrs={'id': 'datepicker'}),
        }

class AddSizeTov(ModelForm):

    def __init__(self,idd, *args, **kwargs):
        super(AddSizeTov, self).__init__(*args, **kwargs)
        size = []

        if idd != None:
            tovar = Tovar.objects.filter(id=idd)
            if len(tovar)>0:
                sizetovar = tovar[0].sizetovars_set.all()
                for t in sizetovar:
                    size.append(t.Size.name)
            self.fields['Size'].queryset = Size.objects.filter(~Q(name__in=size))

    class Meta:
        model = SizeTovars
        fields = ['Size','Tovar','nalichie']


class AddArendaTovars(ModelForm):

    def __init__(self,idd, *args, **kwargs):
        super(AddArendaTovars, self).__init__(*args, **kwargs)
        vid = []

        if idd != None:
            tovar = Tovar.objects.filter(id=idd)
            if len(tovar)>0:
                vidarendi = tovar[0].vidarenditovars_set.all()
                for t in vidarendi:
                    vid.append(t.vidArendi.name)
            self.fields['vidArendi'].queryset = VidArendi.objects.filter(~Q(name__in=vid))

    class Meta:
        model = VidArendiTovars
        fields = ['tovar','vidArendi','stoimost','vikup','Vozvrat','platej']



class AddTovar(ModelForm):
    class Meta:
        model = Tovar
        fields = ['name', 'Opisanie', 'brand', 'DateAdd', 'DateEdit', 'Sex','Material']


class EditPerson(ModelForm):
    class Meta:
        model = Person
        fields = ['sex','phone','Vk','Insta','Status','Zamoroz','Email','name','Bird','Adress']

class AddZakaz(ModelForm):
    class Meta:
        models = Zakaz
        fields = ['nomer','date','person']

class EditPersonKlient(ModelForm):
    class Meta:
        model = Person
        fields = ['name','Bird','sex','Email','phone']
        widgets = {
            'sex': Select(choices=((True,'Мужской'),(False,'Женский'))),
            'phone': NumberInput(attrs={'min': '0'}),
            'Bird' : DateTimeInput(attrs={'id': 'datepicker'})
        }