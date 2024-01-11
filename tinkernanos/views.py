from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerfite.utils import *
from tinkernanos.utils import *
from tinkernukes.utils import *

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        request.session['stats'] = initial_nanos()
        print('Session setup')
    return render(request, 'tinkernukes/index.html')