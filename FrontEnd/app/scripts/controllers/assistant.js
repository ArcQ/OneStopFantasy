'use strict';

/**
 * @ngdoc function
 * @name frontEndApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the frontEndApp
 */
angular.module('frontEndApp').controller('AssistantCtrl', ['$rootScope','$scope', '$http', '$timeout','$location','$window',function ($rootScope,$scope, $http, $timeout,$location,$window) {
	var mean = 10;
	var variance = 2;
	var isStarted = false;
	$scope.gotDecisions = false;

	$scope.state = {};
	$scope.state.control = 'begin';
	$scope.state.panel = 'none';
	$scope.state.decision = 'none';
	$scope.state.team_Id = 'none';
	$scope.chartType = '';

	$scope.percentLongRange = 0;
	$scope.averageType = 5;

	$scope.isSubMenu = false;

	$scope.categoryHeaders = ['Points','Rebounds','Assists','3PM','Turnovers','Steals','Blocks','FG%','FT%'];
	$scope.statList = ['points','rebounds','assists','threePointsMade','turnovers','steals','blocks','fieldGoalPercentage','freeThrowPercentage'];
	$scope.stdList = ['points_Std', 'rebounds_Std','assists_Std','steals_Std','blocks_Std','threePointsMade_Std','turnovers_Std','fieldGoalPercentage_Std','freeThrowPercentage_Std'];

	$scope.teamData = {};
	$scope.isSynced = false;
	checkIfSynced(); 

	function checkIfSynced(){
		$rootScope.isLoading = true;
		var request = getUrlForQuery('');

	    $http.get('http://www.onestopfantasyassistant.com:8000/api/v1/FantasyTeam/?format=json&limit=0').success(function(data, status, headers, config) {
	    	console.log(data);
	        if (data.objects.length>0){
	        	$scope.isSynced = true;
	        }
	       	$rootScope.isLoading = false;


		}).error(function(data, status, headers, config) {

	    	$rootScope.isLoading = false;
	        alert("AJAX failed!");
			$rootScope.isLoading = false;

	    });
	}

	$scope.chartObject = {
	  "type": "LineChart",
	  "cssStyle": "height:500px; width:100%;",
	  "displayed": true,
	  "data": {
	    "cols": [
	    	{
	        "id": "stat",
	        "label": "Deviations",
	        "type": "number",
	        "p": {}
	      },
	      {
	        "id": "add",
	        "label": "add",
	        "type": "number",
	        "p": {}
	      },
	      {
	        "id": "drop",
	        "label": "drop",
	        "type": "number",
	        "p": {}
	      }
	    ]
	   },
	  "options": {
	    "title": "Assists Comparison",
	    "isStacked": "true",
	    "fill": 20,
	    "displayExactValues": true,
	    "vAxis": {
	    	"textPosition":"none",
	      "title": "",
	      "gridlines": {
	        "count": 5
	      },
	      'width':400,
	      'height':100
	    },
	    "hAxis": {
	      "title": "Assists"
	    },
	    "curveType": "function"
	  },
	  "formatters": {}
	}

	function setDecisionChart(decision,stat){
		console.log('stat');
		$scope.chartObject.data = {};
		$scope.chartObject.data.cols = [
			{"id": "stat","label": "Deviations","type": "number","p": {}},
	      	{"id": "add","label": "add","type": "number","p": {}},
	    	{"id": "drop","label": "drop","type": "number","p": {}}
	    ];
		$scope.chartObject.data.rows = [];

		// make sure data not repeated
		var checkArray = [];
		var stat_Std = ' ';
		for (var i in $scope.stdList){
			if ($scope.statList[i] == stat){
				stat_Std = $scope.stdList[i];
			}
		}
		var firstMean,firstStd,secondMean, secondStd = 0;
		

		if(decision.add[stat]<decision.drop[stat]){
			firstMean = decision.add[stat];
			firstStd = decision.add[stat_Std];
			secondMean = decision.drop[stat];
			secondStd = decision.drop[stat_Std];
		}
		else{
			secondMean = decision.add[stat];
			secondStd = decision.add[stat_Std];
			firstMean = decision.drop[stat];
			firstStd = decision.drop[stat_Std];
		}

		var addDist = gaussian(decision.add[stat], decision.add[stat_Std]);
		var dropDist = gaussian(decision.drop[stat], decision.drop[stat_Std]);

		$scope.chartObject.data.cols[1].label = decision.add.firstName +' '+decision.add.lastName;
		$scope.chartObject.data.cols[2].label = decision.drop.firstName +' '+decision.drop.lastName;
		$scope.chartObject.options.title =  stat + ' ' + 'comparison';

		var j = -3;
		for (var i = 0; i<12; i++){
			var xPos = firstMean+(firstStd*j);
			//check if already added

			if (checkArray.indexOf(xPos) > -1){

			}
			else{
				checkArray[i] = xPos;
				$scope.chartObject.data.rows[i] = {};
				$scope.chartObject.data.rows[i].c = [];
				$scope.chartObject.data.rows[i].c[0] = {};
				$scope.chartObject.data.rows[i].c[1] = {};
				$scope.chartObject.data.rows[i].c[2] = {};

				$scope.chartObject.data.rows[i].c[0].v = xPos;
				$scope.chartObject.data.rows[i].c[1].v = addDist.pdf(xPos);
				$scope.chartObject.data.rows[i].c[2].v = dropDist.pdf(xPos);
			}
			j = j+0.5;

			
		}
		j = -3;
		var k = 12;
		for (var i = 12; i<24; i++){
			var xPos = secondMean+(secondStd*j);
			console.log(xPos);

			if (checkArray[checkArray.length-1]>xPos){

			}
			else{
				checkArray[k] = xPos;
				$scope.chartObject.data.rows[k] = {};
				$scope.chartObject.data.rows[k].c = [];
				$scope.chartObject.data.rows[k].c[0] = {};
				$scope.chartObject.data.rows[k].c[1] = {};
				$scope.chartObject.data.rows[k].c[2] = {};

				$scope.chartObject.data.rows[k].c[0].v = xPos;
				$scope.chartObject.data.rows[k].c[1].v = addDist.pdf(xPos);
				$scope.chartObject.data.rows[k].c[2].v = dropDist.pdf(xPos);
				k = k +1;
			}
			j = j+0.5;
		}
		

	}

	function getUrlForQuery(query){
		var apiUrl = "http://www.onestopfantasyassistant.com:8000/api/v1/";
		var jsonFormatFooter = "&format=json&limit=0";
		return apiUrl + query + jsonFormatFooter;
	}

	//getting team information
	$scope.recalculate = function(){
		getInitialPayload();
	}

	function getInitialPayload(){
		$rootScope.isLoading = true;
		var request = getUrlForQuery('AssistantInitialPayload/?username='+$window.localStorage.osfaUsername+'&averageType='+$scope.averageType+'&percentLongTerm='+$scope.percentLongRange);
		$http.get(request).success(function(data, status, headers, config) {
			if(data.object.length>0){
				parseData(data)
				console.log($scope.data);
			}
			else{
			}
			$rootScope.isLoading = false;
			$scope.changeStateControl('team');

	    }).error(function(data, status, headers, config) {
	    	$rootScope.isLoading = false;
	        alert("An error has occured!");
	    });

	};

	$scope.changeChart = function(){
		setDecisionChart($scope.dataDecision,$scope.state.stat);
	}

	function parseData(data){
		$scope.data={};
		$scope.data.team = [];
		for (var i in data.object){
			$scope.data.team[i] = {fantasyTeam:{},roster:[],algorithmResult:{}};
			$scope.data.team[i].algorithmResult = JSON.parse(data.object[i].algorithmResult);
			$scope.data.team[i].fantasyTeam = JSON.parse(data.object[i].fantasyTeam);
			for(var j in data.object[i].roster){
				$scope.data.team[i].roster[j] = {athlete:{},stats:{},weekStats:{}}

				$scope.data.team[i].roster[j].athlete = JSON.parse(data.object[i].roster[j].athlete);
				$scope.data.team[i].roster[j].averageStats = JSON.parse(data.object[i].roster[j].averageStats);
				$scope.data.team[i].roster[j].weekStats = data.object[i].roster[j].weekStats;

			}
		}
	}

	$scope.getAthleteComparison = function(stat){
		if($scope.dataDecision != undefined){
			return ($scope.dataDecision.add[stat]-$scope.dataDecision.drop[stat]).toFixed(2);
		}
		else{
			return ' ';
		}
	}

	//user interactions
	$scope.toggleSubmenu = function(){
		$scope.isSubMenu = !($scope.isSubMenu);
		console.log($scope.isSubMenu);

	}
	$scope.changeStateControl = function(state){
		if(!isStarted){
			isStarted = true;
			getInitialPayload()
		}
		else{
			$scope.state.control = state;

		}
	}
	$scope.changeStatePanel = function(state){

		$scope.state.panel = state;

	}

	$scope.clickBack = function(){
		switch($scope.state.control) {
		    case 'decision':
		        $scope.state.control = 'team';
		        break;
		    case 'team':
		        $scope.state.control = 'begin';
		        break;
		    default:
		       $scope.state.control = 'begin';
		}
	}

	$scope.setTeam = function(team_Id){
		$scope.state.team_Id = team_Id;
		$scope.teamData = {};
		//find correct team in data
	}

	$scope.setDecision = function(decision){
		$scope.state.decisionId = decision.id;
		$scope.dataDecision = decision;
		$scope.changeStatePanel('decision');
		$scope.state.stat = 'points';
		setDecisionChart(decision,$scope.state.stat);


	}

	//sync with yahoo
	$scope.oauthUser = function(){
		$rootScope.isLoading = true;
        $http.get('http://www.onestopfantasyassistant.com:8000/auth/v1/RequestToken/').success(function(data) {
        	$rootScope.isLoading = false;
            console.log(data);
            $scope.isLogin = false;
            if(data.responseType == 'RequestToken'){
            	window.open(data.value);
            }
            else if (data.responseType == 'RefreshAccessToken'){
            	if(data.value == 'Success'){
            		alert('Your teams have been synced with Yahoo!');
            		location.reload();
            	}
            }
        })
        .error(function(status, data) {
        	$rootScope.isLoading = false;
            console.log(status);
            console.log(data);
        });
    }

    $scope.statClass=function(stat){
		var statClass = stat<0 ?  'fontRed' :  'fontGreen';
		return statClass;

	}

	//getting free agents pressed
	// $scope.getDecisions = function(teamId){
	// 	$rootScope.isLoading = true;
	// 	var request = getUrlForQuery('Decision/?team_Id='+teamId);
	// 	$scope.gotDecisions = true;

	//     $http.get(request).success(function(data, status, headers, config) {

	//         $scope.dataDecisions = data;
	//         console.log($scope.dataDecisions);
	//        	$rootScope.isLoading = false;

	// 	}).error(function(data, status, headers, config) {

	//     	$rootScope.isLoading = false;
	//         alert("AJAX failed!");

	//     });
	// }	

	//closing decision popup
	$scope.toggle = function(){
		$scope.gotDecisions = !$scope.gotDecisions;
	}

}]).config(function ($httpProvider) {
    $httpProvider.interceptors.push('TokenInterceptor');
}).value('googleChartApiConfig', {
            version: '1',
            optionalSettings: {
                packages: ['corechart', 'gauge'],
                language: 'fr'
            }
    });
