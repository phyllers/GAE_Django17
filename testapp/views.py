# Create your views here.
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from testapp.forms import CreateGreetingForm
from testapp.models import Greeting
from django.shortcuts import render
from django.shortcuts import redirect
from urllib2 import Request, urlopen, URLError
from django.db import IntegrityError
from identitytoolkit import gitkitclient
import django
import json
import time
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
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile('gitkit-server-config.json')

MEMCACHE_GREETINGS = 'greetings'


def list_greetings(request):

    try:
        url = 'https://striking-berm-771.appspot.com/_ah/api/gae_endpoints/v1/hellogreeting/'
        req3 = Request(url)
        api_greetings = json.load(urlopen(req3))
    except URLError, e:
        api_greetings = 'No Response', e

    greetings = cache.get(MEMCACHE_GREETINGS)
    if greetings is None:
        greetings = Greeting.objects.all().order_by('-date')[:10]
        cache.add(MEMCACHE_GREETINGS, greetings)

    context_dict = {
        'request': request,
        'greetings': greetings,
        'form': CreateGreetingForm(),
        'djversion': django.get_version(),
        'api_greetings': api_greetings,
        'userinfo': ''
    }

    if 'gtoken' in request.COOKIES:
        gitkit_user = gitkit_instance.VerifyGitkitToken(request.COOKIES['gtoken'])
        if gitkit_user:
            gitkit_user_by_email = gitkit_instance.GetUserByEmail(gitkit_user.email)
            user = authenticate(username=gitkit_user.email, password=gitkit_user.user_id)
            if user is None:
                first_name = None
                last_name = None
                if gitkit_user_by_email.name:
                    print 'gitkit_user_by_email.name: ' + gitkit_user_by_email.name
                    first_name = gitkit_user_by_email.name.split(' ')[0]
                    last_name = gitkit_user_by_email.name.split(' ')[1]
                    # print 'first name is ' + first_name
                    # print 'last name is ' + last_name
                if gitkit_user_by_email.photo_url:
                    # print "gitkit_user_by_email.photo_url: " + gitkit_user_by_email.photo_url
                    pass

                try:
                    user = User.objects.create_user(
                        username=gitkit_user.email,
                        email=gitkit_user.email,
                        password=gitkit_user.user_id,
                        first_name=first_name,
                        last_name=last_name
                        )
                    login(request, user)
                except IntegrityError, e:
                    print 'error is ' + str(e)
            else:
                login(request, user)
            context_dict['userinfo'] = str(vars(gitkit_user))

    return render(request, 'testapp/index.html', context_dict)


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

def css_test(request):
    return render(request, 'testapp/css_test.html', {'request': request})

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

    elements = [{'id': 1, 'label': 'Participant'},
                {'id': 2, 'label': 'Sample'},
                {'id': 3, 'label': 'Portion'},
                {'id': 4, 'label': 'Analyte'},
                {'id': 5, 'label': 'Slide'},
                {'id': 6, 'label': 'Aliquot'},
                {'id': 7, 'label': '(Radiation)'},
                {'id': 8, 'label': '(Drug)'},
                {'id': 9, 'label': '(Examination)'},
                {'id': 10, 'label': '(Surgery)'},
                {'id': 11, 'label': 'Shipped Portion'}]

    platforms = [{'id': 1, 'label': 'ABI'},
                 {'id': 2, 'label': 'AgilentG4502A_07'},
                 {'id': 3, 'label': 'CGH-1x1M_G4447A'},
                 {'id': 4, 'label': 'Genome_Wide_SNP_6'},
                 {'id': 5, 'label': 'H-miRNA_8x15k'},
                 {'id': 6, 'label': 'HG-CGH-244A'},
                 {'id': 7, 'label': 'HG-U133_Plus_2'},
                 {'id': 8, 'label': 'HT_HG_U133A'},
                 {'id': 9, 'label': 'Human1MDuo'},
                 {'id': 10, 'label': 'HumanMethylation27'},
                 {'id': 11, 'label': 'IlluminaDNAMethylation_OMA002_CPI'}]


    return render(request, 'testapp/search.html', {'request': request,
                                                   'tumor_types': tumor_types,
                                                   'elements': elements,
                                                   'platforms': platforms})

def search_results(request):
    fake_data = []
    for i in range(1, 10):
        fake_data.append({'name':'Some Title %i' % i,
                          'source':'Kitty ipsum',
                          'visibility': 'Public',
                          'updated': time.strftime('%m/%d/%Y')})
    return render(request, 'testapp/search_results.html', {'request': request,
                                                           'data': fake_data,})


def widget(request):
    return render(request, 'testapp/widget.html', {})


def logout(request):
    # if 'gtoken' in request.COOKIES:
    #     request.COOKIES['gtoken'] = None
    logout(request)
    return render(request, 'testapp/index.html')

