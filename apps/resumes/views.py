from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Candidate, JobProfile, Resume
from .serializers import AnalyzeResumeSerializer, CandidateSerializer, JobProfileSerializer, ResumeSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    search_fields = ("full_name", "email", "phone")

    def get_queryset(self):
        return Candidate.objects.filter(recruiter=self.request.user)


class JobProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobProfileSerializer

    def get_queryset(self):
        return JobProfile.objects.filter(recruiter=self.request.user)


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    filterset_fields = ("status", "candidate")
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return Resume.objects.select_related("candidate").prefetch_related("analyses").filter(candidate__recruiter=self.request.user)

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        resume = self.get_object()
        serializer = AnalyzeResumeSerializer(data=request.data, context={"request": request, "resume": resume})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "queued"}, status=status.HTTP_202_ACCEPTED)
