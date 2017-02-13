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
            category = form.cleaned_data['category']
            vfile = form.cleaned_data['videofile']
            # Let's name the video
            # ex: 3.mp4
            vfile.name = "%s.mp4" % (tag,)

            tagvid = TaggedVideo.objects.add(category, tag, vfile)

            messages.success(request,
                "Your video has been successfully uploaded")
            return HttpResponseRedirect(form.cleaned_data['redirect'])
        else:
            if 'HTTP_REFERER' in request.META:
                url = request.META['HTTP_REFERER']
            else:
                url = '/'
            return redirect(url)


def video(request, category, tag):
    '''
    Redirect to the video url for this category + tag
    '''
    taggedvideo = get_object_or_404(TaggedVideo, category=category, tag=tag)
    return redirect(taggedvideo.get_absolute_url())

@login_required
def deletevideo(request, category, tag):
    '''
    Remove the video for this gloss, if there is an older version
    then reinstate that as the current video (act like undo)
    '''
    if request.method == "POST":
        video = get_object_or_404(TaggedVideo, category=category, tag=tag)
        result = video.revert()
        # result is True if there is an older version we've reverted to
        if result:
            msgtext = "Video reverted to previous version, %s versions remaining" % video.versions()
        else:
            # here we just delete the tagged video object
            video.delete()
            msgtext = "Video deleted, no versions remaining"

        messages.success(request, msgtext)

    # TODO: provide some feedback that it worked (if
    # immediate non-display of video isn't working)
    # return to referer
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)


def poster(request, category, tag):
    """Generate a still frame for a video (if needed) and
    generate a redirect to the static server for this frame"""
    # We want the latest video associated with this tag(it has version 0)
    video = get_object_or_404(TaggedVideo, category=category, tag=tag)
    return redirect(video.poster_url())

def iframe(request, category, tag):
    """Generate an iframe with a player for this video"""

    try:
        TaggedVideo = TaggedVideo.objects.get(category=category, tag=tag, version=0)
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
