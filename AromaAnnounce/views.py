from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import AromaEvent
from AromaNote.models import AromaNote
from AromaUser.models import AromaUser

@require_http_methods(["GET"])
def announce(request):
    if request.user.is_authenticated():
        # get request.user's note repo
        event = AromaEvent.objects.all().order_by('-created_date')
        variables = RequestContext(request, {
            'event' : event,
            })
        return render_to_response('announce/announce_main.html', variables)
    notes = AromaNote.objects.all().order_by('-created')
    variables = RequestContext(request, {
        'note' : notes,
        })
    return render_to_response('note/note_main_unauth.html', variables)