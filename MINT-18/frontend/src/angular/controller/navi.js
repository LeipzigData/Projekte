angular
    .module("app")
    .controller("NaviController",
        function($scope,
            $routeParams,
            $controller,
            $rootScope,
            $location) {

            $scope.activeMenu = "";

            $scope.$on('$routeChangeSuccess', function(next, current) {
                $scope.activeMenu = "";
                if (current.$$route.originalPath.indexOf("/info") >= 0) { // info
                    $scope.activeMenu = "info";
                } else if (current.$$route.originalPath.indexOf("/search") >= 0) { // search
                    $scope.activeMenu = "search";
                } else if (current.$$route.originalPath.indexOf("/e") >= 0) { // search
                    $scope.activeMenu = "detail";
                } else {
                    $scope.activeMenu = "";
                }
            });
        });
