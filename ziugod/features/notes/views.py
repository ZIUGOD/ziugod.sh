from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def index(request):
    now = datetime.now()
    html = "<html lang='pt-br'><body>Ti is now %s.</body></html>" % now

    return HttpResponse(html)
