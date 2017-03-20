from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
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
		context['jobs'] = user.get_profile().jobs.all()
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
	context['users'] = job.get_recruiter_set()
	print context['users']
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
		form = RecruiterForm(request.POST, instance=rec.get_profile())
		if form.is_valid():
			form.save()
	else:
		form = RecruiterForm(instance=rec.get_profile())
	context['form'] = form
	return render(request, 'permission/recruiter.html', context)

#Sign up form -- generic
def sign_up(request):
	request.session.pop('user', None)
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			u = form.save()
			#Creates and associates user profile
			if u.user_type=='A':
				n = Admin(user=u)
			else:
				n = Recruiter(user=u)
			n.save()
			u.save()
			return HttpResponseRedirect('/permission/index')
	else:
		form = RegistrationForm()

	return render(request, 'permission/sign_up.html', {'form': form})

#Job creation form -- generic
def create_job(request):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/permission/main')
	else:
		form = JobForm()

	return render(request, 'permission/create_job.html', {'form': form})
