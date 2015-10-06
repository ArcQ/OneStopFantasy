'use strict';

/**
 * @ngdoc function
 * @name frontEndApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontEndApp
 */
angular.module('frontEndApp').controller('StatsCtrl', ['$scope', '$http', '$timeout','$location',function ($scope, $http, $timeout,$location) {

	$scope.state = 'none';
	$scope.refreshStats = function(statType){
		var query = '';
		if (statType == 'season'){
			query = 'Athlete_SeasonAverages';
			$scope.state = 'Season Stats'
		}
		var responsePromise = $http.get("http://www.onestopfantasyassistant.com:8000/api/v1/"+query+"/?format=json&limit=0");

	    responsePromise.success(function(data, status, headers, config) {
			$scope.data = data.objects;
	        console.log($scope.data);

	    });

	    responsePromise.error(function(data, status, headers, config) {
	        alert("AJAX failed!");
	    });
	};



 }]);
