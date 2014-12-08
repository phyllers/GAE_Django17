import sys
import os

sys.path.append(os.path.join(os.getcwd(), "django.zip"))
sys.path.append(os.path.join(os.getcwd(), "requests.zip"))
# sys.path.append(os.path.join(os.getcwd(), "requests_oauthlib.zip"))
# sys.path.append(os.path.join(os.getcwd(), "oauthlib.zip"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'GAE_Django17.settings'