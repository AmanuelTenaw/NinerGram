from django.forms import ModelForm
from .models import Room 
from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture', 'pronouns', 'bio']
        