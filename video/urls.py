from django.conf.urls import url

from video import views


app_name = "video"
urlpatterns = [
    # ex: video/1/
    url(r'^video/(?P<videoid>\d+)/$', views.video, 
        name='video'),
    # ex: upload/ 
    url(r'^upload/$', views.addvideo, 
        name="add_video"),
    # ex: delete/1/    
    url(r'^delete/(?P<videoid>\d+)/$', views.deletevideo,
        name='delete'),
    # ex: poster/1/    
    url(r'^poster/(?P<videoid>\d+)/$', views.poster, 
        name='poster'),
    # This url isn't accessed directly
    # by a user. Instead, he gets
    # redirected here.
    # The case of a user direclty
    # entering this url is handled in the view.
    url(r'^success/$', views.successpage,
        name='successpage'),
    # ex: iframe/1/
    #url(r'^iframe/(?P<videoid>\d+)/$', views.iframe,
    #    name='iframe'),
]
