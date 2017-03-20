from django import forms
from permission.models import *
from django.contrib.auth.hashers import check_password

#Form for authenticating users and logging them in
class LogIn(forms.Form):
	email = forms.EmailField(label = "Email")
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	def clean(self):
		password = self.cleaned_data.get("password")
		email = self.cleaned_data.get("email")
		user = SystemUser.objects.filter(email=email)
		if (not (user.exists())):
			raise forms.ValidationError("This email has not been registered")
		else:
			if check_password(password, user[0].password):
				pass
			else:
				raise forms.ValidationError("Email and password combination do not match.")
		return self.cleaned_data

#Form for admins to update which jobs a recruiter has access to
class RecruiterForm(forms.ModelForm):
	jobs = forms.ModelMultipleChoiceField(queryset=Job.objects.all(),widget=forms.SelectMultiple,required=False)
	class Meta:
		model = Recruiter
		fields = ('jobs',)
	def clean(self):
		jobs = self.cleaned_data['jobs']
	def save(self, commit=True):
		user = super(RecruiterForm, self).save(commit=False)
		if commit:
			user.save()
		user.jobs = self.cleaned_data['jobs']
		user.save()
		return user

#Form for creating new users
class RegistrationForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput,
								label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput,
								label="Password (again)")
	class Meta:
		model = SystemUser
		fields = ('first_name', 'last_name', 'email', 'password1',  'password2', 'user_type')
	def clean(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		email = self.cleaned_data.get("email")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		if SystemUser.objects.filter(email=email).exists():
			raise forms.ValidationError("This email has already been registered")
		return self.cleaned_data
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.save()
		return user

#Form for creating new jobs
class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		exclude = []
	def clean(self):
		return self.cleaned_data
	def save(self, commit=True):
		j  = super(JobForm, self).save(commit=False)
		j.save()
		return j