from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	email=models.EmailField(primary_key=True)	
	profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
	# first_name=models.CharField(max_length=20,required=False)
	# last_name=models.CharField(max_length=20,required=False)
	USERNAME_FIELD='username'

	def __str__(self):
		return self.user.username

class RecruiterProfileInfo(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)

	Company_Name=models.CharField(max_length=50,blank=False)
	email=models.EmailField(primary_key=True)	
	profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

	def __str__(self):
		return self.user.username