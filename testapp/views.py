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


MEMCACHE_GREETINGS = 'greetings'

def list_greetings(request):
    # req = Request('http://api.striking-berm-771.appspot.com/')
    # req2 = Request('http://api.striking-berm-771.appspot.com/1')
    # try:
    #     # response = urlopen(req)
    #     # api_result = response.read()
    #     response2 = urlopen(req2)
    #     api_result2 = json.load(response2)
    #
    # except URLError, e:
    #     api_result = 'No response: ', e
    #     api_result2 = 'No response: ', e
    #
    req3 = Request('https://striking-berm-771.appspot.com/_ah/api/gae_endpoints/v1/hellogreeting')
    try:
        res = urlopen(req3)
        api_greetings = json.load(res)
    except URLError, e:
        api_greetings = 'No Response', e

    greetings = cache.get(MEMCACHE_GREETINGS)
    if greetings is None:
        greetings = Greeting.objects.all().order_by('-date')[:10]
        cache.add(MEMCACHE_GREETINGS, greetings)
    return render(request, 'testapp/index.html',
                              {'greetings': greetings,
                               'form': CreateGreetingForm(),
                               'djversion': django.get_version(),
                               # 'api_result': api_result,
                               # 'api_result2': api_result2,
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
