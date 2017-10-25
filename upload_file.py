# Get data from Tumblr API
from * import sample_oauth1_code.py
import requests_oauthlib
import webbrowser
import json

# Registered an app on "https://www.tumblr.com/oauth/apps"
client_key = "O1kHF4BtrMdtWuFi9CGPwGXiIlR4xFcR6kluaeskPII8eE3j1Q" # what Twitter calls Consumer Key
client_secret = "N9MAfKxrnE8gDDpuxopo7M0Jwf3EPobTD9dBgPMBNu6kiPonrE" # What Twitter calls Consumer Secret

if not client_secret or not client_key:
    print("You need to fill in client_key and client_secret. See comments in the code around line 8-14")
    exit()

def get_tokens():
    ## Step 1. Obtain a request token which will identify you (the client) in the next step.
    # At this stage you will only need your client key and secret

    # OAuth1Session is a class defined in the requests_oauthlib module
    # Two values are passed to the __init__ method of OAuth1Session
    # -- the key is passed as the value of the first parameter (whose name we don't know)
    # -- the secret is passed as the value of the parameter that is also called client_secret
    # after this line executes, oauth will now be an instance of the class OAuth1Session
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://www.tumblr.com/oauth/request_token'

    # invoke the fetch_request_token method of the class OAuth1Session on our instance
    # it returns a dictionary that might look like this:
    # {
    #     "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #     "oauth_token_secret": "Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM"
    # }
    # It also saves the oauth_token as an instance variable of the object
    # oauth is bound to, so it can be used in later steps
    fetch_response = oauth.fetch_request_token(request_token_url)

    # pull the two values out of the dictionary and store them in a variable for later use
    # note that d.get('somekey') is another way of writing d['somekey']
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    ## Step 2. Obtain authorization from the user (resource owner) to access their protected resources (images, tweets, etc.). This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter. Note that not all services will give you a verifier even if they should. Also the oauth_token given here will be the same as the one in the previous step.

    base_authorization_url = 'https://www.tumblr.com/oauth/authorize'
    # append the query parameters need to make it a full url.
    # they will include the resource_owner_key from the previus step,
    # which was stored in the oauth object above as an instance variable
    # when fetch_request_token was invoked
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url) # opens a window in your web browser
    # Once you log in, and give permissions, you should see a string of characters that you need to copy.

    # After the user authenticates at Twitter, it would normally "redirect"
    # the browser back to our website. But we aren't running a website.
    # Some services, like Twitter, will let you configure the app to
    # display a verifier, or the entire redirect url, rather than actually
    # redirecting to it.
    # User will have to cut and paste the verifier or the whole redirect url

    # version where the website provides a verifier
    verifier = raw_input('Please input the verifier>>> ')

    # version where the website provides the entire redirect url
    # redirect_response = raw_input('Paste the full redirect URL here: ')
    # oauth_response = oauth.parse_authorization_response(redirect_response)
    # get back something like this
    #{
    #    "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #    "oauth_verifier": "sdflk3450FASDLJasd2349dfs"
    #}
    # verifier = oauth_response.get('oauth_verifier')

    ## Step 3. Obtain an access token from the OAuth provider. Save this token so it can be re-used later.
    # In this step we re-use most of the credentials obtained up to this point.

    # make a new instance of the OAuth1Session class, with several more parameters filled in
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)

    access_token_url = 'https://www.tumblr.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    # You get back something like this
    #{
    #    "oauth_token": "6253282-eWudHldSbIaelX7swmsiHImEL4KinwaGloHANdrY",
    #    "oauth_token_secret": "2EEfA6BG3ly3sR3RjE0IBSnlQu4ZrUzPiYKmrkVU"
    #}
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

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
