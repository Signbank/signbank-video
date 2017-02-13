from django.template import Library
from django.urls import reverse
from django.shortcuts import get_object_or_404

from video.models import TaggedVideo
from video.forms import VideoUploadForm, VideoUploadTagForm

register = Library()

@register.inclusion_tag("video/uploadform.html")
def uploadform(identifier=None, redirect='/'):
    """
    Generate a form to upload a new video.
    """

    if identifier is None:
        form = VideoUploadTagForm(initial={'tag': identifier, 'redirect': redirect})
    else:
        form = VideoUploadForm(initial={'redirect': redirect})

    return {
     'form': form,
    }

@register.inclusion_tag("video/player.html")
def videoplayer(elementid, category, tag):
    """
    Generate an HTML video player for a video given the category and tag
    """

    video = get_object_or_404(TaggedVideo, category=category, tag=tag)

    return {
        'elementid': elementid,
        'video': video
    }
