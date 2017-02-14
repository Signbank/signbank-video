from django.conf.urls import url

from video import views


app_name = "video"
urlpatterns = [
    url(r'^video/$', views.upload, name='upload'),
    # ex: video/1/
    url(r'^video/(?P<category>[^/]+)/(?P<tag>[^/]+)$', views.video, name='video'),
    # ex: delete/1/
    url(r'^delete/(?P<category>[^/]+)/(?P<tag>[^/]+)/$', views.deletevideo, name='delete'),
    # ex: poster/1/
    url(r'^poster/(?P<category>[^/]+)/(?P<tag>[^/]+)/$', views.poster, name='poster'),
]
