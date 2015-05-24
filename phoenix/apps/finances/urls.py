from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
                       # URL pattern for the CategoryFormView
                       url(regex=r'^category/create/$',
                           view=views.CategoryFormView.as_view(),
                           name='finances.category_create'
                           ),
                       )
urlpatterns.extend(views.TransactionCRUDL().as_urlpatterns())