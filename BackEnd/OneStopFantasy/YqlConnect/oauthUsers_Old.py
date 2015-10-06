# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
import urlparse
import oauth2 as oauth
import httplib
import time
import urllib

consumer_key = 'dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--'
consumer_secret = '8a79e55ffaa18b24f74ddae0faddb4ba31c31d59'

request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
callback_url = 'http://onestopfantasyassistant.com/'

params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
    'oauth_callback': callback_url,
    'oauth_signature_method':'PLAINTEXT',
}

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
isAccessTokenNull = True

if(isAccessTokenNull):
    # Step 1: Get a request token. This is a temporary token that is used for 
    # having the user authorize an access token and to sign the request to obtain 
    # said access token.

    resp, content = client.request(request_token_url, method='GET',  parameters= params )
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp)

    request_token = dict(urlparse.parse_qsl(content))

    print "Request Token:"
    print "    - oauth_token        = %s" % request_token['oauth_token']
    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
    print 

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    print 

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')


    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the 
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this 
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'oauth_signature_method':'HMAC-SHA1',
    }

    resp, content = client.request(access_token_url, method="GET", parameters=params)
    access_token = dict(urlparse.parse_qsl(content))




    print "Access Token:"
    print "- oauth_token = %s" % access_token['oauth_token']
    print
    print "- oauth_token_secret   = %s" % access_token['oauth_token_secret']
    print
    print "- xoauth_yahoo_guid   = %s" % access_token['xoauth_yahoo_guid']
    print
    print "You may now access protected resources using the access tokens above." 
    print

    print
    print access_token
else:
    from rauth import OAuth1Service
    from rauth.utils import parse_utf8_qsl
    import pickle

    oauth = OAuth1Service(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            name = "yahoo",
            request_token_url = "https://api.login.yahoo.com/oauth/v2/get_request_token",
            access_token_url = "https://api.login.yahoo.com/oauth/v2/get_token",
            authorize_url = "https://api.login.yahoo.com/oauth/v2/request_auth",
            base_url = "http://fantasysports.yahooapis.com/")

    access_token_time = time.time()
# (access_token, access_token_secret)
    access_Token_Tuple = oauth.get_access_token(
                        "A=Er6SSkXkgiEm5H0jl77HUMX4mdd_P8.IYd6W1pU1VVYj7OWYb7eZZG9Wm6xGi05NR6ZMPoKMvv3L0tJR.vYUi_tDDjOcAA3EvVt71YZ_eVl0ZmesrQXj7qyZE_v7MtRDB2aJgUSsRKAe5UBvP1_6Fg9Vy6hiZ3c48h_LtBtYh6ZEI8Jl0PklQHQ_aRpEUZVr.HRZqZ3CM_ROY.J2KnDQAWK4XevRoHE4FXYQ6twEVpNWAdCodpFRmtbaHFzOH2aa4pcRuSLzD9Rth4uTy.TQbRs.H9AHusH9YBnCtJuiDt8wxpVEvtlUN8hiz32qkaNxUEgdoj8JtcgaN27ARaXP7HUgokZSgOC7HM4Tffe_45_2ivSOK60RaQksfQ4.jhbMjX32wdlV1uf8N7YhK5.UQ2DKSh0rZcH1t1Wcxwaa0wNo0Nja3hc.GX01IRvqLxtijrIKnvUINugDmTJel6EZJPheJy6c4BQ8fWc1VgGqRVumI8dOQArad3jqK30w3P0IB65PXmKMh4G0elDBKpmBFSfc1EBc64hwr_Wmsfm8494eQQX3yJvA49OWMQ5rU_IPkht49mp_KFV3bCykiY4JW8Bd..DJtJ2LWXcvt7f1iX8vnZflpNIvZQQf8w9ib8X7fl4tbuYWpcSWjBrdorE3fG5pPYVOfO.qM.xNI4KF9XErBMRnKvziPXPCmqizh9CQ2aQm5W1w4Uzprf14mIDSdkCknYYi58R.VUXDjcwx5G0P3gqGkKOFr5Rq90I0X4rmYDKu1yJTNqhAm4QLn7tMLGq0mShx7lP1XfKQ_sWbvjRFgkAHKWECzafH2tiY1ME_czf7TZAG7bybIezbkkj7GEuBIM6dD2joSJxijsn5MkCtHeaLAxW2LR7D.7geNQE-",
                        "7450e5d750486dcb0187f63d7a87b1ae983091a4",
                        params={"oauth_session_handle":
                                "ALTFyFQIx0yhpg5zvoxhF1l6ED_7M4qBb.MWHTwGLRPzaALURfSAWhgekxOEBz7yFyb0qn.N"})
    
    print access_Token_Tuple[0]

    # hack
    username = 'eddiedev'
    password = 'password'

    import sys, os
    import re

    sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
    
    import django
    django.setup()
    # your imports, e.g. Django models
    from YqlConnect.models import UserExtended
    from django.contrib.auth.models import User

    # if __name__ == '__main__':    



    # Save Data into Database
    user = ''
    userExtended = ''
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username = username)
        if UserExtended.objects.filter(user=user).exists():
            userExtended = UserExtended.objects.get(user = user)
            userExtended.access_Token = access_Token_Tuple[0]
            userExtended.access_Token_Secret = access_Token_Tuple[1]
        else:
            userExtended = UserExtended(user = user,access_Token = access_Token_Tuple[0], access_Token_Secret = access_Token_Tuple[1], oauth_session_handle = 'ALTFyFQIx0yhpg5zvoxhF1l6ED_7M4qBb.MWHTwGLRPzaALURfSAWhgekxOEBz7yFyb0qn.N' )
    else:
        user = User(username = username, password = password)
        
    user.save()
    userExtended.save()
