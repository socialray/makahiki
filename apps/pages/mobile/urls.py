from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'pages.mobile.views.index', name='mobile_index'),
)