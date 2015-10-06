'use strict';

/**
 * @ngdoc overview
 * @name frontEndApp
 * @description
 * # frontEndApp
 *
 * Main module of the application.
 */
var app = angular
  .module('frontEndApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'googlechart',
    'uiSlider'
  ]);

app.config(['$routeProvider', '$locationProvider', '$httpProvider', function($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        access: { requiredLogin: false }
      })
      .when('/assistant', {
        templateUrl: 'views/assistant.html',
        controller: 'AssistantCtrl',
        access: { requiredLogin: true }
      })
      .when('/stats', {
        templateUrl: 'views/stats.html',
        controller: 'StatsCtrl',
        access: { requiredLogin: false }
      })
      .when('/createAccount', {
        templateUrl: 'views/createAccount.html',
        controller: 'CreateAccountCtrl',
        access: { requiredLogin: false }
      })
      .when('/sync', {
        templateUrl: 'views/sync.html',
        controller: 'SyncCtrl',
        access: { requiredLogin: false }
      })
      .when('/contact', {
        templateUrl: 'views/contactUs.html',
        access: { requiredLogin: false }
      })
      .otherwise({
        redirectTo: '/',
        access: { requiredLogin: false }
      });

      $locationProvider.html5Mode(true);
      $httpProvider.interceptors.push('TokenInterceptor');

  }]);


app.run(function($rootScope, $location, AuthenticationService) {
    $rootScope.$on("$routeChangeStart", function(event, nextRoute, currentRoute) {
        if (nextRoute.access.requiredLogin && !AuthenticationService.isLogged) {
            alert('You must log in to use this feature!')
            $location.path("/");
        }
    });
});
