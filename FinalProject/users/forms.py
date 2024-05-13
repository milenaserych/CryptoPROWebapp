from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

class ProfilePictureForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class UpdateProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'profile_image']
