from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

#Model for Jobs
class Job(models.Model):
	title = models.CharField(verbose_name="Job Title", max_length=200, blank=False)
	description = models.TextField(default='')

	#Sees if a particular user is an admin or is approved to view the job
	def can_view_job(self, user):
		return user.user_type=='A' or user.get_profile().jobs.filter(pk=self.pk).exists()

	#Gets list of recruiters who are able to see a particular job
	def get_recruiter_set(self):
		r = Recruiter.objects.filter(jobs__in=[self]).values_list('user', flat=True)
		l = []
		for i in r:
			l.append(SystemUser.objects.get(pk=i))
		return l

	def __unicode__(self):
		return self.title

#Model for System User -- inherits AbtractBaseUser
#Admin and Recruiter objects are differentiated by the user_type field (for code reuse)
#Email doubles as username and is used for authentication
class SystemUser(AbstractBaseUser):
	#General fields for all users
	first_name = models.CharField(verbose_name="First Name", max_length=30, default="")
	last_name = models.CharField(verbose_name="Last Name", max_length=30, default="")
	email = models.EmailField(
		verbose_name='Email Address',
		max_length=255,
		unique=True,
		default=''
	)
	#User type differentiates between admin and recruiter
	type_choices = (
		('A', 'Admin'),
		('R', 'Recruiter'),
	)
	user_type = models.CharField(max_length=1, choices=type_choices, default='R')

	#User object management fields
	objects=UserManager()
	REQUIRED_FIELDS = ['user_type', 'first_name', 'last_name']
	USERNAME_FIELD = 'email'

	#Gets user profile associated with specific user type
	#separate profiles for extensibility and code reuse
	def get_profile(self):
		if self.user_type == "A":
			return Admin.objects.get(user=self)
		else:
			return Recruiter.objects.get(user=self)

	def __unicode__(self):
		return self.first_name + " " + self.last_name

#Recruiter profile, contains all recruiter specific fields and links to SystemUser objects
class Recruiter (models.Model):
	user = models.OneToOneField(SystemUser, on_delete=models.CASCADE, primary_key=True)
	#Fields specific to Recruiter
	jobs = models.ManyToManyField(Job, blank=True)

#Admin profile, contains all recruiter specific fields and links to SystemUser objects
class Admin (models.Model):
	user = models.OneToOneField(SystemUser, on_delete=models.CASCADE, primary_key=True)
	#Fields specific to Admin