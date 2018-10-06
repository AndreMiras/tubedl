from urllib.error import URLError
from urllib.request import urlopen

from django import forms
from youtube_dl import extractor

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
        self.fields['url'].widget = forms.TextInput(attrs={
            'placeholder': 'http://somesite.com/video'})
        # Adds Twitter Bootstrap 3 "form-control" class.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # large input
        self.fields['url'].widget.attrs['class'] += ' input-lg'

    def clean_url(self):
        """
        - verifies at least one extractor recognizes it
        - verifies the URL exists
        """
        url = self.cleaned_data['url']
        extractors = list(extractor._ALL_CLASSES)
        # GenericIE always returns True for suitable(url)
        extractors.remove(extractor.generic.GenericIE)
        if True not in [x.suitable(url) for x in extractors]:
            raise forms.ValidationError("URL not supported.")
        # verifies the URL exists
        try:
            urlopen(url)
        except URLError:
            raise forms.ValidationError("The provided URL does not exist.")
        return url


class DownloadFormat(forms.Form):
    audio_only = forms.BooleanField(
        widget=forms.HiddenInput,
        required=False)
