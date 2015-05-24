from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       # URL pattern for the AnimalDocumentUploadView
                       url(regex=r'^records-animaldocument-upload/$',
                           view=views.AnimalDocumentUploadView.as_view(),
                           name='records.animaldocument_upload'
                           ),
                       # URL pattern for the AnimalDocumentListView
                       url(regex=r'^records-animaldocument-list/$',
                           view=views.AnimalDocumentListView.as_view(),
                           name='records.animaldocument_list'
                           ),
                       # URL pattern for the AnimalDocumentDeleteView
                       url(regex=r'^records-animaldocument-delete/(?P<pk>\d+)/$',
                           view=views.AnimalDocumentDeleteView.as_view(),
                           name='records.animaldocument_delete'
                           ),
                       )


urlpatterns.extend(views.AnimalNoteCRUDL().as_urlpatterns())

