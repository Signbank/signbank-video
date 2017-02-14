# -*- coding: latin-1 -*-
import datetime

from django.test import TestCase, RequestFactory, override_settings
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser, User, Permission
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import MultipleObjectsReturned

from video.views import upload, deletevideo, poster, video
from video.models import TaggedVideo
from .basetests import BaseTest

def create_request(url, method, data=None, permission=None):
    '''
    This function creates one of various requests.
    param 1 - url) url can be anything becase views are called directly.
    param 2 - method) String, either 'get' or 'post'.
    param 3 - data) A dictionary of data to be passed to post request.
    param 4 - permission) String, encodes the permission of the request

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
        self.data = {"tag" : "3",
                     "category": self.category,
                     "videofile" : self.videofile1,
                     "redirect": '/redirect'
                     }

    def test_add_video_view_redirects_after_successful_request(self):
        '''
        The add video view should redirect
        to the given redirect url
        '''
        request = create_request(url=self.url, method='post', data=self.data)
        response = upload(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.data['redirect'], response.url)

    def test_add_view_redirects_to_index_if_no_video_uploaded(self):
        '''
        The add video view should redirect to the index view if
        no video is uploaded.
        '''
        request = create_request(url=self.url, method='post')
        response = upload(request)
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
        response = upload(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_referer, response.url)

    def test_add_video_calls_revert_on_existing_videos(self):
        '''If addvideo is called for a tag that already contains
            a video, then that video should go through revert
        '''
        request = create_request(url=self.url, method='post', data=self.data)
        # First, create the video
        tag = 3
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        # Now, add a video via addvideo
        response = upload(request)

        # There should now be two videos for the tag
        self.assertEqual(2, vid.versions())


class DeleteVideoTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = reverse('video:delete', kwargs={'category': self.category, 'tag': 1})

    def test_deletevideo_redirects_to_index_on_successful_delete_if_no_referer(self):
        '''
        The deletevideo view should redirect to index on successful delete
        if there is no referer.
        '''
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        request = create_request(url=self.url, method='post')
        response = deletevideo(request, self.category, tag)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_deletevideo_redirects_to_referer_on_successful_delete_if_referer_given(self):
        '''
        The deletevideo view should redirect to referer if
        it's given and on success.
        '''
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        request = create_request(url=self.url, method='post')
        referer_test = '/test/test'
        request.META['HTTP_REFERER'] = referer_test
        response = deletevideo(request, self.category, tag)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, referer_test)

    def test_deletevideo_removes_video(self):
        '''
        The deletevideo view should delete the video
        '''
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        self.assertEqual(1, vid.versions())
        request = create_request(url=self.url, method='post')
        response = deletevideo(request, self.category, tag)
        vids = TaggedVideo.objects.filter(tag=tag, category=self.category)
        self.assertEqual(0, vids.count())

    def test_deletevideo_reverts_video_if_more_than_one_video(self):
        '''
        The deletevideo view should delete the latest video
        and revert the second latest video.
        '''
        # First, create the video
        tag = 1
        vid1 = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        # Revert the first video
        vid1.revert()
        # Now, create another video
        tag = 1
        vid2 = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        # Now, delete the latest video
        request = create_request(url=self.url, method='post')
        response = deletevideo(request, self.category, tag)
        # There should be one video
        videos =  TaggedVideo.objects.all()
        self.assertEqual(len(videos), 1)

class PosterTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/poster/1/'

    def test_poster_returns_404_if_video_does_not_exist(self):
        request = create_request(url=self.url, method='post')
        # No video with this gloss_is exists...
        tag = 1
        # The view should raise a http404 exception...
        self.assertRaises(Http404, poster, request, self.category, tag)

    def test_poster_returns_poster_url_if_vid_exists(self):
        request = create_request(url=self.url, method='post')
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        response = poster(request, self.category, tag)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, vid.poster_url())


class VideoTests(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/video/1/'

    def test_video_exists_and_is_only_one_with_tag(self):
        '''If a video exists then the video view should return its url'''
        request = create_request(url=self.url, method='get')
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        response = video(request, self.category, tag)
        self.assertEqual(vid.get_absolute_url(), response.url)
        self.assertEqual(response.status_code, 302)

    def test_video_exists_and_there_is_another_with_the_tag(self):
        '''If two videos with the same tag exist, then
           the video with version 0 should have its url returned.
        '''
        request = create_request(url=self.url, method='get')
        # First, create the video
        tag = 1
        vid = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        vid.revert()
        # Now, add another video...
        vid2 = TaggedVideo.objects.add(videofile=self.videofile1, tag=tag, category=self.category)
        # The video with version 0 should have its url returned...
        response = video(request, self.category, tag)
        self.assertEqual(vid2.get_absolute_url(), response.url)
        self.assertEqual(response.status_code, 302)
