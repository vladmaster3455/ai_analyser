from django.contrib import admin

from .models import Candidate, JobProfile, Resume, ResumeAnalysis

admin.site.register(Candidate)
admin.site.register(JobProfile)
admin.site.register(Resume)
admin.site.register(ResumeAnalysis)
