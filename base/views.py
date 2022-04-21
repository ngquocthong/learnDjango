from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm
"""""
rooms = [
    {'id': 1, 'name': 'Let\' learn Python'},
    {'id': 2, 'name': 'Let\' learn C'},
    {'id': 3, 'name': 'Let\' learn Javascript'},
]
"""

def loginPage(request): #be careful because there are built in function name login
    page = 'login'
    if request.method == 'POST':
        usernamee = request.POST.get('username').lower()
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
    context={'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    #page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during the registration')

    return render(request, 'base/login_register.html', {'form':form})



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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #order_by('-created')


    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    """
    room = None
    for i in roos:
        if i['id'] == int(pk):
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()#order_by('-created') #Message.objects.filter(room=room).
    participants = room.participants.all() # many to many no need to _set
    
    #luồng chạy có bị thay đổi không?
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        ) 

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    return render(request, 'base/room.html', context)
    
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html' ,context)

@login_required(login_url='login')    
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        #print(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        #request.POST.get('name')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  
def updateRoom(request, pk): 
    room = Room.objects.get(id=pk) 
    form = RoomForm(instance=room) #refill the text

    if request.user != room.host:
        return HttpResponse("You do not have permission")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')  
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You do not have permission")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')  
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You do not have permission")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

