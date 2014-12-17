import sys
import os

sys.path.append(os.path.join(os.getcwd(), "django.zip"))
sys.path.append(os.path.join(os.getcwd(), "requests.zip"))
sys.path.append(os.path.join(os.getcwd(), "identitytoolkit.zip"))
sys.path.append(os.path.join(os.getcwd(), "oauth2client.zip"))
sys.path.append(os.path.join(os.getcwd(), "six.zip"))
sys.path.append(os.path.join(os.getcwd(), "OpenSSL.zip"))
sys.path.append(os.path.join(os.getcwd(), "cryptography.zip"))
sys.path.append(os.path.join(os.getcwd(), "cffi.zip"))
sys.path.append(os.path.join(os.getcwd(), "pycrypto-2.6.1.zip"))
sys.path.append(os.path.join(os.getcwd(), "pyOpenSSL-0.14.zip"))
sys.path.append(os.path.join(os.getcwd(), "simplejson.zip"))
sys.path.append(os.path.join(os.getcwd(), "Crypto.zip"))
sys.path.append(os.path.join(os.getcwd(), "apiclient.zip"))
sys.path.append(os.path.join(os.getcwd(), "httplib2.zip"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'GAE_Django17.settings'