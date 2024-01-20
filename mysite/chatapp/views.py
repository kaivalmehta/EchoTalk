
from .models import ChatRoom,ChatMessage
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChatRoomForm
from django.utils.text import slugify


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/rooms/')  # Redirect to your chat page or wherever you want to go after login
    else:
        form = AuthenticationForm()
    return render(request, 'chatapp/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/rooms/')  # Redirect to your chat page or wherever you want to go after signup
    else:
        form = UserCreationForm()
    return render(request, 'chatapp/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page or wherever you want to go after logout

def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request,'chatapp/index.html',{'chatrooms':chatrooms})

def chatroom(request,slug):
    chatroom=ChatRoom.objects.get(slug=slug)
    messages= ChatMessage.objects.filter(room=chatroom)[0:30]
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':messages})

@login_required
def create_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.slug=slugify(room.name)
            room.save()
            return redirect('index')
    else:
        form = ChatRoomForm()

    return render(request, 'chatapp/create_app.html', {'form': form})
