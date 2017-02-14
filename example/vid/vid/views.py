from django.views.generic import TemplateView
from video.models import TaggedVideo

class Home(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['videos'] = TaggedVideo.objects.all()
        return context
