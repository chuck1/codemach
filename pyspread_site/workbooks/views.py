from django.shortcuts import render
from django.http import HttpResponse

import pyspreadservice
import pyspreadservice.request

# Create your views here.

def render_sheet(http_request, response):
    context = {"html": response.sheet.html(http_request)}
    return render(http_request, "workbooks/sheet.html", context)

def cell_change(http_request):

    cell = pyspreadservice.parse_cell(http_request.POST["cell"])
    text = http_request.POST["text"]

    print "cell", repr(cell)
    print "text", repr(text)

    request = pyspreadservice.request.RequestCellSet(http_request.session.session_key)
    request.cell = cell
    request.text = text

    response = pyspreadservice.send_request(request)

    print "response      ", repr(response)
    print "response sheet", repr(response.sheet)

    return render_sheet(http_request, response)

def sheet_add_row(http_request):

    request = pyspreadservice.request.RequestSheetAddRow(http_request.session.session_key)

    response = pyspreadservice.send_request(request)

    return render_sheet(http_request, response)

def sheet_add_col(http_request):

    request = pyspreadservice.request.RequestSheetAddCol(http_request.session.session_key)

    response = pyspreadservice.send_request(request)

    return render_sheet(http_request, response)

def sheet_show_value(http_request):

    request = pyspreadservice.request.RequestSheet(http_request.session.session_key, None)
    request.display_func = pyspreadservice.sheet.display_func_value

    response = pyspreadservice.send_request(request)

    return render_sheet(http_request, response)

def sheet_show_formula(http_request):

    request = pyspreadservice.request.RequestSheet(http_request.session.session_key, None)
    request.display_func = pyspreadservice.sheet.display_func_formula

    response = pyspreadservice.send_request(request)

    return render_sheet(http_request, response)



def test(http_request):

    print "POST", repr(http_request.POST)

    if "cell" in http_request.POST.keys():
        return cell_change(http_request)
    if "btn add row" in http_request.POST.keys():
        return sheet_add_row(http_request)
    if "btn add col" in http_request.POST.keys():
        return sheet_add_col(http_request)
    if "btn show value" in http_request.POST.keys():
        return sheet_show_value(http_request)
    if "btn show formula" in http_request.POST.keys():
        return sheet_show_formula(http_request)





    request2 = pyspreadservice.request.RequestSheet(http_request.session.session_key, "sheet1")

    response = pyspreadservice.send_request(request2)

    print "response      ", repr(response)
    print "response sheet", repr(response.sheet)

    return render_sheet(http_request, response)



