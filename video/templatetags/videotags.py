from django.template import Library
from django.urls import reverse

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
def videoplayer(elementid, posterurl, videourl):
    """
    Generate an HTML video player for this video
    """

    return {
        'elementid': elementid,
        'posterurl': posterurl,
        'videourl': videourl,
    }
