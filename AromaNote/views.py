from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.db.models.signals import post_save

from .models import AromaNote
from .forms import AromaNoteForm
from AromaUser.models import AromaUser

@require_http_methods(["GET"])
def note_main(request):
    if request.user.is_authenticated():
        # get request.user's note repo
        notes = AromaNote.objects.filter(author=request.user).order_by('-created')
        variables = RequestContext(request, {
            'note' : notes,
            })
        return render_to_response('note/note_main.html', variables)
    notes = AromaNote.objects.all().order_by('-created')
    variables = RequestContext(request, {
        'note' : notes,
        })
    return render_to_response('note/note_main_unauth.html', variables)

@require_http_methods(["GET"])
def note_repo(request, user_id):
    #get user_id's note repo

    user = get_object_or_404(AromaUser, pk=user_id)
    if request.user == user:
        return HttpResponseRedirect(reverse('note_main'))
    notes = AromaNote.objects.filter(author=user).order_by('-created')
    variables = RequestContext(request, {
        'nickname' : user.nickname,
        'note' : notes,
    })
    return render_to_response('note/note_repo.html', variables)

@login_required(login_url='/auth/signin/')
@require_http_methods(["GET", "POST"])
def note_create(request):
    # create a note
    errors=[]
    if request.method == "GET":
        # get an empty edit board
        form = AromaNoteForm()

    elif request.method == "POST":
        # save the note
        form = AromaNoteForm(request.POST)
        if form.is_valid():
            note = _note_save(request, form)
            #post_save.send(sender=AromaNote, instance=note)
            return HttpResponseRedirect(
                reverse('note_detail', args=[request.user.id, note.id])
                )
        else:
            form = AromaNoteForm(request.POST)
            errors = form.errors

    variables = RequestContext(request, {
        'form' : form,
        'errors' : errors,
    })
    return render_to_response('note/note_create.html', variables)

def _note_save(request, form):
    note = AromaNote.objects.create(
        content = form.cleaned_data['content'],
        title = form.cleaned_data['title'],
        author = request.user,
        created = datetime.now(),
        updated = datetime.now(),
        )
    note.save()
    return note

@require_http_methods(["GET", "POST"])
def note_detail(request, user_id, note_id):
    # display a note and process edit request

    if request.method == "GET":
        if request.user.id == int(user_id) and request.GET.get('action','') == 'edit':
            # get edit board with note content

            note = get_object_or_404(AromaNote, pk=note_id)
            form = AromaNoteForm(instance=note)
            variables = RequestContext(request, {
                'form' : form,
                'user_id' : user_id,
                'note_id' : note_id,
            })
            return render_to_response('note/note_edit.html', variables)
        else:
            user = get_object_or_404(AromaUser, pk=user_id)
            note = get_object_or_404(AromaNote, pk=note_id)
            variables = RequestContext(request, {
                'note' : note,
                'repo_user' : user,

            })
            # show the note
            return render_to_response('note/note_detail.html', variables)

    elif request.method == "POST":
        # save the editted note
        form = AromaNoteForm(request.POST)
        if form.is_valid():
            note = get_object_or_404(AromaNote, pk=note_id)
            note.title = form.cleaned_data['title']
            note.content = form.cleaned_data['content']
            note.save()
            return HttpResponseRedirect(reverse('note_detail', args=[user_id, note.id]))
        return HttpResponseRedirect(
            reverse('note_main')
            )

