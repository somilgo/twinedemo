from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

#Model for Jobs
class Job(models.Model):
	title = models.CharField(verbose_name="Job Title", max_length=200, blank=False)
	description = models.TextField(default='')

	def can_view_job(self, user):
		return user.user_type=='A' or self.systemuser_set.filter(pk=user.pk).exists()
		
	def __unicode__(self):
		return self.title

#Model for System User -- inherits AbtractBaseUser
#Admin and Recruiter objects are differentiated by the user_type field (for extensibility)
#Email doubles as username and is used for authentication
class SystemUser(AbstractBaseUser):
	first_name = models.CharField(verbose_name="First Name", max_length=30, default="")
	last_name = models.CharField(verbose_name="Last Name", max_length=30, default="")
	email = models.EmailField(
		verbose_name='Email Address',
		max_length=255,
		unique=True,
		default=''
	)
	USERNAME_FIELD = 'email'
	jobs = models.ManyToManyField(Job, blank=True)
	type_choices = (
		('A', 'Admin'),
		('R', 'Recruiter'),
	)
	user_type = models.CharField(max_length=1, choices=type_choices, default='R')
	objects=UserManager()

	def __unicode__(self):
		return self.first_name + " " + self.last_name