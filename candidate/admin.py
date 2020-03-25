from django.contrib import admin
from candidate.models import UserProfileInfo,RecruiterProfileInfo,JobInfo
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(RecruiterProfileInfo)
admin.site.register(JobInfo)