from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
"""
rooms = [
    {'id': 1, 'name': 'Let\' learn Python'},
    {'id': 2, 'name': 'Let\' learn C'},
    {'id': 3, 'name': 'Let\' learn Javascript'},
]
"""


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
def room(request, pk):
    """
    room = None
    for i in roos:
        if i['id'] == int(pk):
    """
    room = Room.objects.get(id=pk)
    context = {'room': room}
    print (context)
    return render(request, 'base/room.html', context)
# Create your views here.
