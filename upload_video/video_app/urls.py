from django.urls import path
from .views import *
from . import views


app_name = "video_app"
urlpatterns = [
    path("upload/", views.uploading),
    path("", views.index),
    path("video_frame/", views.video_frame),
]