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
from django.views.decorators.csrf import csrf_protect
from django.db.models import Max
from django.contrib.auth.decorators import login_required
import django
import json
import time
import requests


gitkit_instance = gitkitclient.GitkitClient.FromConfigFile('gitkit-server-config.json')

MEMCACHE_GREETINGS = 'greetings'


def genespotre(request):
    return render(request, 'testapp/genespot-re-demo.html', {})


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
    }

    return render(request, 'testapp/index.html', context_dict)


def widget(request):
    return render(request, 'testapp/widget.html', {})


def user_logout(request):
    # this just logs out of django, not google+
    # the javascript on the index.html page logs out of google+ when it sees the django user is logged out
    logout(request)
    return render(request, 'testapp/landing.html')


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


def landing_page(request):
   # among other things, the gtoken cookie contains
    # 1) the user's email, which is set here to the username for the django.auth User model
    # 2) a user_id that is specific to each google+ user for each client. Here it becomes the password for the user
    if 'gtoken' in request.COOKIES:
        gitkit_user = gitkit_instance.VerifyGitkitToken(request.COOKIES['gtoken'])
        if gitkit_user:
            user = authenticate(username=gitkit_user.email, password=gitkit_user.user_id)
            if user is None:
                # If this is the first time the google+ user logs in to the client application,
                # the google+ user information is used to make a new User entry in the django database.
                # In the future, here is where we could keep out unauthorized users
                first_name = None
                last_name = None
                gitkit_user_by_email = gitkit_instance.GetUserByEmail(gitkit_user.email)
                if gitkit_user_by_email:
                    first_name = gitkit_user_by_email.name.split(' ')[0]
                    last_name = gitkit_user_by_email.name.split(' ')[1]
                try:
                    User.objects.create_user(
                        # the primary key id is created manually here because django seems to try to use
                        # gitkit_user.user_id as the id field, which exceeds the maximum number of bytes
                        # allowed for mysql type int. The id's were then automatically set to the maximum
                        # number, 2147483647. An alternative solution would be to subclass User and make
                        # the id field type varchar instead of int
                        id=User.objects.all().aggregate(Max('id'))['id__max']+1,
                        username=gitkit_user.email,
                        email=gitkit_user.email,
                        password=gitkit_user.user_id,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user = authenticate(username=gitkit_user.email, password=gitkit_user.user_id)
                except IntegrityError, e:
                    # used to get integrity errors when user id's were automatically
                    # set to 2147483647
                    print 'error is ' + str(e)
                    return render(request, 'testapp/landing.html')
            login(request, user)
        else:
            # this shouldn't ever happen
            print 'this shouldnt ever happen'
            logout(request)
    else:
        logout(request)
    return render(request, 'testapp/landing.html',
        {'request': request})


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

@login_required
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

@csrf_protect
def search_results(request):

    if request.method == 'POST':
        url = 'https://tcga-data.nci.nih.gov/uuid/uuidBrowser.json?_dc=1418770411240&start=0&limit=10'
        req = Request(url)
        results = json.load(urlopen(req))
        queries = {}

        if 'elements_selected' in request.POST:
            queries['elements_selected'] = json.loads(request.POST['elements_selected'])
        if 'platforms_selected' in request.POST:
            queries['platforms_selected'] = json.loads(request.POST['platforms_selected'])
        if 'tumors_selected' in request.POST:
            queries['tumors_selected'] = json.loads(request.POST['tumors_selected'])

        return render(request,'testapp/search_results.html', {'request': request,
                                                           'data': results,
                                                           'queries': queries})

