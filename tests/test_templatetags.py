import os

from django.conf import settings

from video.models import Video, TaggedVideo
from .basetests import BaseTest
from django.template import Template, Context


class TemplateTagTests(BaseTest):

    def test_uploadform(self):

        tpl = Template("{% load videotags %} {% uploadform %}")

        rendered = tpl.render(Context({}))
        self.assertIn('form', rendered)
        self.assertIn('category', rendered)
        self.assertIn('tag', rendered)

    def test_uploadform_preset(self):

        tpl = Template("{% load videotags %} {% uploadform category='foo' tag='bar' %}")

        rendered = tpl.render(Context({}))
        self.assertIn('form', rendered)
        self.assertIn('foo', rendered)
        self.assertIn('bar', rendered)

    def test_player(self):

        vid = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)

        tpl = Template("{% load videotags %} {% videoplayer elementid='xyzzy' category='test' tag='hello' %}")

        rendered = tpl.render(Context({}))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn(vid.video.videofile.name, rendered)
        self.assertIn('</video>', rendered)


    def test_thumbnail_popup(self):

        vid = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)

        tpl = Template("{% load videotags %} {% thumbnail_popup id='xyzzy' category='test' tag='hello' %}")

        rendered = tpl.render(Context({}))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn(vid.video.videofile.name, rendered)
        self.assertIn('</video>', rendered)
        self.assertIn(vid.poster_url(), rendered)


    def test_uploadform_modal(self):

        tpl = Template("{% load videotags %} {% upload_modal id='xyzzy' category='foo' tag='bar' %}")

        rendered = tpl.render(Context({}))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn('modal', rendered)
        self.assertIn('category', rendered)
        self.assertIn('tag', rendered)
