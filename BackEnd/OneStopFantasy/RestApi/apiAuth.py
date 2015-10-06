from django.contrib.auth.models import User
from django.db import models
from tastypie.resources import ModelResource
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.models import create_api_key, ApiKey
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
from tastypie.authentication import ApiKeyAuthentication,BasicAuthentication,Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from YqlConnect.oauthUsers import OauthUsers
from YqlConnect.connectToYqlOauth import ConnectToYqlOauth

# models.signals.post_save.connect(create_api_key, sender=User)


class RequestToken(ModelResource):

    class Meta:
        resource_name = 'RequestToken'
        default_format = "application/json"
        authentication = ApiKeyAuthentication()

    def get_list(self, request, **kwargs):
        # Do any operation here and return in form of json in next line
        username = request.user.username;
        oauthUsers = OauthUsers()
        response = oauthUsers.requestOauth(username)

        if(response[0] == 'RefreshAccessToken'):
            c = ConnectToYqlOauth(username)
            userInformationRetrieval = c.getAllUserInformation();
            return self.create_response(request, {'responseType':response[0], 'value':response[1], 'userInformationRetrieval':userInformationRetrieval})
        else:
            return self.create_response(request, {'responseType':response[0], 'value':response[1]})

class AccessToken(ModelResource):

    class Meta:
        resource_name = 'AccessToken'
        default_format = "application/json"
        authentication = ApiKeyAuthentication()

    def get_list(self, request, **kwargs):
        # Do any operation here and return in form of json in next line
        username = request.user.username;
        oauth_verifier =  request.GET['oauth_verifier']
        oauthUsers = OauthUsers()
        response = oauthUsers.getAccessToken(username,oauth_verifier)
        c = ConnectToYqlOauth(username)
        userInformationRetrieval = c.getAllUserInformation();
        return self.create_response(request, {'responseType':response[0], 'accessTokenRetrieval':response[1], 'userInformationRetrieval':userInformationRetrieval})



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email','username']
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        filtering = {
            "username": ("exact")
        }
        always_return_data = True

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def obj_create(self, bundle, request=None, **kwargs):
        username, password, email = bundle.data['username'], bundle.data['password'], bundle.data['email']
        try:
            bundle.obj = user = User.objects.create_user(username,email,password)
            apiKey = ApiKey.objects.create(user=user)
            
            bundle.data['apiKey'] = apiKey.key
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle
        
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            apiKey = ApiKey.objects.get(user = user)
            apiKey = apiKey.key
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True, 'apiKey' : apiKey
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)
