from django.shortcuts import render
from candidate.forms import UserForm,UserProfileInfoForm,RecruiterProfileInfoForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date,datetime
from candidate.models import UserProfileInfo,RecruiterProfileInfo,JobInfo
# Create your views here.
def index(request):
	return render(request,'index.html')

def cand_register(request):

	registered=False
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		# if 'candregister' in request.POST:
		# 	profile_form=UserProfileInfoForm(data=request.POST)
		# elif 'recregister' in request.POST:
		profile_form=UserProfileInfoForm(data=request.POST)
		is_candidate=True

		if user_form.is_valid() and profile_form.is_valid():

			user=user_form.save(commit=False)
			password = user_form.cleaned_data['password']
			try:
				validate_password(password, user)
			except ValidationError as e:
				user_form.add_error('password', e)
				return render(request,'register.html',{'is_candidate':is_candidate,'registered':registered,'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
			user.set_password(user.password)
			user.save()
			# user.profile.email = profile_form.cleaned_data.get('email')
			# # user.profile. = profile_form.cleaned_data.get('location')
			# user.profile.save()
			profile=profile_form.save(commit=False)
			profile.user=user
			

			if 'profile_pic' in request.FILES:
				profile.profile_pic=request.FILES['profile_pic']

			profile.save()
			registered=True

		else:
			print(user_form.errors,profile_form.errors)

	else:
		user_form=UserForm()
		profile_form=UserProfileInfoForm()
		is_candidate=True

	return render(request,'register.html',{'is_candidate':is_candidate,'registered':registered,'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})

def rec_register(request):

	registered=False
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		# if 'candregister' in request.POST:
		# 	profile_form=UserProfileInfoForm(data=request.POST)
		# elif 'recregister' in request.POST:
		profile_form=RecruiterProfileInfoForm(data=request.POST)
		is_candidate=False

		if user_form.is_valid() and profile_form.is_valid():

			user=user_form.save(commit=False)
			password = user_form.cleaned_data['password']
			try:
				validate_password(password, user)
			except ValidationError as e:
				user_form.add_error('password', e)
				return render(request,'register.html',{'is_candidate':is_candidate,'registered':registered,'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
			user.set_password(user.password)
			user.save()
			# user.profile.email = profile_form.cleaned_data.get('email')
			# # user.profile. = profile_form.cleaned_data.get('location')
			# user.profile.save()
			profile=profile_form.save(commit=False)
			profile.user=user
			

			if 'profile_pic' in request.FILES:
				profile.profile_pic=request.FILES['profile_pic']

			profile.save()
			registered=True

		else:
			print(user_form.errors,profile_form.errors)

	else:
		user_form=UserForm()
		profile_form=RecruiterProfileInfoForm()
		is_candidate=False

	return render(request,'register.html',{'is_candidate':is_candidate,'registered':registered,'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})

def candlogin(request):
	return render(request,'candlogin.html')

def reclogin(request):
	return render(request,'reclogin.html')

def user_login(request):

	if request.method=='POST':
		username=request.POST.get('Username')
		password=request.POST.get('Password')
		is_candidate=request.POST.get('iscand')

		user=authenticate(username=username, password=password)
		global u
		u=username

		if user:
			

			if user.is_active:
				login(request,user)
				print(is_candidate)
				if is_candidate=='True':
					return HttpResponseRedirect('canddashboard')
				else:
					return HttpResponseRedirect('recdashboard')

		else:
			# messages.error(request,"Invalid Login Details")
			if is_candidate=='True':
				return render(request,'candlogin.html')
			else:
				return render(request,'reclogin.html')

	else:
		return render(request,'reclogin.html')

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def canddashboard(request):
	today=date.today()
	today=today.strftime('%Y-%m-%d')
	jobs=JobInfo.objects.filter(deadline__gte=today)
	args={'user':request.user,'jobs':jobs}
	return render(request,'canddashboard.html',context=args)

@login_required
def recdashboard(request):
	jobs=JobInfo.objects.filter(recruiter=request.user).order_by('-posting_date','-deadline')
	print(jobs)
	args={'user':request.user,'jobs':jobs}
	return render(request,'recdashboard.html',context=args)

@login_required
def candprofile(request):
	args={'user':request.user}
	return render(request,'candprofile.html',context=args)

@login_required
def recprofile(request):
	args={'user':request.user}
	return render(request,'recprofile.html',context=args)

@login_required
def postjob(request):
	return render(request,'postjob.html')

@login_required
def jobconfirm(request):
	if request.method=='POST':
		jobname=request.POST.get('job_name')
		jobdesc=request.POST.get('job_description')
		skills=request.POST.get('skill')
		experiences=request.POST.get('experience')
		expsalary=request.POST.get('salary')
		deaddate1=request.POST.get('deadline')
		deaddate=datetime.strptime(deaddate1,"%Y-%m-%d")
		today=date.today()
		postdate=today.strftime("%Y-%m-%d")
		recuser=request.user
		JobInfo.objects.create(job_name=jobname,job_description=jobdesc,skill=skills,experience=experiences,salary=expsalary,deadline=deaddate,posting_date=postdate,recruiter=recuser)
		args={'user':request.user,'job_name':jobname,'job_description':jobdesc,'skill':skills,'experience':experiences,'salary':expsalary,'deadline':deaddate,'posting_date':postdate}
	return render(request,'jobconfirm.html',context=args)