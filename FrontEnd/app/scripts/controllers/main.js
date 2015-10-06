'use strict';

/**
 * @ngdoc function
 * @name frontEndApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontEndApp
 */
angular.module('frontEndApp').controller('MainCtrl', ['$rootScope','$scope', '$location', '$window', 'UserService', 'AuthenticationService','$http', function AdminUserCtrl($rootScope, $scope, $location, $window, UserService, AuthenticationService,$http) {

	    $rootScope.isLogin = false;
	   	$rootScope.isLoading = false;
	    AuthenticationService.isLogged  = ($window.localStorage.osfaToken != undefined)? true:false;
	   	$rootScope.currentUsername = ($window.localStorage.osfaUsername != undefined)? $window.localStorage.osfaUsername:'';
	    $rootScope.isGuest = !AuthenticationService.isLogged;
	    $scope.getBeginPath = function(){
	    	return $rootScope.isGuest? 'createAccount': 'assistant';
	    }
		$scope.toggleLogin = function(){
			$rootScope.isLogin = !$rootScope.isLogin;
			console.log($rootScope.isLogin);
		}

	    $scope.logIn = function(username, password) {
            if (username !== undefined && password !== undefined) {
 
                UserService.logIn(username, password).success(function(data) {
                    AuthenticationService.isLogged = true;
                    console.log('data:');
                    console.log(data);
                    $window.localStorage.osfaUsername = username;
                    $window.localStorage.osfaToken = 'ApiKey ' +username + ':' + data.apiKey;
                    $rootScope.isGuest = false;
                    $rootScope.isLogin = false;
                   	$rootScope.currentUsername = ($window.localStorage.osfaUsername != undefined)? $window.localStorage.osfaUsername:'';
                    alert('Logged In!')
                    $location.path("/assistant");
                }).error(function(status, data) {
                	alert('error:'+stats)
                    console.log(status);
                    console.log(data);
                });
            }
        }
	    
	    $scope.cancelOverlay = function(){
	    	$rootScope.isLogin = false;
	    }

	    $scope.logout = function logout() {
	        if (AuthenticationService.isLogged) {
	            AuthenticationService.isLogged = false;
	            $rootScope.isGuest = true;
	            alert('Signed Out!')
	            delete $window.localStorage.osfaToken;
	            $location.path("/");
	        }
	    }

	    if(window.innerWidth <= 800 && window.innerHeight <= 600) {
	     $rootScope.isMobile == true;} 
		 else {
		     $rootScope.isMobile == false;
		  }
	    }
]);