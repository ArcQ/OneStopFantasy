'use strict';

/**
 * @ngdoc function
 * @name frontEndApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontEndApp
 */
angular.module('frontEndApp').controller('CreateAccountCtrl', ['$rootScope','$scope', '$location', '$window', 'UserService', 'AuthenticationService','$http',
    function ($rootScope,$scope, $location, $window, UserService, AuthenticationService,$http) {
 		$rootScope.isLogin = false;
 		$scope.isGuest = true;
        $scope.inputData = {};
        $scope.submitted = false;
        $scope.inputData.username, $scope.inputData.password, $scope.inputData.confirmPassword, $scope.inputData.email, $scope.inputData.confirmEmail = '';

        //boolean for username field, to reset after every change to the field
        $scope.isUsernameUnique = false;
        console.log($location.search());
        $scope.usernameChanged = function(){
            $scope.isUsernameUnique = false;
        }

        $scope.checkAvailability=function(){
            var query = 'user/?username='+$scope.inputData.username;
            var responsePromise = $http.get("http://www.onestopfantasyassistant.com:8000/auth/v1/"+query+"&format=json&limit=0");

            responsePromise.success(function(data, status, headers, config) {
                data = data.objects;
                if(data.length>0){
                    $scope.signUpForm.usernameField.$setValidity('uniqueName',false)
                }
                else{
                    $scope.signUpForm.usernameField.$setValidity('uniqueName',true)
                    $scope.isUsernameUnique = true;
                }
            });

            responsePromise.error(function(data, status, headers, config) {
                alert("AJAX failed!");
            });
        }

        $scope.checkSignUpFormValidated = function(){

            var query = 'user/?username='+$scope.inputData.username;

            $http.get("http://www.onestopfantasyassistant.com:8000/auth/v1/"+query+"&format=json&limit=0").success(function(data, status, headers, config) {
                data = data.objects;
                console.log(data);
                if(data.length>0){
                    $scope.signUpForm.usernameField.$setValidity('uniqueName',false)
                }
                else{
                    $scope.signUpForm.usernameField.$setValidity('uniqueName',true)
                    $scope.isUsernameUnique = true;
                    if(($scope.signUpForm.usernameField.$valid) && 
                    ($scope.signUpForm.passwordField.$valid) && 
                    ($scope.signUpForm.confirmPasswordField.$valid) && 
                    ($scope.signUpForm.emailField.$valid) && 
                    ($scope.signUpForm.emailConfirmField.$valid)){
                        submitNewUser();
                    }
                    else{
                        alert('You have errors in your form!');
                    }
                }
            }).error(function(data, status, headers, config) {
                alert("AJAX failed!");
            });

        }

        function submitNewUser(){
            $rootScope.isLoading = true;

            console.log('hey');
            $http.post('http://www.onestopfantasyassistant.com:8000/auth/v1/user/',
                JSON.stringify({ username: $scope.inputData.username, password: $scope.inputData.password, email: $scope.inputData.email }))
            .success(function(data) {
                AuthenticationService.isLogged = true;
                console.log(data);
                $window.localStorage.osfaUsername = $scope.inputData.username;
                $window.localStorage.osfaToken = 'ApiKey ' +$scope.inputData.username + ':' + data.apiKey;
                $rootScope.isLogin = false;
                $rootScope.currentUsername = $scope.inputData.username;
                $rootScope.isGuest = !AuthenticationService.isLogged;
                oauthUser();

                //$location.path("/onestopfantasyassistant/assistant");
            })
            .error(function(status, data) {
                console.log(status);
                console.log(data);
            });

        }

        function oauthUser(){
            console.log('hey');
            $http.get('http://www.onestopfantasyassistant.com:8000/auth/v1/RequestToken/')
            .success(function(data) {
                $rootScope.isLoading = false;
                console.log(data);
                $scope.isLogin = false;
                if(data.responseType == 'RequestToken'){
                    window.open(data.value);
                    $location.path('/onestopfantasy')
                }
            })
            .error(function(status, data) {
                $rootScope.isLoading = false;
                $location.path('/onestopfantasy')
            });

        }

        $scope.cancelOverlay = function(){
        	$scope.isLogin = false;
        }
 
        $scope.logout = function () {

            UserService.logOut(username, password).success(function(data) {
            		console.log('Logged Out!')
                }).error(function(status, data) {
                    console.log(status);
                    console.log(data);
                });
            if (AuthenticationService.isLogged) {
                AuthenticationService.isLogged = false;
                delete $window.localStorage.token;
                alert('Logged Out!')
                $scope.isGuest = true;
                $location.path("/");
            }
        }
    }
]).config(function ($httpProvider) {
    $httpProvider.interceptors.push('TokenInterceptor');
});

