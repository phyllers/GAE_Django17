# Create your views here.
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from testapp.forms import CreateGreetingForm
from testapp.models import Greeting
from django.shortcuts import render
from django.shortcuts import redirect
from urllib2 import Request, urlopen, URLError
import django
import json
import requests

# from requests_oauthlib import OAuth1

# !!! Commented out API authorization code until I can get it to work with Endpoints !!!
# from apiclient import discovery
# import httplib2
# import oauth2client
# from oauth2client import tools
# import argparse

# CLIENT_ID = '1042486265945-969e0e0blptg1l9suhj7ppn5qjal8idb.apps.googleusercontent.com'
# CLIENT_SECRET = 'gGcU6r-00xB23my8MUzvzn5C'
# SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
# USER_AGENT = 'my-app'
# OAUTH_DISPLAY_NAME = 'HAPPY APPY'
#
# API_ROOT = 'https://striking-berm-771.appspot.com/_ah/api'
# API = 'gae_endpoints'
# VERSION = 'v1'


MEMCACHE_GREETINGS = 'greetings'

def list_greetings(request):

    # storage = oauth2client.file.Storage('guestbook.dat')
    # credentials = storage.get()
    # parser = argparse.ArgumentParser(
    #     description='Auth sample',
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     parents=[tools.argparser])
    # flags = parser.parse_args('')
    #
    # if credentials is None or credentials.invalid:
    #     flow = oauth2client.client.OAuth2WebServerFlow(
    #         client_id=CLIENT_ID,
    #         client_secret=CLIENT_SECRET,
    #         scope=SCOPE,
    #         user_agent=USER_AGENT,
    #         xoauth_displayname=OAUTH_DISPLAY_NAME
    #     )
    #     credentials = tools.run_flow(flow, storage, flags)
    # http = httplib2.Http()
    # http = credentials.authorize(http)
    # discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (API_ROOT, API, VERSION)
    try:
        # service = discovery.build(API, VERSION, discoveryServiceUrl=discovery_url, http=http)
        # response = service.greetings()
        # api_greetings = service

        url = 'https://striking-berm-771.appspot.com/_ah/api/gae_endpoints/v1/hellogreeting/1'
        # auth = OAuth1(CLIENT_ID, CLIENT_SECRET)
        req3 = Request(url)
        api_greetings = json.load(urlopen(req3))
    except URLError, e:
        api_greetings = 'No Response', e

    greetings = cache.get(MEMCACHE_GREETINGS)
    if greetings is None:
        greetings = Greeting.objects.all().order_by('-date')[:10]
        cache.add(MEMCACHE_GREETINGS, greetings)
    return render(request, 'testapp/index.html',
                              {'request': request,
                               'greetings': greetings,
                               'form': CreateGreetingForm(),
                               'djversion': django.get_version(),
                               'api_greetings': api_greetings,
                               })

def create_greeting(request):
    if request.method == 'POST':
        form = CreateGreetingForm(request.POST)
        if form.is_valid():
            greeting = form.save(commit=False)
            if request.user.is_authenticated():
                greeting.author = request.user
            greeting.save()
            cache.delete(MEMCACHE_GREETINGS)
    return redirect('/testapp/')

def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.save()
            return redirect('/testapp/')
    else:
        form = UserCreationForm()
    return render(request, 'testapp/user_create_form.html',
        {'form': form})

def search(request):
    tumor_types = [{'id': 'BLCA', 'label': 'Bladder Urothelial Carcinoma'},
                   {'id': 'BRCA', 'label': 'Breast Invasive Carcinoma'},
                   {'id': 'COAD', 'label': 'Colon Adenocarcinoma'},
                   {'id': 'GBM', 'label': 'Glioblastoma Multiforme'},
                   {'id': 'HNSC', 'label': 'Head and Neck Squamous Cell Carcinoma'},
                   {'id': 'KIRC', 'label': 'Kidney Renal Clear Cell Carcinoma'},
                   {'id': 'LUAD', 'label': 'Lung Adenocarcinoma'},
                   {'id': 'LUSC', 'label': 'Lung Squamous Cell Carcinoma'},
                   {'id': 'OV', 'label': 'Ovarian Serous Cystadenocarcinoma'},
                   {'id': 'READ', 'label': 'Rectum Adenocarcinoma'},
                   {'id': 'UCEC', 'label': 'Uterine Corpus Endometrial Carcinoma'}]

    return render(request, 'testapp/search.html', {'request': request,
                                                   'tumor_types': tumor_types})

def search_results(request):
    fake_data = []
    for i in range(1, 10):
        fake_data.append({'name':'Some Title %i' % i,
                          'info':'Kitty ipsum dolor sit amet, catnip sleep in the sink toss the mousie judging you, sleep on your keyboard judging you hiss hiss sunbathe lick. Fluffy fur zzz lay down in your way sniff claw, catnip knock over the lamp stretching litter box biting.'})
    return render(request, 'testapp/search_results.html', {'request': request,
                                                           'data': fake_data,})

