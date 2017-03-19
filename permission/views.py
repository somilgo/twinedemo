from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LogIn, RecruiterForm
from django.contrib.auth import authenticate
from .models import *

def index(request):
	if 'user' not in request.session:
		return log_in(request)
	else:
		return HttpResponseRedirect("/permission/main")

def log_in(request):
	form = LogIn(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			request.session['user'] = email
			return index(request)
		else:
			messages.warning(request, "Username or password is incorrect.")
	return render(request, 'permission/log_in.html', {'form':form})

def main(request):
	if 'user' not in request.session:
		return HttpResponseRedirect("/permission/index")
	user = SystemUser.objects.filter(email=request.session['user'])[0]
	context = {}
	context['admin'] = user.user_type=="A"
	if context['admin']:
		context['jobs'] = Job.objects.all()
		context['recruiters'] = SystemUser.objects.filter(user_type="R")
	else:
		context['jobs'] = user.jobs.all()
	context['user'] = user
	return render(request, 'permission/main.html', context)

def job(request, pk):
	if 'user' not in request.session:
		return HttpResponseRedirect("/permission/index")
	context = {}
	user = SystemUser.objects.filter(email=request.session['user'])[0]
	job = Job.objects.get(pk=pk)
	if not job.can_view_job(user):
		return HttpResponse("You do not have permission to view this job.")
	context['users'] = job.systemuser_set.all()
	context['job'] = job
	context['admin'] = user.user_type=="A"
	return render(request, 'permission/job.html', context)

def recruiter(request, pk):
	if 'user' not in request.session:
		return HttpResponseRedirect("/permission/index")
	context = {}
	user = SystemUser.objects.filter(email=request.session['user'])[0]
	rec = SystemUser.objects.get(pk=pk)
	if not user.user_type=="A":
		return HttpResponse("You do not have permission to view this page.")
	context['rec'] = rec

	if request.method == 'POST':
		form = RecruiterForm(request.POST, instance=rec)
		if form.is_valid():
			form.save()
	else:
		form = RecruiterForm(instance=rec)
	context['form'] = form
	return render(request, 'permission/recruiter.html', context)