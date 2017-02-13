import os

from django.conf import settings

from video.models import Video, TaggedVideo
from .basetests import BaseTest


class TaggedVideoTests(BaseTest):

    def test_TaggedVideoManager_add(self):
        """
        The add method on the taggedvideo manager creates a new
        object when none already exists for this tag"""

        vid = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)

        self.assertEqual("hello", vid.tag)
        self.assertEqual(0, vid.video.version)

    def test_TaggedVideoManager_add_second(self):
        """
        The add method on the taggedvideo manager adds a new
        version of a video if one already exists"""

        vid1 = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)
        vid2 = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile2)

        self.assertEqual("hello", vid1.tag)
        self.assertEqual(0, vid1.video.version)
        self.assertEqual(vid1, vid1.video.tag)
        self.assertEqual(vid1, vid2)
        self.assertEqual(os.path.basename(vid1.video.videofile.name), self.videofile2.name)

        # should be two versions
        vv = Video.objects.filter(tag__tag__exact="hello")
        self.assertEqual(vv.count(), 2)


    def test_TaggedVideoManager_revert(self):
        """
        The revert method removes the most recent
        video"""

        vid1 = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)
        vid2 = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile2)

        self.assertTrue(vid2.revert())
        self.assertEqual(os.path.basename(vid1.video.videofile.name), self.videofile1.name)

        # should be one version
        vv = Video.objects.filter(tag__tag__exact="hello")
        self.assertEqual(vv.count(), 1)


    def test_Video_poster_path(self):
        '''
        We can generate a poster image for a video
        '''
        vid = TaggedVideo.objects.add(category="test", tag="hello", videofile=self.videofile1)

        poster = vid.video.poster_url()
        poster_abs = settings.MEDIA_ROOT + poster
        self.assertTrue(os.path.exists(poster_abs),
            "poster image %s is missing" % (poster_abs,))
        # do it again should give the same result, but won't have created the file
        poster2 = vid.video.poster_url()
        self.assertEqual(poster, poster2)
