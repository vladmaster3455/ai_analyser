from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CandidateViewSet, JobProfileViewSet, ResumeViewSet

router = DefaultRouter()
router.register("candidates", CandidateViewSet, basename="candidate")
router.register("jobs", JobProfileViewSet, basename="job-profile")
router.register("resumes", ResumeViewSet, basename="resume")

urlpatterns = [path("", include(router.urls))]
