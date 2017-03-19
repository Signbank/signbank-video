from django.template import Library
from django.urls import reverse
from django.shortcuts import get_object_or_404

from video.models import TaggedVideo
from video.forms import VideoUploadForm, VideoUploadTagForm

register = Library()

@register.inclusion_tag("video/uploadform.html")
def uploadform(category=None, tag=None, redirect='/'):
    """
    Generate a form to upload a new video.
    """

    if tag is not None and category is not None:
        form = VideoUploadForm(initial={'category': category, 'tag': tag, 'redirect': redirect})
    else:
        form = VideoUploadTagForm(initial={'redirect': redirect})

    return {
     'form': form,
    }

@register.inclusion_tag("video/upload_modal.html")
def upload_modal(id, category=None, tag=None, redirect='/'):
    """
    Generate a modal containing a video upload form supporting drag and drop.
    """
    if tag is not None and category is not None:
        form = VideoUploadForm(initial={'category': category, 'tag': tag, 'redirect': redirect})
    else:
        form = VideoUploadTagForm(initial={'redirect': redirect})

    return {
     'id': id,
     'form': form,
    }


@register.inclusion_tag("video/player.html")
def videoplayer(id, category, tag, width=300, height=200):
    """
    Generate an HTML video player for a video given the category and tag
    """

    try:
        video = TaggedVideo.objects.get(category=category, tag=tag)
    except:
        video = None

    return {
        'id': id,
        'video': video,
        'width': width,
        'height': height,
    }


@register.inclusion_tag("video/thumbnail-popup.html")
def thumbnail_popup(id, category, tag, width=300, height=200):
    """
    Generate a thumbnail image that triggers a modal video player
    """

    try:
        video = TaggedVideo.objects.get(category=category, tag=tag)
    except:
        video = None

    return {
        'id': id,
        'video': video,
        'width': width,
        'height': height,
    }
