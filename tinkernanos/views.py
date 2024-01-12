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

            try: level = int(data.get('level'))
            except: level = 1
            if level is not None and 1 <= level <= 220: request.session['stats']['level'] = level

            try: spec = int(data.get('specialization'))
            except: spec = 0
            if spec is not None and 0 <= spec <= 8: request.session['stats']['specialization'] = spec

            try: subscription = int(data.get('subscription'))
            except: subscription = 0
            if subscription is not None and 0 <= subscription <= 128: request.session['stats']['subscription'] = subscription

            try: mm = int(data.get('mm'))
            except: mm = 0
            if mm is not None and 0 <= mm : request.session['stats']['mm'] = mm

            try: bm = int(data.get('bm'))
            except: bm = 0
            if bm is not None and 0 <= bm : request.session['stats']['bm'] = bm

            try: mc = int(data.get('mc'))
            except: mc = 0
            if mc is not None and 0 <= mc : request.session['stats']['mc'] = mc

            try: ts = int(data.get('ts'))
            except: ts = 0
            if ts is not None and 0 <= ts : request.session['stats']['ts'] = ts

            try: pm = int(data.get('pm'))
            except: pm = 0
            if pm is not None and 0 <= pm : request.session['stats']['pm'] = pm

            try: si = int(data.get('si'))
            except: si = 0
            if si is not None and 0 <= si : request.session['stats']['si'] = si

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

            return JsonResponse({'success': True, 'message': '', 'stats' : request.session['stats'], 'nanos' : retlist})
            
        except Exception as e:
            #if DEBUG:
            import traceback
            traceback.print_exc()

            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})
