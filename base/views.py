from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Topic, Message, Post, Follow, Event
from .forms import RoomForm, EventForm, PostForm, UserForm, ProfileForm, MessageForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile, Message, Thread
from django.db import models


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
    posts = Post.objects.filter(Q(user__in=followed_ids) | Q(user=request.user)).order_by('-created')
    events = Event.objects.filter(Q(user__in=followed_ids) | Q(user=request.user)).order_by('-created')
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'main.html', {
        'posts': posts,
        'events': events,
        'users': users,
        'followed_ids': list(followed_ids), 
    })





@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        Follow.objects.get_or_create(follower=request.user, following=target_user)
    return redirect('user-profile', username=target_user.username)




@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        Follow.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('user-profile', username=target_user.username)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        post.delete()
        return redirect('user-profile', username=request.user.username)


    return render(request, 'base/delete_post.html', {'post': post})







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

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)


    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect('edit_profile')

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'base/edit_profile.html', context)




def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

"""
@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by('-created')
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)

    context = {
        'profile': profile,
        'posts': posts,
        'followers_count': followers.count(),
        'following_count': following.count(),
    }
    return render(request, 'base/profile.html', context)
"""

def event_list(request):
    events = Event.objects.all().order_by('-created')
    return render(request, 'base/event_list.html', {'events': events})

@login_required
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event-list')
    return render(request, 'base/create_event.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Message, Follow
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def thread_list_view(request):
    threads = Thread.objects.filter(participants=request.user)
    return render(request, 'base/thread_list.html', {'threads': threads})

@login_required
def thread_detail_view(request, username):
    other_user = get_object_or_404(User, username=username)
    thread = Thread.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not thread:
        thread = Thread.objects.create()
        thread.participants.set([request.user, other_user])

    messages = thread.messages.all()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.thread = thread
            message.save()
            return redirect('thread-detail', username=other_user.username)
    else:
        form = MessageForm()

    return render(request, 'base/thread_detail.html', {
        'form': form,
        'messages': messages,
        'other_user': other_user
    })

@login_required
def start_conversation_view(request):
    followed_users = User.objects.filter(followers__follower=request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        return redirect('thread-detail', username=username)

    return render(request, 'base/start_conversation.html', {
        'followed_users': followed_users
    })

@login_required
def search_users_view(request):
    query = request.GET.get('q')
    current_user_profile = get_object_or_404(Profile, user=request.user)
    suggestions = Profile.objects.none()

    if current_user_profile.major and current_user_profile.year:
        suggestions = Profile.objects.filter(
            Q(major=current_user_profile.major) | Q(year=current_user_profile.year)
        ).exclude(user=request.user).exclude(id__in=current_user_profile.follows.values_list('id', flat=True))

    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else User.objects.none()
    return render(request, 'base/search.html', {'users': users, 'suggestions': suggestions})






@login_required
def friend_suggestions(request):
    user_profile = request.user.profile
    following_ids = Follow.objects.filter(follower=request.user).values_list('following__id', flat=True)

    suggestions = Profile.objects.exclude(user=request.user).exclude(user__id__in=following_ids).filter(
        models.Q(major=user_profile.major) | models.Q(year=user_profile.year)
    )

    return render(request, 'base/friend_suggestions.html', {'suggestions': suggestions})



def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    posts = user.post_set.all()

    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    context = {
        'user': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': posts,
        'is_following': is_following,  
    }
    return render(request, 'base/profile.html', context)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Follow

def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).select_related('following')
    return render(request, 'base/following_list.html', {
        'following': following,
        'profile_user': user
    })

def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).select_related('follower')
    return render(request, 'base/followers_list.html', {
        'followers': followers,
        'profile_user': user
    })
