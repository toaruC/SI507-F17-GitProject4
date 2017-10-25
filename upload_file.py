# Get data from Tumblr API
from sample_oauth1_code.py import *
import requests_oauthlib
import webbrowser
import json

# Registered an app on "https://www.tumblr.com/oauth/apps"
client_key = "O1kHF4BtrMdtWuFi9CGPwGXiIlR4xFcR6kluaeskPII8eE3j1Q" # what Twitter calls Consumer Key
client_secret = "N9MAfKxrnE8gDDpuxopo7M0Jwf3EPobTD9dBgPMBNu6kiPonrE" # What Twitter calls Consumer Secret


try:
    # This code tries to see if you can read the credentials from the file
    # (If you have credentials for the wrong user, or expired credentials
    # just delete the file creds.txt and run this code again)
    f = open("creds-tumblr.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    # If not, you'll have to get them!
    # and then, save them in a file called creds.txt
    tokens = get_tokens()
    f = open("creds-tumblr.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens
