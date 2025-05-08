from django.forms import ModelForm
from .models import Room, Event, Post, Profile, Message
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['display_name', 'avatar', 'pronouns', 'bio', 'major', 'year']






class CustomUserCreationForm(UserCreationForm):
    school_id = forms.CharField(max_length=20, required=True, label="School ID")

    class Meta:
        model = User
        fields = ['username', 'email', 'school_id', 'password1', 'password2']

    def clean_school_id(self):
        school_id = self.cleaned_data.get('school_id', '').strip()
        try:
            with open('Niner_id.txt', 'r') as f:
                valid_ids = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            raise forms.ValidationError("Validation file not found.")

        if school_id not in valid_ids:
            raise forms.ValidationError("School ID not recognized.")
        return school_id
      

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'location', 'date', 'image']





from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']

