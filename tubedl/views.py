import os
import json
import urllib
from mimetypes import MimeTypes
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from youtube_dl import YoutubeDL
from tubedl.forms import DownloadForm, ContactForm


DOWNLOAD_DIR = "/tmp/"

def start_download(url, directory):
    if directory:
        directory = os.path.abspath(directory) + '/'
    ydl_options = {
        # 'outtmpl': directory + u'%(title)s-%(id)s.%(ext)s',
        'outtmpl': directory + u'%(id)s.%(ext)s',
    }
    with YoutubeDL(ydl_options) as ydl:
        ydl.add_default_info_extractors()
        # TODO: do the extraction while downloading
        info = ydl.extract_info(url, download=False)
        video_path = "%s%s.%s" % (directory, info['id'], info['ext'])
        ydl.download([url])
        return video_path


def serve_file(file_path):
    basename = os.path.basename(file_path)
    mime = MimeTypes()
    url = urllib.pathname2url(file_path)
    mimetype, encoding = mime.guess_type(url)
    f = open(file_path)
    response = HttpResponse(f.read(), mimetype = mimetype)
    response['Content-Disposition'] = 'attachment; filename=' + basename
    f.close()
    return response

def home(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            video_path = start_download(url, DOWNLOAD_DIR)
            # messages.success(request, 'Your download will start shortly.')
            response = serve_file(video_path)
            return response
    else:
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
