from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^bbb/', include('bbb.urls')),
)
