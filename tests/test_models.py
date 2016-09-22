import os
import shutil

from django.test import TestCase
from django.core.files import File
from django.conf import settings

from video.models import Video, GlossVideo


class BaseModelTests(TestCase):
    '''
    This class simply defines the setUp() function
    which is common to the VideoTests class and the
    GlossVideoTests class.
    '''
    def setUp(self): 
        # this is the path to the video used by the tests
        self.vidfilename = os.path.join(settings.MEDIA_ROOT,'video.mp4')
        self.videofile = File(open(self.vidfilename, "rb"), "12345.mp4")
    

class VideoTests(BaseModelTests): 
    def tearDown(self):
        # After each test, delete any left over files that 
        # were created by the test
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, settings.VIDEO_UPLOAD_LOCATION),
            ignore_errors=True)
    
    def test_video_create(self):
        '''
        An instance the Video model should correspond to 
        an actual video in the file system, stored in the correct location
        '''
        vid = Video.objects.create(videofile=self.videofile)
        # new file should be located in the upload directory
        self.assertEquals(os.path.dirname(vid.videofile.name), 
            settings.VIDEO_UPLOAD_LOCATION)
        self.assertTrue(os.path.exists(vid.videofile.path), 
            "vidfile doesn't exist at %s" % (vid.videofile.path,))
        
    def test_video_delete(self):
        '''
        An instance of the Video model should be deletable.
        The file which it represents should be removed
        from the file system.
        '''
        vid = Video.objects.create(videofile=self.videofile)
        vid.delete_files()
        self.assertFalse(os.path.exists(vid.videofile.path), 
          "vidfile still exists after delete at %s" % (vid.videofile.path,))
          
        
class GlossVideoTests(BaseModelTests):
    def tearDown(self):
        # After each test, delete any left over files that 
        # were created by the test
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 
            settings.GLOSS_VIDEO_DIRECTORY),
             ignore_errors=True)
    
    def test_GlossVideo_create(self):
        '''
        An instance of the GlossVideo model should
        correspond to an actual video in the filesystem, 
        sroted in the correct location.
        '''
        vid = GlossVideo.objects.create(videofile=self.videofile) 
        self.assertEquals(os.path.dirname(os.path.dirname(vid.videofile.name )), 
            settings.GLOSS_VIDEO_DIRECTORY)
        self.assertTrue(os.path.exists(vid.videofile.path), 
            "vidfile doesn't exist at %s" % (vid.videofile.path,))
    
    def test_GlossVideo_delete(self):
        '''
        An instance of the GlossVideo model should
        be deletable. The file which it represents
        should be removed from the fily system.
        '''
        vid = GlossVideo.objects.create(videofile=self.videofile) 
        vid.delete_files()
        self.assertFalse(os.path.exists(vid.videofile.path), 
            "vidfile still exists after delete at %s" % (vid.videofile.path,))
            
    def test_reversion_revert_is_true_one_video(self):
        '''
        Calling reversion on a GlossVideo instance should
        increment its version, append .bak to its name,
        and this name change should be reflected in the
        file system.
        '''
        # create the video
        vid = GlossVideo.objects.create(videofile=self.videofile)
        oldname = vid.videofile.name
        vid.reversion()
        # The video's version should = 1
        self.assertEqual(vid.version, 1)
        # it's name should have .bak on the end of it
        self.assertEqual(vid.videofile.name, oldname+".bak")
        videos_in_directory = os.listdir(os.path.dirname(vid.videofile.path))
        self.assertEquals(len(videos_in_directory), 1)
        self.assertTrue(os.path.exists(vid.videofile.path),
            "vidfile doesn't exist at %s" % (vid.videofile.path,))
            
    def test_reversion_revert_is_false_one_video(self):
        '''
        Calling reversion with revert = False on the the only instance of 
        a GlossVideo with a particular name should delete it
        from the file system
        '''       
        # create the video
        vid = GlossVideo.objects.create(videofile=self.videofile)
        directory_of_video = os.path.dirname(vid.videofile.path)
        vid.reversion(revert=True)
        # The directory containing the video should be empty
        self.assertFalse(os.listdir(directory_of_video))
           
    def test_Video_poster_path(self):
        '''
        We can generate a poster image for a video
        '''
        vid = Video.objects.create(videofile=self.videofile)
        poster = vid.poster_path()
        poster_abs = os.path.join(settings.MEDIA_ROOT, poster)
        self.assertTrue(os.path.exists(poster_abs), 
            "poster image %s is missing" % (poster_abs,))
        # do it again should give the same result, but won't have created the file
        poster2 = vid.poster_path()
        self.assertEqual(poster, poster2) 
