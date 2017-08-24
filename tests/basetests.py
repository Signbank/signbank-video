# -*- coding: utf-8 -*-
import shutil
import os

from django.test import TestCase
from django.core.files import File
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from video.models import TaggedVideo


class BaseTest(TestCase):
    """
    This class simply defines the setUp() and
    tearDown() functions common to all the tests.
    """

    def setUp(self):
        # this is the path to the video used by the tests
        self.vidfilename1 = os.path.join(settings.MEDIA_ROOT, 'video1.mov')
        self.vidfilename2 = os.path.join(settings.MEDIA_ROOT, 'video2.mov')
        self.testfilename = os.path.join(settings.MEDIA_ROOT, 'SampleVideo_1280x720_1mb.mp4')
        self.videofile1 = File(open(self.vidfilename1, 'rb'), 'video1.mov')
        self.videofile2 = File(open(self.vidfilename2, 'rb'), 'video2.mov')
        self.testvideofile = File(open(self.testfilename, 'rb'))
        # Using this ContentType in tests because it should exist.
        self.content_type = ContentType.objects.get(app_label='video', model='taggedvideo')
        self.test_object = TaggedVideo.objects.add(content_type=self.content_type.id, object_id=0,
                                                   videofile=self.testvideofile)

    def tearDown(self):
        # After each test, delete any left over files that
        # were created by the test
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, settings.VIDEO_UPLOAD_LOCATION),
                      ignore_errors=True)

        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, settings.GLOSS_VIDEO_DIRECTORY),
                      ignore_errors=True)
