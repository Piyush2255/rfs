from django.shortcuts import render
from candidate.forms import UserForm,UserProfileInfoForm,RecruiterProfileInfoForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
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

def canddashboard(request):
	args={'user':request.user}
	return render(request,'canddashboard.html',context=args)

def recdashboard(request):
	args={'user':request.user}
	return render(request,'recdashboard.html',context=args)

def candprofile(request):
	args={'user':request.user}
	return render(request,'candprofile.html',context=args)

def recprofile(request):
	args={'user':request.user}
	return render(request,'recprofile.html',context=args)