import shutil
import os

from django.test import TestCase
from django.core.files import File
from django.conf import settings


class BaseTest(TestCase):
    '''
    This class simply defines the setUp() and 
    tearDown() functions common to all the tests.
    '''
    def setUp(self): 
        # this is the path to the video used by the tests
        self.vidfilename = os.path.join(settings.MEDIA_ROOT,'video.mp4')
        self.videofile = File(open(self.vidfilename, "rb"), "12345.mp4")
        
    def tearDown(self):
        # After each test, delete any left over files that 
        # were created by the test
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, settings.VIDEO_UPLOAD_LOCATION),
            ignore_errors=True) 
            
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 
            settings.GLOSS_VIDEO_DIRECTORY),
             ignore_errors=True)
