from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LogIn, RecruiterForm
from django.contrib.auth import authenticate
from .models import *

#Home page redirects to log in page if not logged in
def index(request):
	if 'user' not in request.session:
		return log_in(request)
	else:
		return HttpResponseRedirect("/permission/main")

#Log in page for both recruiters and admins
def log_in(request):
	form = LogIn(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = SystemUser.objects.get(email=email)
		if user is not None:
			request.session['user'] = email
			return index(request)
		else:
			pass
	return render(request, 'permission/log_in.html', {'form':form})

def logout(request):
	request.session.pop('user', None)
	return HttpResponseRedirect("/permission/main")

'''
Main dashboard -- shows jobs (that the current user has access to) and
a list of the recruiters (if admin)
'''
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

#Page that shows the title and description for a job. If admin, shows recruiters.
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

#Page for admins that shows the jobs that a recruiter has access to and allows admin to edit
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