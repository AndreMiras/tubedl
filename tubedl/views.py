import sys

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.template import Context, loader
from django.urls import reverse

from tubedl.forms import ContactForm
from videodl.forms import DownloadForm


def home(request):
    audio_only = request.session.get("audio_only")
    initial = {"audio_only": audio_only}
    form = DownloadForm(initial=initial)
    data = {
        "form": form,
    }
    return render(request, "videodl/download_form.html", data)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            subject = form.cleaned_data["subject"]
            subject = settings.EMAIL_SUBJECT_PREFIX + subject
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]
            recipients = [tup[1] for tup in settings.MANAGERS]
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)
            messages.success(request, "Message sent, redirecting to home page.")
            return HttpResponseRedirect(reverse("home"))
    else:
        form = ContactForm()
    data = {
        "form": form,
    }
    return render(request, "contact.html", data)


def error404(request):
    """
    Simply renders 404 error template for testing purpose.
    """
    data = {}
    return render(request, "404.html", data)


def error500(request):
    """
    Simply renders 500 error template for testing purpose.
    """
    data = {}
    return render(request, "500.html", data)


def custom_500(request):
    t = loader.get_template("500.html")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    data = {
        "exception_type": str(exc_type),
        "exception_value": exc_value,
    }
    return HttpResponseServerError(t.render(Context(data)))
