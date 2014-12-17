from django.conf.urls import patterns, url

urlpatterns = patterns('testapp.views',
    url(r'^$', 'landing_page'),
    url(r'^sign/$', 'create_greeting'),
)