from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('video/', include("video_app.urls"), name="video"),
                  path('', include("video_app.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)