# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
)

urlpatterns.extend(views.AnimalCRUDL().as_urlpatterns())
urlpatterns.extend(views.ServiceCRUDL().as_urlpatterns())
urlpatterns.extend(views.PregnancyCheckCRUDL().as_urlpatterns())
urlpatterns.extend(views.MilkProductionCRUDL().as_urlpatterns())
urlpatterns.extend(views.BreedCRUDL().as_urlpatterns())
urlpatterns.extend(views.AnimalTreatmentCRUDL().as_urlpatterns())
urlpatterns.extend(views.AnimalTransactionCRUDL().as_urlpatterns())

