from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Job)
admin.site.register(Admin)
admin.site.register(Recruiter)
admin.site.register(SystemUser)