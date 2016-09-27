# -*- coding: latin-1 -*-
import datetime

from django.test import TestCase, RequestFactory
from django.conf import settings 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser, User, Permission
from django.contrib.messages.storage.fallback import FallbackStorage

from video.views import addvideo
from .basetests import BaseTest

def create_request(url, method, data=None, permission=None):
    '''
    This function creates one of various requests. The type
    of request that this function creates depends on the parametres
    of the function.
    
    Call this function in a test case, and use the returned
    request object as an argument to a view. 
    '''
    factory = RequestFactory()
    # Set up the user...
    user = create_user(permission)       
    if 'GET' in method.upper():
        request = factory.get(url)        
    elif 'POST' in method.upper():
        request = factory.post(url, data)
    else:
        raise ValueError("%s is an unrecognised method. It must be one of 'post' or 'get'"%(method))
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)      
    request.user = user      
    return request
    
    
def create_user(permission=None):
    users = User.objects.all()
    nusers = len(users)
    # If the user has already been created...
    if nusers != 1: 
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
    else:
        # If the user has already been created, use it 
        user = users[0]
    if permission is not None:
        permission = Permission.objects.get(name=permission)
        user.user_permissions.add(permission)             
    return user


class AddVideoTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/addvideo/'
        self.success_url = '/success/'
        self.data = {"gloss_id" : "3", "videofile" : self.videofile}
        
    def test_add_video_view_redirects_to_success_page_after_successful_request(self):
        '''
        The add video view should redirect 
        to the success view on succecssful upload of a video.
        '''
        request = create_request(url=self.url, method='post', data=self.data)
        response = addvideo(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('video:successpage'),response.url)
        
    def test_add_view_redirects_to_index_if_no_video_uploaded(self):
        '''
        The add video view should redirect to the index view if 
        no video is uploaded.
        '''
        request = create_request(url=self.url, method='post')
        response = addvideo(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/',response.url)
        
    def test_add_view_redirects_to_referer_if_referer_present_and_error(self):
        '''
        If the referer attribute in the request is present,
        then the view should redirect there on error.
        '''
        request = create_request(url=self.url, method='post')
        test_referer = 'test/test'
        request.META['HTTP_REFERER'] = test_referer
        response = addvideo(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_referer, response.url)
        
        
        
        
        
 
       
        
     
