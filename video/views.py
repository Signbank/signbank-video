from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from video.models import GlossVideo
from video.forms import VideoUploadForGlossForm


def addvideo(request):
    '''
    View to process a video upload.
    '''
    if request.method == 'POST':
        form = VideoUploadForGlossForm(request.POST, request.FILES)
        if form.is_valid():
            gloss_id = form.cleaned_data['gloss_id']            
            vfile = form.cleaned_data['videofile']
            # Let's name the video
            # ex: 3.mp4   
            vfile.name = "%s.mp4"%(gloss_id)  
            # deal with any existing video for this sign
            old_videos = GlossVideo.objects.filter(gloss_id=gloss_id)
            for video in old_videos:
                video.reversion()
            video = GlossVideo(videofile=vfile, gloss_id=gloss_id)
            video.save()      
            messages.success(request, 
                "Your video has been successfully uploaded")
            return HttpResponseRedirect(reverse('video:successpage'))
    # if we can't process the form, just redirect back to the
    # referring page, should just be the case of hitting
    # Upload without choosing a file but could be
    # a malicious request, if no referrer, go back to root
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)
    
    
@login_required
def deletevideo(request, videoid):
    '''
    Remove the video for this gloss, if there is an older version
    then reinstate that as the current video (act like undo)
    '''
    if request.method == "POST":
        # deal with any existing video for this sign
        videos = GlossVideo.objects.filter(gloss_id=videoid).order_by('version')
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
    # Get all videos with criteria ...
    video = GlossVideo.objects.filter(gloss_id=videoid, version=0)
    # If no videos were found...
    if len(video) == 0:
        raise Http404("No poster for the video could be found")
    # Only one video can have a version of 0
    if len(video) > 1:
        # Django treats this as a 500 error
        # see -- https://docs.djangoproject.com/en/1.10/ref/views/#the-500-server-error-view
        raise ValueError()
    else:
        return redirect(video[0].poster_url())
    
def video(request, videoid):
    '''
    Redirect to the video url for this videoid
    '''
    # We want the latest video associated with this gloss_id (it has version 0)
    video = get_object_or_404(GlossVideo, gloss_id=videoid, version=0)
    return redirect(video)


# TODO talk to steve about this one
# Instead of initiating looking for the gloss here, initiate it
# in the dictionary app, and when it's found, look for its video here.      
'''
def iframe(request, videoid):
    """Generate an iframe with a player for this video"""    
    try:
        #gloss = Gloss.objects.get(pk=videoid)
        #glossvideo = gloss.get_video()
        
        if django_mobile.get_flavour(request) == 'mobile':
            videourl = glossvideo.get_mobile_url()
        else:
            videourl = glossvideo.get_absolute_url()
                
        posterurl = glossvideo.poster_url()
    except:
        gloss = None
        glossvideo = None
        videourl = None
        posterurl = None
    return render_to_response("iframe.html",
                              {'videourl': videourl,
                               'posterurl': posterurl,
                               'aspectRatio': settings.VIDEO_ASPECT_RATIO,
                               },
                               context_instance=RequestContext(request))
'''
    
    
def successpage(request):
    # If there is a success message to display
    if messages.get_messages(request):
        return render(request, "video/success_page.html")
    else:
    # If not go back to the index page
        return redirect('/')
