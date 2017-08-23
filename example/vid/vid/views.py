from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from video.models import TaggedVideo


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['videos'] = TaggedVideo.objects.all()
        context['test_content_type'] = ContentType.objects.get_for_model(TaggedVideo)
        try:
            context['test_object'] = context['videos'][0]
        except:
            context['test_object'] = None
        return context
