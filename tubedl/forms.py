import urllib2
from django import forms


class DownloadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Adds Twitter Bootstrap 3 "form-control" class.
        """
        super(DownloadForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    url = forms.URLField(
        widget=forms.TextInput(attrs={
            'placeholder': 'http://somesite.com/video',
            }))
    audio_only = forms.BooleanField(
        widget=forms.HiddenInput,
        required=False)

    # TODO: also verify it's part of supported services
    def clean_giturl(self):
        data = self.cleaned_data['url']
        try:
            content = urllib2.urlopen(data)
        except urllib2.URLError as e:
            raise forms.ValidationError("The provided URL does not exist.")
        return data

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Adds Twitter Bootstrap 3 "form-control" class.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        widget=forms.Textarea
        )
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
