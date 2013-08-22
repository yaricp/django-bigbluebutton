#-*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from urllib2 import urlopen
from urllib import urlencode
from hashlib import sha1
import xml.etree.ElementTree as ET
import random
from time import gmtime, strftime

import settings

def parse(response):
    try:
        xml = ET.XML(response)
        code = xml.find('returncode').text
        if code == 'SUCCESS':
            return xml
        else:
            raise
    except:
        return 'error'
        
def connect_bbb(url):
    try: result = urlopen(url).read()
    except: result = 'error'
    return result
        
class Record():
    id = ''
    type = ''
    url = ''
    published = ''
    starttime = ''
    endtime = ''

class Meeting(models.Model):

    name = models.CharField(verbose_name=_(u'name'), max_length=100, unique=True)
    attendee_password = models.CharField(verbose_name=_(u'password of user'), max_length=50)
    moderator_password = models.CharField(verbose_name=_(u'password of moderator'),max_length=50)
    duration = models.TimeField(verbose_name=_(u'duration'),
                                blank=True, 
                                null=True, 
                                )
    record = models.BooleanField(verbose_name=_(u'make record'),default=False)
    timestart = models.DateTimeField(verbose_name=_(u'data time of start'),
                                    default=strftime("%Y-%m-%d %H:%M", gmtime()), 
                                    )
    timestop = models.DateTimeField(verbose_name=_(u'date time of end'),null=True)
    public = models.BooleanField(verbose_name=_(u'is public'),default=True)
    openout = models.BooleanField(verbose_name=_(u'is open from out'),default=True)
    owner = models.ForeignKey(User)
    running = ''
    info = None
    
    @classmethod
    def api_call(self, query, call):
        prepared = "%s%s%s" % (call, query, settings.SALT)
        checksum = sha1(prepared).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result
    
    def is_running(self):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', 'meeting_'+str(self.id)),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(connect_bbb(url))
        print result
        if result=='error':
            return 'error'
        elif result!=2:
            return result.find('running').text
        else:
            return 'not running'

    def end_meeting(self,password):
        call = 'end'
        query = urlencode((
            ('meetingID', 'meeting_'+str(self.id)),
            ('password', password),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        print url
        result = parse(connect_bbb(url))
        if result:
            pass
        else:
            return 'error'

    @classmethod
    def meeting_info(self, id, password):
        call = 'getMeetingInfo'
        query = urlencode((
            ('meetingID', 'meeting_'+str(id)),
            ('password', password),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        print url
        r = parse(connect_bbb(url))
        if r:
            # Create dict of values for easy use in template
            d = {
                _(u'participant count'): r.find('participantCount').text,
                _(u'moderator count'): r.find('moderatorCount').text,
                _(u'password of user'): r.find('attendeePW').text,
                _(u'password of moderator'): r.find('moderatorPW').text,
            }
            return d
        else:
            return None
            
    @classmethod
    def url_meetings(self):
        call = 'getMeetings'
        query = urlencode((
            ('random', 'random'),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        return url
    
    @classmethod
    def del_record(self, recID):
        call = 'deleteRecordings'
        query = urlencode((
            ('recordID', str(recID)),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        print url
        r = parse(connect_bbb(url))
        return r

    @classmethod
    def get_meetings(self, user=None, admin=None):
        if user:
            if admin:
                meetings = Meeting.objects.all()
            else:
                meetings = Meeting.objects.filter(owner=user)
        else:
            meetings = Meeting.objects.filter(public=True)
        #list_id=['meeting_'+str(m.id) for m in archives]
        call = 'getMeetings'
        query = urlencode((
            ('random', 'random'),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(connect_bbb(url))
        d = []
        print str(dir(result[1]))
        for meeting in meetings:
            if result!='error' and result:
                list_meeting_bbb = result[1].findall('meeting')
                for m in list_meeting_bbb:
                    meetingID=m.find('meetingID').text
                    if 'meeting_'+str(meeting.id) == meetingID:
                        meeting.running = m.find('running').text
                        meeting.info = meeting.meeting_info(
                                                    meeting.id,
                                                    meeting.moderator_password)
            d.append(meeting)
        return d


    def create_and_get_url(self):
        call = 'create'
        voicebridge = 70000 + random.randint(0,9999)
        #if not self.meeting_id:
        mettingID='meeting_'+str(self.id)
        #else:
        #    mettingID=self.meeting_id
        query = urlencode((
            ('meetingID', mettingID),
            ('name', self.name.encode('utf-8')), 
            ('attendeePW', self.attendee_password),
            ('moderatorPW', self.moderator_password),
            ('voiceBridge', voicebridge),
            ('logoutURL ', settings.logoutURL), 
            ('duration', self.duration), 
            ('record', self.record), 
            ('welcome', _(u'Welcome!')),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        print '!'+url
        result = parse(connect_bbb(url))
        return result
    
    @classmethod
    def change_public_record(self, record_id, publish):
        call = 'publishRecordings'
        if publish=='true':
            publish='false'
        else:
            publish='true'
        query = urlencode((
            ('recordID', record_id),
            ('publish', publish ), 
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(connect_bbb(url))
        return result
    
    def get_records(self):
        call = 'getRecordings'
        query = urlencode((
            ('meetingID', 'meeting_'+str(self.id)),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + call + '?' + hashed
        result = parse(connect_bbb(url))
        records=[]
        if result=='error':
            return result
        if result:
            for r in result.find('recordings').findall('recording'):
                rec=Record()
                rec.id=r.find('recordID').text
                playbacks=r.findall('playback')
                rec.published = r.find('published').text
                rec.starttime = strftime('%d-%m-%Y %H:%M',gmtime(int(r.find('startTime').text)))
                rec.endtime = strftime('%d-%m-%Y %H:%M',gmtime(int(r.find('endTime').text)))
                for p in playbacks:
                    for f in p.findall('format'):
                        rec.type=f.find('type').text
                        rec.url=f.find('url').text
                        
                records.append(rec)
        return records

    def join_url(self, name, password, start=0):
        call = 'join'
        flag=0
        if start==0:
            if self.is_running()!='false':
                flag=1
            else:
                url='not running'
        else:
            flag=1
        if flag==1:
            query = urlencode((
                ('fullName', name),
                ('meetingID', 'meeting_'+str(self.id)),
                ('password', password),
            ))
            hashed = self.api_call(query, call)
            url = settings.BBB_API_URL + call + '?' + hashed
        return url
        
    def get_body_join_mail(self):
        out='subject=Приглашение на Видеоконференцию '+settings.FACILITY+'.'
        out+='&body=\n'\
                'Приглашаем Вас на видеоконференцию "'+self.name.encode('utf-8')+'", которая состоится '
        out+=str(self.timestart)+' и продлится '+str(self.duration).encode('utf-8')+'.\n'
        out+='Пароль для входа участника: '+ self.attendee_password.encode('utf-8')+' \n'
        out+='Для входа пройдите по ссылке "http://localhost:8000/bbb/meeting/'+str(self.id)+'/join"'
        return out


        def clean(self):
            data = self.cleaned_data

            if Meeting.objects.filter(name = data.get('name')):
                raise forms.ValidationError(_(u'There is duplicate of conference!'))
            return data

    
            
    
