from django.urls import path

from video import views


app_name = "video"
urlpatterns = [
    path('video/', views.upload, name='upload'),
    # ex: video/1/
    path('video/<category>/<tag>', views.video, name='video'),
    # ex: delete/1/
    path('delete/<category>/<tag>', views.deletevideo, name='delete'),
    # ex: poster/1/
    path('poster/<category>/<tag>/', views.poster, name='poster'),
]
