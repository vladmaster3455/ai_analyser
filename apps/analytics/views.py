from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.resumes.models import ResumeAnalysis


class RecruiterDashboardView(APIView):
    def get(self, request):
        analyses = ResumeAnalysis.objects.filter(resume__candidate__recruiter=request.user)
        data = analyses.aggregate(total=Count("id"), average_score=Avg("score"))
        top_candidates = analyses.select_related("resume__candidate").order_by("-score")[:5]
        data["top_candidates"] = [{"candidate": item.resume.candidate.full_name, "score": item.score} for item in top_candidates]
        return Response(data)
