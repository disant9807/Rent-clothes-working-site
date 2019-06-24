from django import forms
from datetime import timedelta, datetime
from .models import Size
from django.forms import DateTimeInput

class PersonForm(forms.Form):
    name = forms.CharField(max_length=100, label="Имя")
    sex = forms.ChoiceField(choices=((1, "Мужчина"), (2, "Женщина")), label="Пол")
    DateAge = forms.DateField(label="Дата рождения", widget = forms.SelectDateWidget())
    Email = forms.CharField(label="Email")
    Phone = forms.IntegerField(label="Телефон",min_value=1,required=False)
    Vk = forms.CharField(label="Вконтакте",required=False)
    Insta = forms.CharField(label="Инстаграм",required=False)


class otzyvForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())
    rating = forms.ChoiceField(choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")  ))


class EditTovarForm(forms.Form):
    name = forms.CharField(label="Название", required=True)
    opisanie = forms.CharField(widget=forms.Textarea(), label="Описание товара", required=True)
    material = forms.CharField(widget=forms.Textarea(), label="Описание материала")
    vidtovars = forms.MultipleChoiceField(label="Тип товара", required=True, choices=(("Куртки", "Куртки"), ("Пальто", "Пальто"),("Ветровки", "Ветровки"),
                                                               ("Пуховики","Пуховики"),("Худи","Худи"),("Жакеты","Жакеты"),("Майки","Майки"),
                                                               ("Рубашки","Рубашки"),("Джинсы","Джинсы"),("Трико","Трико"),("Джоггеры","Джоггеры"),
                                                               ("Классика","Классика"),("Кроссовки","Кроссовки"),("Кеды","Кеды"),("Ботинки","Ботинки"),
                                                               ("Туфли","Туфли")))

    brand = forms.CharField(label="Бренд", required=True)
    sex = forms.ChoiceField(label="Пол", required=True, choices=((1,'Мужской'),(2,'Женский'),(3,'Унисекс')))
    seaz = forms.MultipleChoiceField(choices=(("Весна", "Весна"),("Зима",'Зима'),("Осен","Осен"),("Лето","Лето")), required=True)
    main = forms.FileField(label=u'Главная фотография', widget=forms.FileInput())

    def process(self):
        cd = self.cleaned_data
        return cd

class FilterPadiForm(forms.Form):

    prynatie = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    neprynatie = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    plusminus = forms.ChoiceField(label="Тип", choices=((True,"Пополнение"),(False,"Списание")), required=False)
    datemin = forms.DateTimeField(label="Дата от", required=False)
    datemax = forms.DateTimeField(label="Дата до", required=False)
    moneymin = forms.DateTimeField(label="Сумма от", required=False)
    moneymax = forms.DateTimeField(label="Сумма до", required=False)
    tovar = forms.CharField(label="Название товара", required=False)
    client = forms.CharField(label="Клиент", required=False)


class AddPhotoTovar(forms.Form):
    photo = forms.FileField(required=True, widget=forms.FileInput())
    main = forms.BooleanField(required=False, widget=forms.CheckboxInput())

class FormJournal(forms.Form):

    def GetSize(self):
        siz = Size.objects.all()

        hz = []

        for s in siz:
            hz.append((s.name,s.name))
        return hz

    def __init__(self, *args, **kwargs):
        super(FormJournal, self).__init__(*args, **kwargs)
        self.fields["size"].choices = (
            self.GetSize()
        )
    plus = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Операции добавления")
    minus = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Операции списания")
    size = forms.MultipleChoiceField( label="Размеры", required=False)
    DateMin = forms.DateTimeField(required=False, label="Дата от",widget=DateTimeInput(attrs={'id': 'date1'}))
    DateMax = forms.DateTimeField(required=False, label="Дата до", widget=DateTimeInput(attrs={'id': 'date2'}))
    minCena = forms.FloatField(required=False, label="Минимальная цена")
    maxCena = forms.FloatField(required=False, label="Максимальная цена")
    tovar = forms.CharField(required=False, label="Товар")
    Client = forms.CharField(required=False, label="Клиент")
    str = forms.IntegerField(required=True, initial=1)
    kolich = forms.IntegerField(required=False, initial=10)


class FormOtzivi(forms.Form):
    Client = forms.CharField(required=False)
    Vesh = forms.CharField(required=False)
    one = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck4'}))
    two = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck5'}))
    three = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck6'}))
    fo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck7'}))
    five = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck8'}))
    ok = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck1'}))
    no = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck2'}))
    wtf = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck3'}))
    delete = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'defaultCheck9'}))

    kolich = forms.IntegerField(required=False, initial=10)

class SortClient(forms.Form):
    sort = forms.ChoiceField(required=True, choices=(('bird','Дата Рождения'),('balance','Баланс'),('schmotki','Число шмоток'),('paid','Общая плата')))
    sortingType = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    str = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'value': '1'}))
    kolich = forms.IntegerField(initial=10, min_value=1, widget=forms.NumberInput(attrs={'value': '10'}))

class SortTovars(forms.Form):
    sort = forms.ChoiceField(required=True, choices=(('arenda','Стоимость аренды'),('stoimost','Стоимость'),('like','Количество лайков'),('DateAdd','Дата'),('paid','Количество заказов')))
    sortingType = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    str = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'value': '1'}))
    kolich = forms.IntegerField(initial=10, min_value=1, widget=forms.NumberInput(attrs={'value': '10'}))

class SortOtz(forms.Form):
    sort = forms.ChoiceField(required=True, choices=(('date','Дата'),('zvezdi','Рейтинг')))
    sortingType = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    str = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'value': '1'}))
    kolich = forms.IntegerField(initial=10, min_value=1, widget=forms.NumberInput(attrs={'value': '10'}))

class SortZakaz(forms.Form):
    sort = forms.ChoiceField(required=True, choices=(('date', 'Дата'),('date','Дата')))
    sortingType = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    str = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'value': '1'}))
    kolich = forms.IntegerField(initial=10, min_value=1, widget=forms.NumberInput(attrs={'value': '10'}))


class SortOperations(forms.Form):
    sort = forms.ChoiceField(required=True, choices=(('date', 'Дата'),('money','Сумма'),('plusminus','Тип')))
    sortingType = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    str = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'value': '1'}))
    kolich = forms.IntegerField(initial=10, min_value=1, widget=forms.NumberInput(attrs={'value': '10'}))

class FindZakaz(forms.Form):
    datemin = forms.DateTimeField(required=False)
    datemax = forms.DateTimeField(required=False)
    person = forms.CharField(required=False)
    raz = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    unraz = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    code = forms.CharField(required=False)
    vidan =  forms.BooleanField(required=False, widget=forms.CheckboxInput())
    noVidan = forms.BooleanField(required=False, widget=forms.CheckboxInput())

class FrontFind(forms.Form):
    name = forms.CharField()
    brand = forms.CharField()


class FindClient(forms.Form):
    name = forms.CharField(required=False)
    phone = forms.IntegerField(required=False, min_value=1)
    monmin = forms.IntegerField(required=False, min_value=1)
    monma = forms.IntegerField(required=False, min_value=1)
    minprice = forms.FloatField(required=False, min_value=0)
    maxprice = forms.FloatField(required=False, min_value=0)
    minvesh = forms.IntegerField(required=False, min_value=0)
    maxvesh = forms.IntegerField(required=False, min_value=0)
    monmin = forms.FloatField(required=False, min_value=0)
    monma = forms.FloatField(required=False, min_value=0)
    man = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    woman = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    moroz = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    razmoroz = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class Registration(forms.Form):
    sex = forms.ChoiceField(required=True, choices=((True,'Мужской'),(False,'Женский')), widget=forms.Select())
    phone = forms.IntegerField(required=True, widget=forms.NumberInput())
    Email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    Bird = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'id': 'datepicker'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    login = forms.CharField(required=True)

    def process(self):
        cd = self.cleaned_data
        return cd