from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#import python modules
import os

#import django modules
from django.conf.urls import *
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.core.urlresolvers import reverse

#import mint modules
#from Announce.views import announce_main
#from AromaUser.views import signin, signup, signout
#from AromaNote.views import note_main, note_create, note_repo, note_detail

#admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mint.views.home', name='home'),
    # url(r'^mint/', include('mint.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    #announce
    #url(r'^$', announce_main),

    #user auth
    #url(r'^auth/signin/$', signin),
    #url(r'^auth/signup/$', signup),
    #url(r'^auth/signout/$', signout),
    
    url(r'^admin/', include(admin.site.urls)),
    
)

urlpatterns += patterns('AromaAnnounce.views',
    url(r'^$', 'announce', name='announce'),
)

urlpatterns += patterns('AromaNote.views',
    url(r'^note/$', 'note_main', name='note_main'),
    url(r'^note/create/$', 'note_create', name='note_create'),
    url(r'^note/(?P<user_id>\d+)/$', 'note_repo', name='note_repo'),
    url(r'^note/(?P<user_id>\d+)/(?P<note_id>\d+)/$', 'note_detail', name='note_detail'),
)

urlpatterns += patterns('AromaUser.views',
    url(r'^auth/signin/$', 'signin', name='signin'),
    url(r'^auth/signup/$', 'signup', name='signup'),
    url(r'^auth/signout/$', 'signout', name='signout'),
)


