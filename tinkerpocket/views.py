from django.shortcuts import render

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        # request.session['stats'] = initial_weapons()
        print('Session setup')
    return render(request, 'tinkerpocket/index.html')