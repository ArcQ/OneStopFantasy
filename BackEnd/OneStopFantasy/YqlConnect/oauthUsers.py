# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
import urlparse
import oauth2 as oauth
import httplib
import time
import urllib
import sys, os
import re

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'

import django
django.setup()
# your imports, e.g. Django models
from YqlConnect.models import UserExtended
from django.contrib.auth.models import User

consumer_key = 'dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--'
consumer_secret = '8a79e55ffaa18b24f74ddae0faddb4ba31c31d59'

request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
callback_url = 'http://onestopfantasyassistant.com/onestopfantasy/sync/'



class OauthUsers:

    def refreshAccessToken(self,username):
        from rauth import OAuth1Service
        from rauth.utils import parse_utf8_qsl
        import pickle
        try:
            userExtended = UserExtended.objects.get(user__username = username)

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
                                userExtended.access_Token,
                                userExtended.access_Token_Secret,
                                params={"oauth_session_handle":
                                        userExtended.oauth_session_handle})
            
            print access_Token_Tuple[0]

            userExtended = ''
            user = User.objects.get(username = username)
            if UserExtended.objects.filter(user=user).exists():
                userExtended = UserExtended.objects.get(user = user)
                userExtended.access_Token = access_Token_Tuple[0]
                userExtended.access_Token_Secret = access_Token_Tuple[1]
            else:
                userExtended = UserExtended(user = user,access_Token = access_Token_Tuple[0], access_Token_Secret = access_Token_Tuple[1], oauth_session_handle = userExtended.oauth_session_handle)
            
            userExtended.save()
            return ["RefreshAccessToken","Success"]
        except Exception as e:
            return ["error",str(e)]

        # if __name__ == '__main__':    

    def getRequestToken(self,username):
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_callback': callback_url,
            'oauth_signature_method':'PLAINTEXT',
        }
        try:
            # Step 1: Get a request token. This is a temporary token that is used for 
            # having the user authorize an access token and to sign the request to obtain 
            # said access token.
            consumer = oauth.Consumer(consumer_key, consumer_secret)
            client = oauth.Client(consumer)
            resp, content = client.request(request_token_url, method='GET',  parameters= params )
            if resp['status'] != '200':
                # raise Exception("Invalid response %s." % resp)
                return ['InvalidResponse',resp]

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

            userExtended = ''
            user = User.objects.get(username = username)
            if UserExtended.objects.filter(user=user).exists():
                userExtended = UserExtended.objects.get(user = user)
                userExtended.oauth_Token = request_token['oauth_token']
                userExtended.oauth_Token_Secret = request_token['oauth_token_secret']
            else:
                userExtended = UserExtended(user = user, oauth_Token = request_token['oauth_token'], oauth_Token_Secret = request_token['oauth_token_secret'])
            
            userExtended.save()
            response = ['RequestToken',authorize_url+"?oauth_token="+request_token['oauth_token']]
            return response
        except Exception as e:
            return ["error",str(e)]

    def getAccessToken(self,username,oauth_verifier):
        try:
            # After the user has granted access to you, the consumer, the provider will
            # redirect you to whatever URL you have told them to redirect to. You can 
            # usually define this in the oauth_callback argument as well.

            userExtended = UserExtended.objects.get(user__username = username)

            # Step 3: Once the consumer has redirected the user back to the oauth_callback
            # URL you can request the access token the user has approved. You use the 
            # request token to sign this request. After this is done you throw away the
            # request token and use the access token returned. You should store this 
            # access token somewhere safe, like a database, for future use.
            token = oauth.Token(userExtended.oauth_Token,
                userExtended.oauth_Token_Secret)
            token.set_verifier(oauth_verifier)
            consumer = oauth.Consumer(consumer_key, consumer_secret)
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
            print "- oauth_session_handle   = %s" % access_token['oauth_session_handle']
            print
            print "You may now access protected resources using the access tokens above." 
            print

            print
            print access_token

            userExtended = ''
            user = User.objects.get(username = username)
            if UserExtended.objects.filter(user=user).exists():
                userExtended = UserExtended.objects.get(user = user)
                userExtended.access_Token = access_token['oauth_token']
                userExtended.access_Token_Secret = access_token['oauth_token_secret']
                userExtended.oauth_session_handle = access_token['oauth_session_handle']

            else:
                userExtended = UserExtended(user = user,access_Token = access_token['oauth_token'], access_Token_Secret = access_token['oauth_token_secret'], oauth_session_handle = access_token['oauth_session_handle'])
            
            userExtended.save()

            response = ["getAccessToken","success"]
            return response
        except Exception as e:
            return ["error",str(e)]


    def requestOauth(self,username):
        isAccessTokenNull = False
        if UserExtended.objects.filter(user__username = username).exists():
            userExtended = UserExtended.objects.get(user__username = username)
            if not userExtended.access_Token:
                isAccessTokenNull = True
        else:
            user = User.objects.get(username = username)
            userExtended = UserExtended(user = user)
            isAccessTokenNull = True

        if(isAccessTokenNull == True):
            return self.getRequestToken(username)
        else:
            return self.refreshAccessToken(username)

oauthUsers =OauthUsers()
print oauthUsers.requestOauth('test19')
#print oauthUsers.getAccessToken('test1','hrr4ch')


