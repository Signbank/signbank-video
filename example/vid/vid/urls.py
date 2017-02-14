
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import Home

urlpatterns = [
    url(r'^$', Home.as_view()),

    url(r'^admin/', admin.site.urls),
    url(r'^v/', include('video.urls', namespace='video')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
