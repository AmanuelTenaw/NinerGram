from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Topic, Message, Post, Follow
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PostForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})




@login_required(login_url='login')
def main_view(request):
    followed_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(
    Q(user__in=followed_ids) | Q(user=request.user)
).order_by('-created')
    
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'main.html', {
        'posts': posts,
        'users': users,
        'followed_ids': list(followed_ids), 
    })




@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('home')  # or 'profile', etc.

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('home')





@login_required
def follow_search(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

    followed_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    context = {
        'users': users,
        'query': query,
        'followed_ids': list(followed_ids),
    }
    return render(request, 'follow_search.html', context)




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

