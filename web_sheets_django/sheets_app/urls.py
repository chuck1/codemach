
from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^sheet/(?P<sheet_id>)/$', views.sheet, name='sheet'),
            url(r'^set_cell$', views.set_cell, name='set_cell'),
            url(r'^add_column$', views.add_column, name='add_column'),
            ]

