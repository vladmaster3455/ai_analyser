from rest_framework import serializers

from .models import Candidate, JobProfile, Resume, ResumeAnalysis
from .tasks import analyze_resume_task


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ("id", "full_name", "email", "phone", "source", "created_at")

    def create(self, validated_data):
        validated_data["recruiter"] = self.context["request"].user
        return super().create(validated_data)


class JobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfile
        fields = ("id", "title", "description", "required_skills", "seniority_weight", "skills_weight", "education_weight")

    def create(self, validated_data):
        validated_data["recruiter"] = self.context["request"].user
        return super().create(validated_data)


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ("id", "job_profile", "score", "matched_skills", "missing_skills", "seniority_years", "summary", "created_at")


class ResumeSerializer(serializers.ModelSerializer):
    analyses = ResumeAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ("id", "candidate", "file", "status", "raw_text", "error_message", "analyses", "created_at")
        read_only_fields = ("status", "raw_text", "error_message")


class AnalyzeResumeSerializer(serializers.Serializer):
    job_profile_id = serializers.PrimaryKeyRelatedField(queryset=JobProfile.objects.all(), source="job_profile")

    def validate_job_profile_id(self, value):
        if value.recruiter != self.context["request"].user:
            raise serializers.ValidationError("Profil de poste non autorise.")
        return value

    def save(self, **kwargs):
        resume = self.context["resume"]
        job_profile = self.validated_data["job_profile"]
        analyze_resume_task.delay(resume.id, job_profile.id)
        return resume
