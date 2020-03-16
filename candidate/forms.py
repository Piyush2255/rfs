from django import forms
from django.contrib.auth.models import User
from candidate.models import UserProfileInfo
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):

	password=forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model=User
		fields=('username','first_name','last_name','password')

class UserProfileInfoForm(forms.ModelForm):

	# password=forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model=UserProfileInfo
		fields=('email','profile_pic')