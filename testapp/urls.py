from django.conf.urls import patterns, url

urlpatterns = patterns('testapp.views',
    url(r'^$', 'list_greetings'),
    url(r'^sign/$', 'create_greeting'),
)