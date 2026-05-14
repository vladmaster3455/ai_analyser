from django.urls import path

from .views import RecruiterDashboardView

urlpatterns = [path("dashboard/", RecruiterDashboardView.as_view(), name="dashboard")]
