from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerpocket.models import *
# from tinkerpocket.utils import *


import json

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        # request.session['stats'] = initial_weapons()
        print('Session setup')
    return render(request, 'tinkerpocket/index.html')

def boss_info(request):
    if request.method == 'POST':
        boss_data = json.loads(request.body)
        name = boss_data['name']

        boss = Pocketboss.objects.filter(name=name)
        if boss is None or len(boss) != 1:
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        boss = boss[0]

        info = {}
        info['name'] = boss.name
        info['level'] = boss.level
        info['mobs'] = boss.mobs
        info['playfield'] = boss.playfield
        info['location'] = boss.location
        info['drops'] = []

        # if name == 'The Night Heart':
        #     breakpoint()

        for drop in boss.drops.all():
            info['drops'].append([drop.aoid, drop.name, drop.ql])
        
        return JsonResponse({'success': True, 'data': info})