from django.test import TestCase
from django.core.urlresolvers import resolve

from video.views import addvideo, deletevideo, poster, video


class VideoURLs(TestCase):
    def test_upload_url_resolves_to_addvideo_view(self):
        '''
        '/upload/' should be routed to the 'addvideo' function
        in 'views.py'
        '''
        found = resolve('/upload/')
        self.assertEqual(found.func, addvideo)

    def test_delete_video_url_resolves_to_deletevideo_view(self):
       '''
       '/delete/1/', for example, should be routed to the 'deletevideo'
       function in 'views.py'
       '''
       found = resolve('/delete/1/')
       self.assertEqual(found.func, deletevideo)         
       
    def test_poster_url_resolves_to_poster_view(self):
       '''
       '/poster/1/', for example, should be routed to the 'poster'
       function in 'views.py'
       '''
       found = resolve('/poster/1/')
       self.assertEqual(found.func, poster)
       
    def test_video_url_resolves_to_video_view(self):
        '''
        '/video/1/', for example, should be routed to the
        'video' function in 'views.py'      
        '''  
        found = resolve('/video/1/')
        self.assertEqual(found.func, video)
        

    
