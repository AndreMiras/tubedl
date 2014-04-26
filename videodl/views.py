import os
import json
import urllib
from mimetypes import MimeTypes
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from youtube_dl import YoutubeDL, extractor
from youtube_dl.utils import DownloadError
from youtube_dl.postprocessor.ffmpeg import FFmpegExtractAudioPP
from videodl.forms import DownloadForm, DownloadFormat
from videodl.models import DownloadLink


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
        if extract_audio:
            info['ext'] = 'mp3'
            # FFmpegExtractAudioPP(
            #     preferredcodec=opts.audioformat, preferredquality=opts.audioquality, nopostoverwrites=opts.nopostoverwrites))
            audio_extractor = FFmpegExtractAudioPP(
                preferredcodec=info['ext'])
            ydl.add_post_processor(audio_extractor)
        video_path = "%s%s.%s" % (DOWNLOAD_DIR, info['id'], info['ext'])
        ydl.download([url])
        return (video_path, info)

def serve_file(file_path, filename=None):
    if filename is None:
        filename = os.path.basename(file_path)
    mime = MimeTypes()
    url = urllib.pathname2url(file_path)
    mimetype, encoding = mime.guess_type(url)
    f = open(file_path)
    response = HttpResponse(f.read(), mimetype = mimetype)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = 'attachment; filename=' + filename
    f.close()
    return response

def video_info(request, download_link_uuid):
    download_link = get_object_or_404(DownloadLink, uuid=download_link_uuid)
    url = download_link.url
    if request.method == 'POST':
        form = DownloadFormat(request.POST)
        # TODO: else (!is_valid) this could crash with a video_thumbnail & video_title not defined
        if form.is_valid():
            audio_only = form.cleaned_data['audio_only']
            # save form value to session for user convenience
            request.session['audio_only'] = audio_only
            video_path, info = start_download(url, audio_only)
            title_sanitized = urllib.quote(info.get('title').encode('utf8'))
            filename = title_sanitized + '.' + info.get('ext')
            response = serve_file(video_path, filename)
            return response
    else:
        # restores form state from session for user convenience
        audio_only = request.session.get('audio_only')
        initial = {'audio_only': audio_only}
        form = DownloadFormat(initial=initial)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.add_default_info_extractors()
            try:
                # TODO: do the extraction while downloading
                info = ydl.extract_info(url, download=False)
            except DownloadError as ex:
                messages.error(
                    request,
                    "Could not download your video.\n" +
                    "Exception was: %s" % (ex.message))
                return HttpResponseRedirect(reverse('home'))
        video_thumbnail = info.get('thumbnail')
        video_title = info.get('title')
    data = {
        'form': form,
        'video_thumbnail': video_thumbnail,
        'video_title': video_title,
    }
    return render(request, 'videodl/video_info.html', data)

def download_form(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            # save the download info as a DownloadLink for later reshare
            download_link, created = DownloadLink.objects.get_or_create(url=url)
            # messages.success(request, 'Your download will start shortly.')
            return HttpResponseRedirect(reverse('video_info', kwargs={ 'download_link_uuid': download_link.uuid }))
    else:
        form = DownloadForm()
    data = {
        'form': form,
    }
    return render(request, 'videodl/download_form.html', data)

def supported_sites(request):
    sites = [x.IE_NAME for x in extractor.gen_extractors()]
    sites.sort()
    data = {
        "sites": sites,
    }
    return render(request, 'videodl/supported_sites.html', data)
