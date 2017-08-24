# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from video.models import Video, TaggedVideo
from .basetests import BaseTest


class TaggedVideoTests(BaseTest):

    def test_TaggedVideoManager_add(self):
        """
        The add method on the taggedvideo manager creates a new
        object when none already exists for this object"""
        vid = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)

        self.assertEqual(ContentType.objects.get(app_label='video', model='taggedvideo'), self.content_type)
        self.assertEqual(1, vid.object_id)
        self.assertEqual(0, vid.video.version)

    def test_TaggedVideoManager_add_second(self):
        """
        The add method on the taggedvideo manager adds a new
        version of a video if one already exists"""

        vid1 = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)
        vid2 = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile2)

        self.assertEqual(1, vid1.object_id)
        self.assertEqual(0, vid1.video.version)
        self.assertEqual(vid1, vid1.video.tag)
        self.assertEqual(vid1, vid2)
        self.assertEqual(os.path.basename(vid1.video.videofile.name), self.videofile2.name)

        vv = Video.objects.filter(tag__object_id=1).order_by('version')
        # check that videos have correct versions, should start from 0->
        for i, v in enumerate(vv):
            self.assertEqual(i, v.version)
        # should be two versions
        self.assertEqual(vv.count(), 2)

    def test_TaggedVideoManager_revert(self):
        """
        The revert method removes the most recent
        video"""

        vid1 = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)
        vid2 = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile2)

        self.assertTrue(vid2.revert())
        self.assertEqual(os.path.basename(vid1.video.videofile.name), self.videofile1.name)

        # should be one version
        vv = Video.objects.filter(tag__object_id=1)
        self.assertEqual(vv.count(), 1)

    def test_Video_poster_path(self):
        """
        We can generate a poster image for a video
        """
        vid = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=1, videofile=self.videofile1)

        poster = vid.video.poster_url()
        poster_abs = settings.MEDIA_ROOT + poster
        self.assertTrue(os.path.exists(poster_abs),
                        "poster image %s is missing" % (poster_abs,))
        # do it again should give the same result, but won't have created the file
        poster2 = vid.video.poster_url()
        self.assertEqual(poster, poster2)
