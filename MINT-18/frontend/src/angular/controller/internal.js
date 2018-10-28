angular
    .module("app")
    .controller("InternalController",
        function($scope,
            JsonData,
            $timeout) {

            JsonData.getData(data => $scope.rawJson = data);

            $scope.select = which => {
                $scope.selected = which;
            };
            $scope.selected = 'table';
        });
