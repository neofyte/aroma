from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from AromaUser.models import AromaUser
from AromaPaper.models import AromaPaperEntry
from .forms import ArXivLinkForm

from lib.arxiv_retriever.arxiv_id_parser import arxiv_id_parser
from lib.arxiv_retriever.arxiv_query import arxiv_query
from lib.arxiv_retriever.arxiv_response_parser import xml_parser
from .validator import validate_identifier

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
    elif request.method == "POST":
        paper, paper.id = paper_search(request)
        if request.is_ajax():
            arxiv_dict = serializers.serialize("json", paper)
            return HttpResponse(json.dumps(arxiv_dict), mimetype='application/javascript')
        return HttpResponseRedirect('/paper/{0}/'.format(paper.id))

def _paper_save(arxiv_dict):
    paper = AromaPaperEntry(k=v for k,v in arxiv_dict)
    paper.save()
    return paper

@require_http_methods(["POST"])
def paper_search(request):
    arxiv_id = validate_identifier(request.POST['arxiv_id'])
    if arxiv_id:
        try:
            paper = AromaPaperEntry.objects.get(identifier=arxiv_id)
        except:
            id_cleaned = arxiv_id_parser(arxiv_id)
            xml = arxiv_query(id_cleaned)
            arxiv_dict = xml_parser(xml, arxiv_id)
            paper = _paper_save(arxiv_dict)
        return paper, paper.id
    else:
        raise Http404

