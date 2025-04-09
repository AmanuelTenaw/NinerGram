from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.


#rooms = [
#   {'id': 1, 'name': 'Lets learn python!'},
#   {'id': 2, 'name': 'Design with me'},
#   {'id': 3, 'name': 'Frontend developer'},
#]
 
def loginPage(request):
   page = 'login'
   if request.user.is_authenticated:
      return redirect('home')


   if request.method == 'POST':
      username = request.POST.get('username').lower()
      password = request.POST.get('password')

      try:
         user = User.objects.get(username=username)
      except:
         messages.error(request, 'User does not exist')
      user = authenticate(request, username = username, password=password)

      if user is not None:
         login(request, user)
         return redirect('home') 
      else:
         messages.error(request, 'Username OR password does not exist')

   context = {'page': page}
   return render(request, 'base/login_register.html', context)

def logoutUser(request):
   logout(request)
   return redirect('home')

def registerPage(request):
   form = UserCreationForm(request.POST)
   
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'An error occured during registration')



   return render(request, 'base/login_register.html', {'form': form})



#URLS trigger views, and that is what the user gets back.
def home(request):
   q = request.GET.get('q') if request.GET.get('q') != None else ''
   rooms = Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q) 
      )
   

   topics = Topic.objects.all()
   room_count = rooms.count()
   room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

   context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
              'room_messages' : room_messages}
   return render(request, 'base/home.html', context)

