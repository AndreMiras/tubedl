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
from youtube_dl.postprocessor.ffmpeg import FFmpegExtractAudioPP
from videodl.forms import DownloadForm


DOWNLOAD_DIR = "/tmp/"
YDL_OPTIONS = {
    # 'outtmpl': DOWNLOAD_DIR + u'%(title)s-%(id)s.%(ext)s',
    'outtmpl': DOWNLOAD_DIR + u'%(id)s.%(ext)s',
}

def start_download(url, extract_audio=False):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.add_default_info_extractors()
        # TODO: do the extraction while downloading
        info = ydl.extract_info(url, download=False)
        ext = info['ext']
        if extract_audio:
            ext = 'mp3'
            # FFmpegExtractAudioPP(
            #     preferredcodec=opts.audioformat, preferredquality=opts.audioquality, nopostoverwrites=opts.nopostoverwrites))
            audio_extractor = FFmpegExtractAudioPP(
                preferredcodec=ext)
            ydl.add_post_processor(audio_extractor)
        video_path = "%s%s.%s" % (DOWNLOAD_DIR, info['id'], ext)
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

def download_form(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            audio_only = form.cleaned_data['audio_only']
            # save form value to session for user convenience
            request.session['audio_only'] = audio_only
            video_path = start_download(url, audio_only)
            # messages.success(request, 'Your download will start shortly.')
            response = serve_file(video_path)
            return response
    else:
        # restores form state from session for user convenience
        audio_only = request.session.get('audio_only')
        initial = {'audio_only': audio_only}
        form = DownloadForm(initial=initial)
    data = {
        'form': form,
    }
    return render(request, 'videodl/download_form.html', data)
