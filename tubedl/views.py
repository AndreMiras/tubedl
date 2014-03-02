import json
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tubedl.forms import DownloadForm, ContactForm


def home(request):
    form = DownloadForm() # An unbound form
    data = {
        'form': form,
    }
    return render(request, 'home.html', data)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = [tup[1] for tup in settings.MANAGERS]
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)
            messages.success(request, 'Message sent, redirecting to home page.')
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
    })
