from django.conf.urls import patterns, url

urlpatterns = patterns('testapp.views',
    url(r'^$', 'landing_page'),
    url(r'sign/$', 'create_greeting'),
    url(r'^bubble_animation', 'bubble_animation', name='bubble_animation'),
)