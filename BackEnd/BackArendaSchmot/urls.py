"""BackArendaSchmot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from firstapp import views


urlpatterns = [
    path('tovars/<int:Str>/', views.FindTovars),
    path('tovars/', views.FindTovars),
    path('tovar/<int:id>/', views.tovars),
    path('tovar/', views.tovars),
    path('sets/', views.Setssss),
    path('set/<int:id>/', views.SetOne),
    path('auto/', views.auto),
    path('kabinet/',views.kabinet),
    path('Edit/', views.edit),
    path('Editpass/', views.editPass),
    path('calend/', views.calend),
    path('history/',views.HistOper),
    path('korzina/', views.Korz),
    path('Otz/<int:id>/', views.tovarAddOT),
    path('zakaz/<int:id>/', views.ZakazClient),
    path('Registration/', views.Registr),
    path('Vihod/', views.Vihod),
    path('main/', views.main),
    path('/', views.main),


    path('admtovars/', views.AdmTovar),
    path('admtovar/<int:id>', views.AdmKardTovar),
    path('admaddsize/<int:id>', views.AdmAddSize),
    path('admedittov/', views.AdmEdTov),
    path('admnalichie/<int:id>', views.NalichieTovar),
    path('admnenalichie/<int:id>', views.NenalichieTovar),
    path('admntovaredit/<int:id>', views.EditTov),
    path('admntovarphoto/<int:id>', views.EditTovPhoto),
    path('admnpersons/', views.GetPerson),
    path('admnkardperson/<int:id>', views.AdmMaxPerson),
    path('admeditperson/<int:id>', views.AdmEditPerson),
    path('admnotzivi/', views.AdminspisokOtz),
    path('admnotziv/<int:id>', views.AdmOtz),
    path('admaddotz/<int:id>', views.AdmAddOtz),
    path('admeditotz/<int:id>', views.AdmEditOtz),
    path('admpaid/', views.AdmPaid),
    path('admjournal/', views.GetJournal),
    path('editadmjournal/<int:id>', views.EditJournal),
    path('admzakaz/<int:id>', views.zakaz),
    path('admtovarszakaz/<int:id>', views.TovarZakaz),
    path('admzakazi/',views.GetZakazi),
    path('admpaid/<int:id>',views.GetPaid)

]
