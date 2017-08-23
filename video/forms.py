from django import forms


class VideoUploadForm(forms.Form):
    """Form for video upload with a hidden field for the content_type and object_id"""
    videofile = forms.FileField(label="")
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    redirect = forms.CharField(widget=forms.HiddenInput, required=False)


class VideoUploadMultipleForm(VideoUploadForm):
    """Form for video upload including the content_type and object_id fields"""
    videofile = forms.FileField(label=False, widget=forms.FileInput(attrs={'multiple': True,}))
