#-*- coding: utf-8 -*-
from time import  strftime, localtime

from django.utils.translation import ugettext_lazy as _

from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required 
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages

from bbb.models import Meeting
import settings

from bbb.forms import CreateForm, JoinForm

def home_page(request):
    context = RequestContext(request, {'settings':settings,
    })
    return render_to_response('home.html', context)


def error(request, text=None):
    if not text:
        text = _(u'Unknown error!')
    context = RequestContext(request, {
        'mess': text,
        })
    return render_to_response('bbb_error.html', context)
    
@login_required
def start_meeting(request,  meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if request.user==meeting.owner:
        result = meeting.create_and_get_url()
        if result=='error':
                return error(request, text=_(u'sorry! server BBB unavailable now'))
        return HttpResponseRedirect(meeting.join_url(request.user.username, meeting.moderator_password, start=1))
    else:
        return error(request, text=_(u'sorry!You can`t start this conference')) 
    
def logout(request):
    return HttpResponseRedirect(reverse('pub_meetings'))
    
    
@login_required
def meeting(request, meeting_id):
    meeting=Meeting.objects.get(id=meeting_id)
    recordings=meeting.get_records()
    mess=''
    if recordings=='error':
        recordings = None
        mess = _(u'Server BBB unavailable now')
    from forms import EditForm
    form_class = EditForm

    if request.method == "POST":
        # Get post data from form
        form = form_class(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('meetings'))
    else:
        form = form_class(instance=meeting)
    context = RequestContext(request, {
        'meeting': meeting,
        'recordings':recordings, 
        'form': form,
        'mess':mess, 
    })

    return render_to_response('meeting.html', context)

@login_required
def meetings(request):

    my_meetings = Meeting.get_meetings(request.user)
    context = RequestContext(request, {
        'my_meetings': my_meetings,
        
    })

    return render_to_response('meetings.html', context)
    
@login_required
def admin_meetings(request):
    if request.user.is_superuser:
        meetings = Meeting.get_meetings(request.user, admin=1)
        context = RequestContext(request, {
            'meetings': meetings,
            })
        return render_to_response('admin_meetings.html', context)
    else:
        return error(request, text=_(u'sorry!You can`t show this page'))

def public_meetings(request):
    meetings = Meeting.get_meetings()
    context = RequestContext(request, {
        'meetings': meetings,
        
    })

    return render_to_response('sharing_meetings.html', context)


@login_required
def edit_meeting(request, meeting_id):
    form_class = Meeting.EditForm
    meeting=Meeting.objects.get(id=meeting_id)
    if meeting.owner!=request.user:
        return error(request, text=_(u'sorry!You can`t edit this conference'))
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('meetings'))
    else:
        form = form_class()
    context = RequestContext(request, {
        'form': form,
        'meeting_id': meeting_id, 
    })

    return render_to_response('edit.html', context)
        

def join_meeting(request, meeting_id):
    form_class = JoinForm
    meeting=Meeting.objects.get(id=meeting_id)
    ip = request.META['REMOTE_ADDR']
    access=None
    if request.method == "POST":
        if request.user==meeting.owner:
            url=meeting.join_url(request.user.username, meeting.moderator_password)
            if url=='error':
                return error(request, text=_(u'Server BBB unavailable now'))
            elif url=='not running':
                return error(request, text=_(u'This conference is not running now. Please ask to creator of this conference to start it'))
        else:
            # Get post data from form
            form = form_class(request.POST)
            # Проверка открытости конференции извне
            if not meeting.openout:
                in_lans=[]
                for lan in settings.INDOOR_LANS:
                    in_lans.append(lan.split('/')[0])
                lan_ip=''
                for i in ip.split('.')[0:3]:
                    lan_ip+=i+'.'
                lan_ip+='0'
                if lan_ip in in_lans: 
                    access=True
            else:
                print 'access'
                access=True
            if access:
                if form.is_valid():
                    data = form.cleaned_data
                    name = data.get('name')
                    password = data.get('password')
                    url=meeting.join_url(name, password)
                    if url=='error':
                        return error(request, text=_(u'Server BBB unavailable now'))
                    elif url=='not running':
                        return error(request, text=_(u'This conference is not running now. Please ask to creator of this conference to start it'))
            else:
                return error(request, text=_(u'Sorry! This conference is available only into the net of ')+ settings.FACILITY)
        return HttpResponseRedirect(url)
    else:
        form = form_class()
 
    context = RequestContext(request, {
        'form': form,
        'meeting': meeting,
    })
    return render_to_response('join.html', context)

@login_required
def end_meeting(request, meeting_id, password):
    if request.method == "POST":
        meeting = Meeting.objects.get(id=meeting_id)
        result = meeting.end_meeting(password)
        if result=='error':
                return error(request, text=_(u'Server BBB unavailable now'))
        meeting.timestop = strftime("%Y-%m-%d %H:%M", localtime())
        meeting.save()
        msg = _(u'Conference') + str(meeting_id)+ _(' is ended.')
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('meetings'))
    else:
        msg = _(u'fail to stop conference ') + meeting_id
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('meetings'))

@login_required
def del_record(request, record_id):
    if request.user.is_superadmin:
        if request.method == "POST":
            result = Meeting.del_record(record_id)
            if result=='error':
                return error(request, text=_(u'Server BBB unavailable now'))
            msg = _(u'Record ')+str(record_id)+_(u' is deleted')
            messages.success(request, msg)
            #return HttpResponse(str(r))
            return HttpResponseRedirect(reverse('meetings'))
        else:
            msg = _(u'fail to delete record ')+str(record_id)
            messages.error(request, msg)
    else:
        return error(request, text=_(u'You can`t to delete record'))
        
        
@login_required
def edit_record(request, meeting_id, record_id, publish):
    if request.user.is_superuser:
        result=Meeting.change_public_record(record_id, publish)
        if result=='error':
            return error(request, text=_(u'Server BBB unavailable now'))

        return HttpResponseRedirect('/bbb/meeting/'+str(meeting_id))
    else:
        return error(request, text=_(u'You can`t to edit record'))

@login_required
def del_meeting(request, meeting_id):
    m=Meeting.objects.get(id=meeting_id)
    
    if request.user.is_superuser or m.owner==request.user:
        if request.method == "POST":
            msg = _('Conference ')+m.name.encode('utf-8')+_(' is deleted')
            messages.success(request, msg)
            m.delete()
            return HttpResponseRedirect(reverse('meetings'))
        else:
            msg = _('fail to delete conference ')+str(m.name)
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('meetings'))
    else:
        return error(request, text=_(u'You can`t to delete conference'))


@login_required
def create_meeting(request):
    form_class = CreateForm
    if request.method == "POST":
        # Get post data from form
        form = form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            meeting = Meeting()
            meeting.name = data.get('name')
            meeting.attendee_password = data.get('attendee_password')
            meeting.moderator_password = data.get('moderator_password')
            meeting.timestart = data.get('timestart')
            meeting.duration = data.get('duration')
            meeting.record = data.get('record')
            meeting.public = data.get('public')
            meeting.openout = data.get('openout')
            meeting.owner = request.user
            meeting.save()
            return HttpResponseRedirect(reverse('meetings'))

    else:
        form = form_class()
        
    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response('create.html', context)


            
