from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from AromaUser.models import AromaUser
from AromaPaper.models import AromaPaperEntry
from .forms import ArXivLinkForm

@require_http_methods(["GET"])
def paper_main(request):
    if request.user.is_authenticated():
        # get request.user's note repo
        paper = AromaPaperEntry.objects.filter(author=request.user).order_by('-submitted')
        arxiv_link_form = ArXivLinkForm()
        variables = RequestContext(request, {
            'paper' : paper,
            'arXivLinkForm' : arxiv_link_form,
            })
        return render_to_response('paper/paper_main.html', variables)
    paper = AromaPaperEntry.objects.all().order_by('-submitted')
    variables = RequestContext(request, {
        'paper' : paper,
        })
    return render_to_response('paper/paper_main.html', variables)

@require_http_methods(["GET"])
def paper_detail(request, paper_id):
    pass

@require_http_methods(["GET", "POST"])
def paper_add(request):
    if request.method == "GET":
        arxiv_link_form = ArXivLinkForm()
        variables = RequestContext(request, {
            'arXivLinkForm' : arxiv_link_form,
            })
        return render_to_response('paper/paper_add.html', variables)
    else:
        pass