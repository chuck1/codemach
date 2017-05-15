
from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^book_new$', views.book_new, name='book_new'),
            url(r'^book/(?P<book_id>[^/]+)/(?P<sheet_key>[^/]+)/$', views.book, name='book'),
            url(
                r'^set_cell/(?P<book_id>[^/]+)/$',
                views.set_cell,
                name='set_cell'),
            url(
                r'^set_script_pre/(?P<book_id>[^/]+)/$',
                views.set_script_pre,
                name='set_script_pre'),
            url(
                r'^add_column/(?P<book_id>[^/]+)/$',
                views.add_column,
                name='add_column'),
            url(
                r'^add_row/(?P<book_id>[^/]+)/$',
                views.add_row,
                name='add_row'),
            url(
                r'^get_sheet_data/(?P<book_id>[^/]+)/$',
                views.get_sheet_data,
                name='get_sheet_data'),
            ]

