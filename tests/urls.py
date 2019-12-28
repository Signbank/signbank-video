from django.urls import include, path


urlpatterns = [
    path('', include("video.urls", namespace="video")),
]
