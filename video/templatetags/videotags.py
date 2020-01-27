from django.template import Library, Node, TemplateSyntaxError
from django.urls import reverse
from django.shortcuts import get_object_or_404
import natsort

from video.models import TaggedVideo
from video.forms import VideoUploadForm, VideoUploadTagForm

register = Library()

@register.inclusion_tag("video/javascript.html")
def load_video_javascript():
    """Include the required JS for video playback"""

    return {}


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
def thumbnail_popup(id, category, tag, width=300, height=200, preload='auto'):
    """
    Generate a thumbnail image that triggers a modal video player
    """

    try:
        video = TaggedVideo.objects.get(category=category, tag=tag)
    except:
        video = None

    return {
        'id': id,
        'tag': tag,
        'video': video,
        'width': width,
        'height': height,
        'preload': preload,
    }


@register.tag("category_videos")
def do_get_tagged_videos(parser, token):
    """Template tag to get a list of videos with a given tag
    {% category_videos grammar_videos Grammar %}
    {% for video in grammar_videos %}
    ...
    {% endfor %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        template_tag, variable_name, category = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            "%r tag requires exactly three arguments" % token.contents.split()[0]
        )
    return TaggedVideoNode(variable_name, category)


class TaggedVideoNode(Node):
    def __init__(self, variable_name, category):
        self.variable_name = variable_name
        self.category = category
        
    def render(self, context):

        # return videos in natural sorted order by tag, eg. 5.1, 5.7, 5.7a, 5.10 etc
        context[self.variable_name] = natsort.natsorted(TaggedVideo.objects.filter(category=self.category),
                                                        key=lambda x: x.tag)
        return ''