from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

from video.models import TaggedVideo
from video.forms import VideoUploadMultipleForm


def upload(request):
    """Upload a new video or multiple videos."""

    # Use VideoUploadMultipleForm, should work for both 1 file and multiple files.
    form = VideoUploadMultipleForm(request.POST, request.FILES)
    if form.is_valid():
        object_id = form.cleaned_data['object_id']
        content_type = form.cleaned_data['content_type']

        # Add all files sent in the form.
        for f in request.FILES.getlist('videofile'):
            f.name = "%s.mp4" % (object_id,) # Name the video, ex: 3.mp4
            try:
                TaggedVideo.objects.add(content_type, object_id, f)
            except:
                messages.error(request, "Error, unable to upload for, ContentType: " + form.cleaned_data['content_type']
                               + " Object_ID: " + form.cleaned_data['object_id'])
                break
            else:
                messages.success(request, "Your video: " + str(f) + " has been successfully uploaded")

        return HttpResponseRedirect(form.cleaned_data['redirect'])
    else:
        if 'HTTP_REFERER' in request.META:
            url = request.META['HTTP_REFERER']
        else:
            url = '/'
        return redirect(url)


def video(request, content_type_id, object_id):
    '''
    Redirect to the video url for this content_type + object_id
    '''
    taggedvideo = get_object_or_404(TaggedVideo, content_type__id=content_type_id, object_id=object_id)
    return redirect(taggedvideo.get_absolute_url())


def deletevideo(request, content_type_id, object_id):
    '''
    Remove the video for this gloss, if there is an older version
    then reinstate that as the current video (act like undo)
    '''
    if request.method == "POST":
        video = get_object_or_404(TaggedVideo, content_type__id=content_type_id, object_id=object_id)
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


def poster(request, content_type_id, object_id):
    """Generate a still frame for a video (if needed) and
    generate a redirect to the static server for this frame"""
    # We want the latest video associated with this object_id(it has version 0)
    video = get_object_or_404(TaggedVideo, content_type__id=content_type_id, object_id=object_id)
    return redirect(video.poster_url())
