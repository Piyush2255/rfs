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

class JobInfo(models.Model):

	recruiter=models.ForeignKey(User,on_delete=models.CASCADE)
	job_name=models.CharField(max_length=50,blank=False)
	job_description=models.TextField(blank=False)
	experience=models.CharField(blank=False,max_length=15)
	deadline=models.DateField(blank=False)
	skill=models.CharField(max_length=30,blank=False)
	salary=models.IntegerField(blank=False)
	posting_date=models.DateField(blank=False)

	def __str__(self):
		return self.job_name

class ApplicationInfo(models.Model):

	candidate=models.ForeignKey(User,on_delete=models.CASCADE)
	job=models.ForeignKey(JobInfo,on_delete=models.CASCADE)
	resume=models.FileField(upload_to='resumes',blank=False)
	score=models.IntegerField(blank=False)
	status=models.BooleanField(blank=False,default=False)
	# interview_info=models.CharField(max_length=150,blank=True,default='None')

	def __str__(self):
		return self.candidate.username

	class Meta:
		unique_together=('candidate','job',)
