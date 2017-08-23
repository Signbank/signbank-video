from django.conf.urls import url

from video import views


app_name = "video"
urlpatterns = [
    url(r'^video/$', views.upload, name='upload'),
    # ex: video/1/
    url(r'^video/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)$', views.video, name='video'),
    # ex: delete/1/
    url(r'^delete/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/$', views.deletevideo, name='delete'),
    # ex: poster/1/
    url(r'^poster/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/$', views.poster, name='poster'),
]
