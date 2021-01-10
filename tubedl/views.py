import sys

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader

from videodl.forms import DownloadForm


def home(request):
    audio_only = request.session.get("audio_only")
    initial = {"audio_only": audio_only}
    form = DownloadForm(initial=initial)
    data = {
        "form": form,
    }
    return render(request, "videodl/download_form.html", data)


def error500(request):
    t = loader.get_template("500.html")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    data = {
        "exception_type": str(exc_type),
        "exception_value": exc_value,
    }
    return HttpResponseServerError(t.render(data))
