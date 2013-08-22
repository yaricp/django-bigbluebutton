#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bbb.views import (error, home_page, create_meeting, meetings,
                        join_meeting, end_meeting, del_meeting,
                        del_record, meeting, start_meeting, 
                        edit_meeting, edit_record, public_meetings,
                        admin_meetings, logout)


urlpatterns = patterns('',
    url('^$', home_page, name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
            'template_name': 'login.html',
        }, name='login'),
    url(r'^logoff/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logoff'),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url('^error/$', error, name='error'),
    url('^logout/$', logout, name='logout'),
    url('^create/$', create_meeting, name='create'),
    url('^meetings/$', meetings, name='meetings'),
    url('^admin/$', admin_meetings, name='admin_meetings'),
    url('^pub_meetings/$', public_meetings, name='pub_meetings'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/join$', join_meeting,
        name='join'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/(?P<password>.*)/end$', end_meeting,
        name='end'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/del_conf$', del_meeting,
        name='del_conf'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/start$', start_meeting,
        name='start_conf'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/edit$', edit_meeting,
        name='edit_conf'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/$', meeting,
        name='conf'),
    url('^meeting/(?P<record_id>[a-zA-Z0-9 _-]+)/del_record$', del_record,
        name='del_rec'),
    url('^meeting/(?P<meeting_id>[a-zA-Z0-9 _-]+)/(?P<record_id>[a-zA-Z0-9 _-]+)/(?P<publish>.*)/edit_record$', edit_record,
        name='edit_rec'),
    url('^help.html$', 'django.views.generic.simple.redirect_to', {
            'url': 'http://www.bigbluebutton.org/content/videos' ,
        }, name='help'),
)
urlpatterns += staticfiles_urlpatterns()
