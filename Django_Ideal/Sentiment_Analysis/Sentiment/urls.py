"""This File will handle all the routes"""
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Sentiment"
urlpatterns = [
        path("analysis/", AnalysisPage.as_view(), name="index"),
        path("login/", LogIn.as_view(), name="login"),
        path("logout/", LogOut.as_view(), name="logout"),
        path("download/", download, name="download"),
        path("analysis/analyze/", analysis, name="analyze"),
        path("logout/", LogOut, name="logout"),
        path("", HomePage.as_view(), name="dashboard"),
        path("analysis_api/", CSV_API.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
