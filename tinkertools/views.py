from django.shortcuts import render

# Create your views here.


def index(request):
    print('here')
    return render(request, 'tinkertools/index.html')