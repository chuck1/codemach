
from django.conf.urls import url

from . import views

urlpatterns = [
            url(
                r'^$', 
                views.index, 
                name='index'),
            url(
                r'^book_new$', 
                views.book_new, 
                name='book_new'),
            url(
                r'^book/(?P<book_id>[^/]+)/$', 
                views.BookViewView.as_view(), 
                name='book'),
            url(
                r'^set_cell/(?P<book_id>[^/]+)/$',
                views.SetCellView.as_view(),
                name='set_cell'),
            url(
                r'^set_script_pre/(?P<book_id>[^/]+)/$',
                views.SetScriptPreView.as_view(),
                name='set_script_pre'),
            url(
                r'^add_column/(?P<book_id>[^/]+)/$',
                views.AddColumnView.as_view(),
                name='add_column'),
            url(
                r'^add_row/(?P<book_id>[^/]+)/$',
                views.AddRowView.as_view(),
                name='add_row'),
            url(
                r'^get_sheet_data/(?P<book_id>[^/]+)/$',
                views.GetSheetDataView.as_view(),
                name='get_sheet_data'),
            url(
                r'^book_demo/(?P<book_demo_name>[^/]+)/$',
                views.book_demo,
                name='book_demo'),
            ]

