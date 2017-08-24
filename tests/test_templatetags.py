# -*- coding: utf-8 -*-
from video.models import TaggedVideo
from .basetests import BaseTest
from django.template import Template, Context


class TemplateTagTests(BaseTest):

    def test_uploadform(self):

        tpl = Template("{% load videotags %} {% uploadform %}")

        rendered = tpl.render(Context({}))
        self.assertIn('form', rendered)
        self.assertIn('content_type', rendered)
        self.assertIn('object_id', rendered)

    def test_uploadform_preset(self):

        tpl = Template("{% load videotags %} {% uploadform obj=test_object multiple=False %}")

        rendered = tpl.render(Context({'test_object': self.test_object, }))
        self.assertIn('form', rendered)
        self.assertIn('content_type', rendered)
        self.assertIn('object_id', rendered)
        self.assertIn('name="content_type" value="%s"' % self.test_object.content_type.id, rendered)
        self.assertIn('name="object_id" value="%s"' % self.test_object.id, rendered)

    def test_uploadform_videofile_multiple(self):

        tpl = Template("{% load videotags %} {% uploadform obj=test_object multiple=True %}")
        rendered = tpl.render(Context({'test_object': self.test_object, }))
        self.assertIn('multiple', rendered)

    def test_player(self):

        vid = TaggedVideo.objects.add(content_type=self.test_object.content_type.id,
                                      object_id=self.test_object.object_id, videofile=self.videofile1)
        tpl = Template("{% load videotags %}"
                       "{% videoplayer id='xyzzy' video=test_object.video %}")

        rendered = tpl.render(Context({'test_object': vid, }))

        self.assertIn("id='signbank-videoxyzzy'", rendered)
        self.assertIn(vid.video.videofile.name, rendered)
        self.assertIn('</video>', rendered)

    def test_thumbnail_popup(self):

        vid = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)

        tpl = Template("{% load videotags %} {% thumbnail_popup id='xyzzy' video=test_object %}")

        rendered = tpl.render(Context({'test_object': vid, }))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn(vid.video.videofile.name, rendered)
        self.assertIn('</video>', rendered)
        self.assertIn(vid.poster_url(), rendered)

    def test_uploadform_modal(self):

        tpl = Template("{% load videotags %} {% upload_modal id='xyzzy' multiple=False %}")

        rendered = tpl.render(Context({}))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn('modal', rendered)
        self.assertIn('content_type', rendered)
        self.assertIn('object_id', rendered)

    def test_uploadform_modal_bound_object(self):

        vid = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)

        tpl = Template("{% load videotags %} {% upload_modal id='xyzzy' obj=test_object multiple=False %}")

        rendered = tpl.render(Context({'test_object': vid, }))
        self.assertIn('id="xyzzy"', rendered)
        self.assertIn('modal', rendered)
        self.assertIn('content_type', rendered)
        self.assertIn('object_id', rendered)
        self.assertIn('name="content_type" value="%s"' % vid.content_type.id, rendered)
        self.assertIn('name="object_id" value="%s"' % vid.id, rendered)

    def test_get_taggedvideo_for_object(self):

        vid = TaggedVideo.objects.create(id=1001, content_type=self.test_object.content_type,
                                         object_id=self.test_object.id)

        tpl = Template("{% load videotags %}{% get_taggedvideo_for_object test_object as taggedvideo %}"
                       "id={{taggedvideo.id}}")

        rendered = tpl.render(Context({'test_object': self.test_object, }))
        self.assertIn('id=%s' % vid.id, rendered)
