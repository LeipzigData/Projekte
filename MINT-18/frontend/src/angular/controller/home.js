angular
    .module("app")
    .controller("HomeController", function($scope, JsonData) {
        // Fetch data to count the number of entries
        JsonData.getData(data => $scope.baseData = data);
    });
