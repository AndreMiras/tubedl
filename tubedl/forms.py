from django import forms


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Adds Twitter Bootstrap 3 "form-control" class.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
