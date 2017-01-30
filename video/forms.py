from django import forms

from video.models import TaggedVideo

class VideoUploadForm(forms.Form):
    """Form for video upload with a hidden field for the tag"""
    videofile = forms.FileField(label="Upload Video")
    tag = forms.CharField(widget=forms.HiddenInput)
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)


class VideoUploadTagForm(forms.Form):
    """Form for video upload including the tag field"""
    videofile = forms.FileField(label="Upload Video")
    tag = forms.CharField()
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)
