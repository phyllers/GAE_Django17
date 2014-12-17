from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from testapp import views



admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'testapp.views.landing_page'),
    url(r'^testapp/', include('testapp.urls')),

    url(r'^accounts/profile/$', 'testapp.views.list_greetings'),
    url(r'^accounts/logout/$', 'testapp.views.user_logout'),
    url(r'^widget', 'testapp.views.widget', name='widget'),
    url(r'^genespot-re', views.genespotre),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', views.search),
    url(r'^search_results/', views.search_results),
    url(r'^css_test/', views.css_test),

)
