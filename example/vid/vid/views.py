from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from video.models import TaggedVideo, Video


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['taggedvideos'] = TaggedVideo.objects.all()
        context['test_content_type'] = ContentType.objects.get_for_model(TaggedVideo)
        try:
            context['test_object'] = context['taggedvideos'][0]
        except:
            # Creating a TaggedVideo object with one Video to make this example work.
            taggedvideo = TaggedVideo.objects.create(id=0, content_type=context['test_content_type'], object_id=0)
            Video.objects.create(tag=taggedvideo, videofile='SampleVideo_1280x720_1mb.mp4')
            context['test_object'] = taggedvideo
        return context
