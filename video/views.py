from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
            redirect_url = form.cleaned_data['redirect']
            # deal with any existing video for this sign
            old_videos = GlossVideo.objects.filter(gloss_id=gloss_id)
            for video in old_videos:
                video.reversion()
            video = GlossVideo(videofile=vfile, gloss_id=gloss_id)
            video.save()      
            # TODO: provide some feedback that it worked (if
            # immediate display of video isn't working)
            return redirect(redirect_url)
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
    video = get_object_or_404(GlossVideo, gloss_id=videoid)
    return redirect(video.poster_url())
    
    
def video(request, videoid):
    '''
    Redirect to the video url for this videoid
    '''
    video = get_object_or_404(GlossVideo, gloss_id=videoid)
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
    
    
    
