'use strict';

angular.module('App.controller', [])
.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.persons = [];
	$scope.persons_filtered = [];
	$scope.person = false;
	$scope.person_id = false;
	$scope.modal_error = null;

	$scope.getAllPersons = function() {
		$http.get(base_url+'api/v1/person/person/').then(function(response){
			$scope.persons = response.data;
		}, function(){
			console.log('ERROR');
		});
	}
	$scope.getAllPersons();

	$scope.filterPersons = function(firstName) {
		if (firstName == '') {
			$scope.persons_filtered = [];
			return;
		}
		$http.get(base_url+'api/v1/person/person/', { params: { firstName: $scope.firstName } }).then(function(response){
			$scope.persons_filtered = response.data;
		}, function(){
			console.log('ERROR');
		});
	}
	$scope.getAllPersons();

	$scope.getPersonById = function(p_id) {
		var p = $scope.persons.filter(function(person){
			return person.id == p_id
		});
		var person = false;
		if (p.length == 1) {
			person = p[0];
		}
		return person;
	}
	$scope.changePerson = function(person_id) {
		$scope.person = $scope.getPersonById(person_id);
	}
	$scope.savePerson = function(new_person) {
		$http.post(base_url+'api/v1/person/person/', new_person).then(function(response){
			$scope.modal_error = false;
			$scope.getAllPersons();
		}, function(response) {
			$scope.modal_error = response.data;
		});
		new_person = {};
	}
	$scope.$watch('person_id', function(newValue){
		$scope.changePerson(newValue);
	});
}])

