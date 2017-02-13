
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from video.models import TaggedVideo

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^admin/', admin.site.urls),
    url(r'^v/', include('video.urls', namespace='video')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
