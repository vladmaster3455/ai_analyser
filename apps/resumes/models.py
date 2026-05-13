from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class Candidate(TimeStampedModel):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidates")
    full_name = models.CharField(max_length=180)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    source = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.full_name


class Resume(TimeStampedModel):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        ANALYZED = "analyzed", "Analyzed"
        FAILED = "failed", "Failed"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/%Y/%m/")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    raw_text = models.TextField(blank=True)
    error_message = models.TextField(blank=True)


class JobProfile(TimeStampedModel):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_profiles")
    title = models.CharField(max_length=180)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    seniority_weight = models.FloatField(default=0.25)
    skills_weight = models.FloatField(default=0.55)
    education_weight = models.FloatField(default=0.20)


class ResumeAnalysis(TimeStampedModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="analyses")
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE, related_name="analyses")
    score = models.FloatField(default=0)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    seniority_years = models.FloatField(default=0)
    summary = models.TextField(blank=True)
