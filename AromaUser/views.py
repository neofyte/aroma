from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import get_user_model

from AromaUser.forms import AuthForm

User = get_user_model()

def signin(request):
    errors = []
    form =AuthForm()
    if request.method == 'POST':
        form = AuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth_authenticate(username=username, password=password)
        if user is not None:
            if  user.is_active:
                auth_login(request, user)
                return  HttpResponseRedirect('/')
            else:
                errors.append('disabled account')
        else:
            errors.append('invalid login')
    variables = RequestContext(request, {
            'signInForm' : form,
            'errors' : errors,
            })
    return render_to_response('auth/signin.html',variables) 

def signup(request):
    errors=[]
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            auth_login(request, user)
            return  HttpResponseRedirect('/')
        else:
            errors = form.errors
    variables = RequestContext(request, {
        'signUpForm' : form,
        'errors' : errors,
        })
    return render_to_response('auth/signup.html', variables)

def signout(request):
    logout(request)
    return HttpResponseRedirect('note/')