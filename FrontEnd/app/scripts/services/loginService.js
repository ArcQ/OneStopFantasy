var appServices = angular.module('frontEndApp');
appServices.factory('AuthenticationService', function() {
    var auth = {
        isLogged: false
    }
 
    return auth;
});
appServices.factory('UserService', function($http) {
    return {
        logIn: function(username, password) {

            return $http.post('http://www.onestopfantasyassistant.com:8000/auth/v1/user/login/',JSON.stringify({ username: username, password: password }));
        },
 
        logOut: function() {
             return $http.post('http://www.onestopfantasyassistant.com:8000/auth/v1/user/logout/',JSON.stringify({ username: username, password: password }));

        }
    }
});
appServices.factory('TokenInterceptor', function ($q, $window, $location, AuthenticationService) {
    return {
        request: function (config) {
            console.log($window.localStorage.osfaToken)
            config.headers = config.headers || {};
            if ($window.localStorage.osfaToken) {
                config.headers.Authorization = $window.localStorage.osfaToken;
            }
            return config;
        },
 
        requestError: function(rejection) {
            return $q.reject(rejection);
        },
 
        /* Set Authentication.isAuthenticated to true if 200 received */
        response: function (response) {
            if (response != null && response.status == 200 && $window.localStorage.osfaToken && !AuthenticationService.isAuthenticated) {
                AuthenticationService.isAuthenticated = true;
            }
            return response || $q.when(response);
        },
 
        /* Revoke client authentication if 401 is received */
        responseError: function(rejection) {
            if (rejection != null && rejection.status === 401 && ($window.localStorage.osfaToken || AuthenticationService.isAuthenticated)) {
                delete $window.localStorage.osfaToken;
                AuthenticationService.isAuthenticated = false;
                $location.path("/");
            }
 
            return $q.reject(rejection);
        }
    };
});