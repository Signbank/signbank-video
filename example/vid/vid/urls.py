
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import Home

urlpatterns = [
    path('', Home.as_view()),

    path('admin/', admin.site.urls),
    path('v/', include('video.urls', namespace='video')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
