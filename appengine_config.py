import sys
import os


sys.path.append(os.path.join(os.getcwd(), "lib", "apiclient.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "cffi.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "Crypto.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "cryptography.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "django.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "httplib2.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "identitytoolkit.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "oauth2client.zip"))
# sys.path.append(os.path.join(os.getcwd(), "lib", "OpenSSL.zip"))
# sys.path.append(os.path.join(os.getcwd(), "lib", "pycrypto-2.6.1.zip"))
# sys.path.append(os.path.join(os.getcwd(), "lib", "pyOpenSSL-0.14.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "requests.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "simplejson.zip"))
sys.path.append(os.path.join(os.getcwd(), "lib", "six.zip"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'GAE_Django17.settings'