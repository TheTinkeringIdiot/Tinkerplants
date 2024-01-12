from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerfite.utils import *
from tinkernanos.utils import *
from tinkernukes.utils import *

from tinkernanos.models import *

import json, math

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        request.session['stats'] = initial_nanos()
        print('Session setup')
    return render(request, 'tinkernanos/index.html')

def update_stats(request):
    if request.method == 'POST':
        try:
            if request.session.get('stats') is None:
                return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})
            
            data = json.loads(request.body)

            try: profession = int(data.get('profession'))
            except: profession = 0
            if profession is not None and 0 <= profession <= 15: request.session['stats']['profession'] = profession
            try: subscription = int(data.get('subscription'))
            except: subscription = 0
            if subscription is not None and 0 <= subscription <= 128: request.session['stats']['subscription'] = subscription

            prof = request.session['stats']['profession']
            sub = request.session['stats']['subscription']

            if sub <= 0:
                class_nanos = Nano.objects.filter(profession=prof, expansion__lte=sub, level__lte=200, spec__lte=0).all()
            else:
                class_nanos = Nano.objects.filter(profession=prof, expansion__lte=sub).all()

            nanolist = [x.json() for x in class_nanos]
            nanolist = sorted(nanolist, key=lambda x: (x['strain_name'], -x['ql']))

            retlist = []
            for nano in nanolist:
                nano['spec'] = SPECS[nano['spec']]
                nano['expansion'] = SHORT_EXPANSIONS[nano['expansion']]
                if nano['level'] == 1:
                    nano['level'] = ''

                retlist.append(nano)

            return JsonResponse({'success': True, 'message': '', 'data' : retlist})
            
        except Exception as e:
            #if DEBUG:
            import traceback
            traceback.print_exc()

            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})
