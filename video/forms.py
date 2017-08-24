# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType


class VideoUploadForm(forms.Form):
    """Form for uploading one video, with hidden fields for the content_type and object_id"""
    videofile = forms.FileField(label='')
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)


class VideoUploadMultipleForm(VideoUploadForm):
    """Form for uploading multiple videos, with hidden fields for the content_type and object_id"""
    videofile = forms.FileField(label='', widget=forms.FileInput(attrs={'multiple': True,}))


class VideoUploadPickContentTypeForm(VideoUploadForm):
    """Form for uploading one video, with ContentType and Object_id pickers."""
    content_type = forms.ModelChoiceField(label='ContentType', queryset=ContentType.objects.all())
    object_id = forms.IntegerField(label='object_id', widget=forms.NumberInput, min_value=0)


class VideoUploadMultiplePickContentTypeForm(VideoUploadPickContentTypeForm):
    """Form for uploading multiple videos, with ContentType and Object_id pickers."""
    videofile = forms.FileField(label='', widget=forms.FileInput(attrs={'multiple': True, }))

