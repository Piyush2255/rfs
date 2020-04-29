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
from candidate.models import UserProfileInfo,RecruiterProfileInfo,JobInfo,ApplicationInfo
from tika import parser
import os,yagmail
from django.contrib import messages
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
			messages.error(request,"Invalid Login Details")
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
	jobs=JobInfo.objects.filter(deadline__gte=today).order_by('-posting_date','deadline')[:5]
	applications=ApplicationInfo.objects.filter(candidate=request.user)[:5]
	args={'user':request.user,'jobs':jobs,'applications':applications}
	return render(request,'canddashboard.html',context=args)

@login_required
def recdashboard(request):
	jobs=JobInfo.objects.filter(recruiter=request.user).order_by('-posting_date','-deadline')[:5]
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
	args={'user':request.user}
	return render(request,'postjob.html',context=args)

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
		deaddate=deaddate.date()
		if(deaddate<today):
			errmess="Deadline can't be in the past!!!"
			args={'user':request.user,'message':errmess}
			return render(request,'postjob.html',context=args)
		postdate=today.strftime("%Y-%m-%d")
		recuser=request.user
		JobInfo.objects.create(job_name=jobname,job_description=jobdesc,skill=skills,experience=experiences,salary=expsalary,deadline=deaddate,posting_date=postdate,recruiter=recuser)
		mess="Job has been successfully posted"
		jobs=JobInfo.objects.filter(recruiter=request.user).order_by('-posting_date','-deadline')[:5]
		args={'user':request.user,'message':mess,'jobs':jobs}
	return render(request,'recdashboard.html',context=args)

@login_required
def viewjob(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		print(job_id)
		job=JobInfo.objects.filter(id=job_id)
		args={'user':request.user,'jobs':job}
		return render(request,'viewjob.html',context=args)

@login_required
def jobapply(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		job=JobInfo.objects.filter(id=job_id)
		applications=ApplicationInfo.objects.filter(job=job_id,candidate=request.user)
		args={'user':request.user,'jobs':job,'applications':applications}
		return render(request,'jobapply.html',context=args)

@login_required
def confirmapply(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		jobs=JobInfo.objects.filter(id=job_id)
		cand=request.user
		resum=request.POST.get('resume')
		print(request.FILES['resume'])
		if 'resume' in request.FILES:
			resum=request.FILES['resume']
		skills="abc"
		for job in jobs:
			skills=job.skill
		skills=list(skills.split(","))
		total_skills=len(skills)
		each_skill_score=60/total_skills
		total_score=0
		application='a'
		for job1 in jobs:
			application=ApplicationInfo.objects.create(candidate=cand,job=job1,resume=resum,score=total_score,status=False)

		base='C:\\Users\\HP\\Desktop\\Resume\\rfs'
		file_data = parser.from_file(base+application.resume.url)
		text=file_data['content']
		text=str(text)
		text=text.lower()
		for skill in skills:
			skill=skill.lower()
			skill=skill.strip()
			if skill in text:
				total_score=total_score+each_skill_score

		application.score=total_score
		application.save()
		mess='You have successfully applied for job!!!'
		today=date.today()
		today=today.strftime('%Y-%m-%d')
		jobs=JobInfo.objects.filter(deadline__gte=today).order_by('-posting_date','deadline')[:5]
		applications=ApplicationInfo.objects.filter(candidate=request.user)[:5]
		args={'user':cand,'message':mess,'jobs':jobs,'applications':applications}
		return render(request,'canddashboard.html',context=args)

@login_required
def viewapplications(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		jobs=JobInfo.objects.filter(id=job_id)
		applications=ApplicationInfo.objects.filter(job=job_id).order_by('-score')
		args={'user':request.user,'applications':applications,'jobs':jobs}
		return render(request,'viewapplications.html',context=args)

@login_required
def candapplication(request):
	if request.method=='POST':
		application_id=request.POST.get('application_id')
		application=ApplicationInfo.objects.filter(id=application_id)
		args={'user':request.user,'applications':application}
		return render(request,'candapplication.html',context=args)

@login_required
def applicationstatus(request):
	if request.method=='POST':
		application_id=request.POST.get('application_id')
		select=request.POST.get('select')
		interview=request.POST.get('intdetail')
		applications=ApplicationInfo.objects.filter(id=application_id)
		recruiter=request.user
		name=recruiter.first_name+" "+recruiter.last_name
		# yagmail.register(name,'rpg@recruit')
		for application in applications:
			if select=='True':
				application.status=True
				application.save()
			receiver=application.candidate.userprofileinfo.email
			subjects=recruiter.recruiterprofileinfo.Company_Name
			body="Hi! "+application.candidate.first_name+" "+application.candidate.last_name
			if select=='True':
				body=body+", we are glad to inform you that "+recruiter.recruiterprofileinfo.Company_Name
				body=body+" has shortlisted you for the post of "+application.job.job_name+" in their firm."
				if interview:
					body=body+"\nHere is a message from recruiter:\n"
					body=body+interview+"\n";
				body=body+"For further information contact: "+recruiter.recruiterprofileinfo.email
			else:
				body=body+", we would like to inform you that "+recruiter.recruiterprofileinfo.Company_Name
				body=body+" has rejected your application for the post of "+application.job.job_name+" in their firm."
				if interview:
					body=body+"\nHere is a message from recruiter:\n\n"
					body=body+interview+"\n";
				body=body+"For further information contact: "+recruiter.recruiterprofileinfo.email
			email=yagmail.SMTP("rpgrecruiter@gmail.com")
			email.send(
				to=receiver,
				subject=subjects,
				contents=body,
				)
		args={'user':recruiter,'applications':applications}
		return render(request,'candapplication.html',context=args)

@login_required
def alljobs(request):
	today=date.today()
	today=today.strftime('%Y-%m-%d')
	jobs=JobInfo.objects.filter(deadline__gte=today)
	args={'user':request.user,'jobs':jobs}
	return render(request,'alljobs.html',context=args)

@login_required
def allappjobs(request):
	applications=ApplicationInfo.objects.filter(candidate=request.user)
	args={'user':request.user,'applications':applications}
	return render(request,'allappjobs.html',context=args)

@login_required
def allpostjobs(request):
	jobs=JobInfo.objects.filter(recruiter=request.user).order_by('-posting_date')
	args={'user':request.user,'jobs':jobs}
	return render(request,'allpostjobs.html',context=args)

@login_required
def selectmultiple(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		jobs=JobInfo.objects.filter(id=job_id)
		args={'user':request.user,'jobs':jobs}
		return render(request,'selectmultiple.html',context=args)

@login_required
def selectmultipleusers(request):
	if request.method=='POST':
		job_id=request.POST.get('job_id')
		num=int(request.POST.get('candidates'))
		applications=ApplicationInfo.objects.filter(job=job_id).order_by('-score')[:num]
		interview=request.POST.get('intdetail')
		recruiter=request.user
		yagmail.register('rpgrecruiter@gmail.com','rpg@recruit')
		for application in applications:
			if application.status==False:
				application.status=True
				application.save()
				receiver=application.candidate.userprofileinfo.email
				subjects=recruiter.recruiterprofileinfo.Company_Name
				body="Hi! "+application.candidate.first_name+" "+application.candidate.last_name
				body=body+", we are glad to inform you that "+recruiter.recruiterprofileinfo.Company_Name
				body=body+" has shortlisted you for the post of "+application.job.job_name+" in their firm."
				if interview:
					body=body+"\nHere is a message from recruiter:\n"
					body=body+interview+"\n";
				body=body+"For further information contact: "+recruiter.recruiterprofileinfo.email
				email=yagmail.SMTP("rpgrecruiter@gmail.com")
				email.send(
					to=receiver,
					subject=subjects,
					contents=body,
					)
		applications=ApplicationInfo.objects.filter(job=job_id).order_by('-score')
		jobs=JobInfo.objects.filter(id=job_id)
		args={'user':recruiter,'applications':applications,'jobs':jobs}
		return render(request,'viewapplications.html',context=args)