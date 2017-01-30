from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.conf import settings
from django.views.generic import ListView, DetailView

from video.models import TaggedVideo
from video.forms import VideoUploadForm


class VideoList(ListView):
    """A list of videos, also supports upload of new videos"""

    model = TaggedVideo
    template_name = "video/video_list.html"

    def post(self, request, *args, **kwargs):
        """Upload a new video"""

        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            vfile = form.cleaned_data['videofile']
            # Let's name the video
            # ex: 3.mp4
            vfile.name = "%s.mp4" % (tag,)

            tagvid = TaggedVideo.objects.addvideo(tag, vfile)

            messages.success(request,
                "Your video has been successfully uploaded")
            return HttpResponseRedirect(form.cleaned_data['redirect'])
        else:
            if 'HTTP_REFERER' in request.META:
                url = request.META['HTTP_REFERER']
            else:
                url = '/'
            return redirect(url)


def video(request, videoid):
    '''
    Redirect to the video url for this videoid
    '''
    # We want the latest video associated with this tag (it has version 0)
    video = get_object_or_404(TaggedVideo, tag=videoid, version=0)
    return redirect(video)

@login_required
def deletevideo(request, videoid):
    '''
    Remove the video for this gloss, if there is an older version
    then reinstate that as the current video (act like undo)
    '''
    if request.method == "POST":
        # deal with any existing video for this sign
        videos = TaggedVideo.objects.filter(tag=videoid).order_by('version')
        for video in videos:
            # this will remove the most recent video, ie it's equivalent
            # to delete if version=0
            video.reversion(revert=True)
    # TODO: provide some feedback that it worked (if
    # immediate non-display of video isn't working)
    # return to referer
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)


def poster(request, videoid):
    """Generate a still frame for a video (if needed) and
    generate a redirect to the static server for this frame"""
    # We want the latest video associated with this tag(it has version 0)
    video = get_object_or_404(TaggedVideo, tag=videoid, version=0)
    return redirect(video.poster_url())

def iframe(request, videoid):
    """Generate an iframe with a player for this video"""

    try:
        TaggedVideo = TaggedVideo.objects.get(tag=videoid, version=0)
        videourl = TaggedVideo.get_absolute_url()
        posterurl = TaggedVideo.poster_url()
    except:
        gloss = None
        TaggedVideo = None
        videourl = None
        posterurl = None
    return render(request, "video/iframe.html",
                  {'videourl': videourl,
                   'posterurl': posterurl,
                   'aspectRatio': settings.VIDEO_ASPECT_RATIO,
                   })
