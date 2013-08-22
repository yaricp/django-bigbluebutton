# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

import settings

main_css= {
            'all': ("/static/css/cupertino/jquery-ui-1.10.3.custom.css",)
        }
 
class DateTimePickerWidget(forms.DateInput):
    class Media:
        css = main_css
        js = (
            "/static/js/jquery-1.9.1.js",
            "/static/js/jquery-ui-1.10.3.custom.js",
            "/static/js/jquery-ui-timepicker-addon.js",
            "/static/js/jquery.ui.datepicker-"+settings.LANGUAGE_CODE.split('-')[0]+".js",
        )
 
    def __init__(self, params='', attrs=None, format=None):
        self.params = params
        super(DateTimePickerWidget, self).__init__(attrs=attrs, format=format)
 
    def render(self, name, value, attrs=None):
        rendered = super(DateTimePickerWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datetimepicker({%s});
            </script>'''%(name, self.params,))
            
            
class TimePickerWidget(forms.TimeInput):
    
    class Media:
        css = main_css
        js = (
            "/static/js/jquery-1.9.1.js",
            "/static/js/jquery-ui-1.10.3.custom.js",
            "/static/js/jquery-ui-timepicker-addon.js",
        )
    
    def __init__(self, params='', attrs=None, format=None):
        self.params = params
        super(TimePickerWidget, self).__init__(attrs=attrs, format=format)
        
    def render(self, name, value, attrs=None):
        rendered = super(TimePickerWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').timepicker({%s});
            </script>'''%(name, self.params,))
        
