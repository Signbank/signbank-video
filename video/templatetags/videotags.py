from django.template import Library, Node, Variable
from django.template.exceptions import TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType

from video.models import TaggedVideo
from video.forms import VideoUploadForm, VideoUploadMultipleForm
from video.forms import VideoUploadPickContentTypeForm, VideoUploadMultiplePickContentTypeForm

register = Library()


@register.inclusion_tag("video/uploadform.html")
def uploadform(obj=None, multiple=False, redirect='/'):
    """
    Generate a form to upload a new video for object.
    If multiple is True, then present a form capable of sending multiple files.
    """
    if multiple:
        form_to_use = VideoUploadMultipleForm
    else:
        form_to_use = VideoUploadForm

    if obj is not None:
        content_type = ContentType.objects.get_for_model(obj)
        form = form_to_use(initial={'content_type': content_type.id, 'object_id': obj.id, 'redirect': redirect})
    else:
        form = form_to_use(initial={'redirect': redirect})

    return {
     'form': form,
    }


@register.inclusion_tag("video/upload_modal.html")
def upload_modal(id, obj=None, multiple=False, redirect='/'):
    """
    Generate a modal containing a video upload form supporting drag and drop.
    """
    if multiple:
        form_to_use = VideoUploadMultipleForm
        form_to_use_ct = VideoUploadMultiplePickContentTypeForm
    else:
        form_to_use = VideoUploadForm
        form_to_use_ct = VideoUploadPickContentTypeForm

    if obj is not None:
        # When object is delivered we can get its ContentType
        content_type = ContentType.objects.get_for_model(obj)
        form = form_to_use(initial={'content_type': content_type.id, 'object_id': obj.id, 'redirect': redirect})
    else:
        # When no object delivered, we must choose ContentType
        form = form_to_use_ct(initial={'redirect': redirect})

    return {
     'id': id,
     'form': form,
    }


@register.inclusion_tag("video/player.html")
def videoplayer(id, video, width=300, height=200):
    """
    Generate an HTML video player for a video given an object.
    """
    return {
        'id': id,
        'video': video,
        'width': width,
        'height': height,
    }


@register.inclusion_tag("video/thumbnail-popup.html")
def thumbnail_popup(id, video, width=300, height=200):
    """
    Generate a thumbnail image that triggers a modal video player
    """
    return {
        'id': id,
        'video': video,
        'width': width,
        'height': height,
    }


@register.tag
def get_taggedvideo_for_object(parser, token):
    """
    Retrieves a list of ``TaggedVideo`` objects associated with an object and
    stores them in a context variable.
    Usage::
       {% get_videos_for_object [object] as [varname] %}
    Example::
        {% get_videos_for_object object as videoslist %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError('%s tag requires exactly three arguments' % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError("second argument to %s tag must be 'as'" % bits[0])
    return TaggedVideoForObjectNode(bits[1], bits[3])


class TaggedVideoForObjectNode(Node):
    def __init__(self, obj, context_var):
        self.obj = Variable(obj)
        self.context_var = context_var

    def render(self, context):
        context[self.context_var] = \
            TaggedVideo.objects.get_for_object(self.obj.resolve(context))
        return ''
