# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms import ModelForm

from widgets import DateTimePickerWidget, TimePickerWidget

from models import Meeting



class EditForm(ModelForm):

    class Meta:
        model = Meeting
        fields = ['name','attendee_password', 'moderator_password', 'timestart', 'duration', 'record', 'public', 'openout']
        
        widgets = {
            'duration': TimePickerWidget(params="showOn: 'button', "\
                                                        "buttonImage: '/static/images/icon_clock.gif',"\
                                                        "buttonImageOnly: true", 
                                        attrs={'class': 'timepicker',}), 
            'timestart': DateTimePickerWidget(params='''dateFormat: 'yy-mm-dd', 
                                                        changeYear: true, 
                                                        showOn: 'button', 
                                                        buttonImage: '/static/images/icon_calendar.gif',
                                                        buttonImageOnly: true''' ,
                                                attrs={'class': 'datetimepicker',}), 
        }
    
        


class CreateForm(forms.Form):
#    class Meta:
#        model = Meeting
#        fields = ['name','attendee_password', 'moderator_password', 'timestart', 'duration', 'record', 'public', 'openout']
#    
        name = forms.CharField(label=_(u'name'))
        attendee_password = forms.CharField(label=_(u'password of user'),)
        moderator_password = forms.CharField(label=_(u'password of moderator'),)
        timestart = forms.DateTimeField(label=_(u'data time of start'), 
                                        widget=DateTimePickerWidget(params='''dateFormat: 'yy-mm-dd', 
                                                                            changeYear: true, 
                                                                            showOn: 'button', 
                                                                            buttonImage: '/static/images/icon_calendar.gif',
                                                                            buttonImageOnly: true''' ,
                                                                    attrs={'class': 'datetimepicker',}))
        duration = forms.TimeField( label=_(u'duration'),
                                    widget=TimePickerWidget(params="showOn: 'button', "\
                                                                    "buttonImage: '/static/images/icon_clock.gif',"\
                                                                    "buttonImageOnly: true", 
                                                            attrs={'class': 'timepicker',}))
        record = forms.BooleanField(label=_(u'make record'), widget=forms.CheckboxInput(), required=False,)
        public = forms.BooleanField(label=_(u'is public'), widget=forms.CheckboxInput(), required=False,)
        openout = forms.BooleanField(label=_(u'is open from out'), widget=forms.CheckboxInput(), required=False,)
 
        def clean(self):
            data = self.cleaned_data

            if Meeting.objects.filter(name = data.get('name')):
                raise forms.ValidationError(_(u'There is duplicate of conference!'))
            return data

class JoinForm(forms.Form):
    name = forms.CharField(label=_(u'login'))
    password = forms.CharField(label=_(u'password'),
                widget=forms.PasswordInput( render_value=False),
                required=False,)
    


        
        
