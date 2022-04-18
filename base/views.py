from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm
"""""
rooms = [
    {'id': 1, 'name': 'Let\' learn Python'},
    {'id': 2, 'name': 'Let\' learn C'},
    {'id': 3, 'name': 'Let\' learn Javascript'},
]
"""

def loginPage(request): #be careful because there are built in function name login
    
    if request.method == 'POST':
        usernamee = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=usernamee)
        except:
            messages.error(request, 'User is not exist!')
        
        user = authenticate(request, username=usernamee, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name or password does not exist')
    context={}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
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
    
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        #print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        #request.POST.get('name')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk): 
    room = Room.objects.get(id=pk) 
    form = RoomForm(instance=room) #refill the text
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

