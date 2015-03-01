import os
import urllib
from mimetypes import MimeTypes
from django.http import Http404, JsonResponse
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
    'keepvideo': True,
}

def supported_sites(request):
    """
    Returns the list of support sites.
    """
    sites = [x.IE_NAME for x in extractor.gen_extractors()]
    sites.sort()
    data = {
        "sites": sites,
    }
    return render(request, 'videodl/supported_sites.html', data)

# This one is being pulled by $.ajax in the js.
def get_progress(request):
    # fetches the count or 0
    progress = request.session.get('progress', 0)
    # fetch the status or False
    done = request.session.get('done', False)
    data = {
        "done": done,
        "progress": progress,
    }
    return JsonResponse(data)

def progress_hook(d):
    if d['status'] == 'downloading':
        print "Downloading"
        # d['downloaded_bytes']
        # d['total_bytes']
    elif d['status'] == 'finished':
        print "Done downloading, now converting ..."

def extract_file_path_helper(id, ext):
    file_path = YDL_OPTIONS['outtmpl'] % ({ 'id': id, 'ext': ext })
    return file_path

def extract_info_helper(url, extract_audio):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.add_default_info_extractors()
        info = ydl.extract_info(url, download=False)
        if extract_audio:
            info['ext'] = 'mp3'
        return info

def download_on_server(url, extract_audio=False):
    """
    Downloads the video locally on the server before serving it to clients.
    """
    with YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.add_progress_hook(progress_hook)
        # TODO: do the extraction while downloading
        # TODO: the info was already extracted at this point
        info = extract_info_helper(url, extract_audio)
        if extract_audio:
            info['ext'] = 'mp3'
            audio_extractor = FFmpegExtractAudioPP(
                downloader=ydl,
                preferredcodec=info['ext'])
            ydl.add_post_processor(audio_extractor)
        file_path = extract_file_path_helper(info['id'], info['ext'])
        ydl.download([url])
        return (file_path, info)

def video_info(request, download_link_uuid):
    """
    Retrieves video info and saves it to server database.
    """
    download_link = get_object_or_404(DownloadLink, uuid=download_link_uuid)
    url = download_link.url
    # restores form state from session for user convenience
    audio_only = request.session.get('audio_only')
    initial = { 'audio_only': audio_only }
    form = DownloadFormat(initial=initial)
    try:
        info = extract_info_helper(url, audio_only)
    except DownloadError as ex:
        messages.error(
            request,
            "Could not download your video.\n" +
            "Exception was: %s" % (ex.message))
        return HttpResponseRedirect(reverse('home'))
    video_thumbnail = info.get('thumbnail')
    video_title = info.get('title')
    download_link.title = video_title
    download_link.save()
    data = {
        'form': form,
        'video_thumbnail': video_thumbnail,
        'download_link': download_link,
    }
    return render(request, 'videodl/video_info.html', data)

def download_form(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            # saves the download info as a DownloadLink for later reshare
            download_link, created = DownloadLink.objects.get_or_create(url=url)
            # messages.success(request, 'Your download will start shortly.')
            return HttpResponseRedirect(reverse('video_info', kwargs={ 'download_link_uuid': download_link.uuid }))
    else:
        form = DownloadForm()
    data = {
        'form': form,
    }
    return render(request, 'videodl/download_form.html', data)

def serve_file_helper(file_path, filename=None):
    """
    Serves the given local server file to remote client via attachment.
    """
    if filename is None:
        filename = os.path.basename(file_path)
    mime = MimeTypes()
    url = urllib.pathname2url(file_path)
    mimetype, encoding = mime.guess_type(url)
    f = open(file_path)
    response = HttpResponse(f.read(), content_type = mimetype)
    response['Content-Length'] = os.path.getsize(file_path)
    # how-to-encode-the-filename-parameter-of-content-disposition-header-in-http
    # http://stackoverflow.com/a/20933751
    filename_encoded = urllib.quote(filename.encode('utf8'))
    response['Content-Disposition'] = "attachment; filename=\"%s\"; filename*=utf-8''%s" % (filename, filename_encoded)
    f.close()
    return response

def prepare_download_redirect(request, download_link_uuid):
    """
    Downloads the file on the local server if needed and redirects the client
    to the download when ready.
    """
    download_link = get_object_or_404(DownloadLink, uuid=download_link_uuid)
    url = download_link.url
    if request.method == 'POST':
        form = DownloadFormat(request.POST)
        download_link.views += 1
        download_link.save()
        if form.is_valid():
            audio_only = form.cleaned_data['audio_only']
            # save form value to session for user convenience
            request.session['audio_only'] = audio_only
            try:

                # try to retrieve file from previous download
                file_path = download_link.get_file_path(audio_only)
                # if file_path not in download_link.get_file_paths():
                if not os.path.isfile(file_path):
                    # or download it then "cache" it (for later use)
                    file_path, info = download_on_server(url, audio_only)
                    download_link.set_file_path(file_path, audio_only)
                    download_link.title = info.get('title')
                    download_link.save()
            except DownloadError as ex:
                messages.error(
                    request,
                    "Could not download your video.\n" +
                    "Exception was: %s" % (ex.message))
                return HttpResponseRedirect(reverse('home'))
            if audio_only:
                download_redirect_url = reverse('serve_audio_download',
                    kwargs={ 'download_link_uuid': download_link_uuid })
            else:
                download_redirect_url = reverse('serve_video_download',
                    kwargs={ 'download_link_uuid': download_link_uuid })
            data = { "download_redirect_url": download_redirect_url }
            # return HttpResponseRedirect(download_redirect_url)
            return JsonResponse(data)
    return HttpResponseRedirect(reverse('video_info',
        kwargs={ 'download_link_uuid': download_link_uuid }))

def serve_download_helper(request, download_link_uuid, extract_audio=False):
    download_link = get_object_or_404(DownloadLink, uuid=download_link_uuid)
    file_path = download_link.get_file_path(extract_audio)
    url = download_link.url
    _, extension = os.path.splitext(file_path)
    # title_sanitized = download_link.get_url_friendly_title()
    # filename = title_sanitized + extension
    filename = download_link.title + extension
    try:
        response = serve_file_helper(file_path, filename)
    except IOError:
        raise Http404
    return response

def serve_video_download(request, download_link_uuid):
    extract_audio = False
    return serve_download_helper(request, download_link_uuid, extract_audio)

def serve_audio_download(request, download_link_uuid):
    extract_audio = True
    return serve_download_helper(request, download_link_uuid, extract_audio)

