from django import forms

from video.models import TaggedVideo

class VideoUploadForm(forms.Form):
    """Form for video upload with a hidden field for the category and tag"""
    videofile = forms.FileField(label="Upload Video")
    category = forms.CharField(widget=forms.HiddenInput)
    tag = forms.CharField(widget=forms.HiddenInput)
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)


class VideoUploadTagForm(forms.Form):
    """Form for video upload including the category and tag fields"""
    videofile = forms.FileField(label="Upload Video")
    category = forms.CharField()
    tag = forms.CharField()
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)
