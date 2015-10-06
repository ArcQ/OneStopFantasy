'use strict';

/**
 * @ngdoc function
 * @name frontEndApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the frontEndApp
 */
angular.module('frontEndApp').controller('SyncCtrl', ['$rootScope','$scope', '$http', '$timeout','$location','$window',function ($rootScope,$scope, $http, $timeout,$location,$window) {
	
	$scope.gotFreeAgent = false;
    checkRequestToken();
    $rootScope.loading = true;
	function checkRequestToken(){

		var params = $location.search();
        if(params.oauth_verifier == undefined)
        {
            $window.close();
        }
        else{
            console.log(params.oauth_verifier);
            SendPin(params.oauth_verifier)

        }
	}
	function SendPin(oauth_verifier){
		console.log('oauthUser');
        $http.get('http://www.onestopfantasyassistant.com:8000/auth/v1/AccessToken/?oauth_verifier='+oauth_verifier)
                .success(function(data) {
                $rootScope.loading = true;
                console.log(data);
                $scope.isLogin = false;
                if(data.responseType == 'getAccessToken'){

                    console.log(data.value);
                    if(data.value == 'Success'){
                        $window.close();
                    }
                }
                else{
                    alert("Sorry, we couldn't connect To Yahoo at this time!")
                }
                //$location.path("/onestopfantasyassistant/assistant");
            })
            .error(function(status, data) {
                $rootScope.loading = false;

                console.log(status);
                console.log(data);
            });
    }

}])
