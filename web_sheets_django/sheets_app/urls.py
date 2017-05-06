
from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^sheet/(?P<sheet_id>[^/]+)/$', views.sheet, name='sheet'),
            url(r'^set_cell/(?P<sheet_id>[^/]+)/$',
                views.set_cell, name='set_cell'),
            url(r'^set_exec/(?P<sheet_id>[^/]+)/$',
                views.set_exec, name='set_exec'),
            url(r'^add_column/(?P<sheet_id>[^/]+)/$',
                views.add_column, name='add_column'),
            ]

