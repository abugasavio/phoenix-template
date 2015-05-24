# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from phoenix.apps.animals.views import AnimalCRUDL

# Comment the next two lines to disable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',  # noqa
    # Your stuff: custom urls includes go here
    url(r'^$', AnimalCRUDL.List.as_view()),
    url(r'^finances/', include('phoenix.apps.finances.urls')),
    url(r'^records/', include('phoenix.apps.records.urls')),
    url(r'^health/', include('phoenix.apps.health.urls')),
    url(r'^animals/', include('phoenix.apps.animals.urls')),
    # Django Admin (Comment the next line to disable the admin)
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include('smartmin.users.urls')),
    # Third party URLs
    (r'^select2/', include('django_select2.urls')),



) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
