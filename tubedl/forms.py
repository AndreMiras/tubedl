import urllib2
from django import forms

class DownloadForm(forms.Form):
    url = forms.URLField(
        widget=forms.TextInput(attrs={
            'placeholder': 'http://somesite.com/video',
            'class': 'input-xxlarge',
            }))

    # TODO: also verify it's part of supported services
    def clean_giturl(self):
        data = self.cleaned_data['url']
        try:
            content = urllib2.urlopen(data)
        except urllib2.URLError as e:
            raise forms.ValidationError("The provided URL does not exist.")
        return data

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-xlarge',
            }))
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
