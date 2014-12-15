from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from testapp import views



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GAE_Django14.views.home', name='home'),
    # url(r'^GAE_Django14/', include('GAE_Django14.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'testapp.views.landing_page'),
    url(r'^testapp/', include('testapp.urls')),

    url(r'^accounts/create_user/$', 'testapp.views.create_new_user'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'testapp/login.html',}),
    url(r'^accounts/profile/$', 'testapp.views.list_greetings'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/testapp/',}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^search/', views.search),
    url(r'^search_results/', views.search_results),
    url(r'^css_test/', views.css_test),

)
