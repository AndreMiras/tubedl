import urllib2
from youtube_dl import extractor
from django import forms
from videodl.models import DownloadLink


class DownloadForm(forms.ModelForm):
    class Meta:
        model = DownloadLink
        fields = ['url']

    def __init__(self, *args, **kwargs):
        """
        Customizes the URL widget with place order.
        Adds Twitter Bootstrap 3 "form-control" class.
        """
        super(DownloadForm, self).__init__(*args, **kwargs)
        # Customizes the URL widget with place order.
        self.fields['url'].widget = widget=forms.TextInput(attrs={
            'placeholder': 'http://somesite.com/video',})
        # Adds Twitter Bootstrap 3 "form-control" class.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean_url(self):
        """
        - verifies the URL exists
        - verifies at least one extractor recognizes it
        """
        url = self.cleaned_data['url']
        extractors = list(extractor._ALL_CLASSES)
        # GenericIE always returns True for suitable(url)
        extractors.remove(extractor.generic.GenericIE)
        if True not in [x.suitable(url) for x in extractors]:
            raise forms.ValidationError("URL not supported.")
        try:
            content = urllib2.urlopen(url)
        except urllib2.URLError as e:
            raise forms.ValidationError("The provided URL does not exist.")
        return url


class DownloadFormat(forms.Form):
    audio_only = forms.BooleanField(
        widget=forms.HiddenInput,
        required=False)
