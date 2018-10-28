angular.module("app", [
        'ngRoute',
        'ngResource',
        'ngSanitize',
        'app.services',
        'ngAnimate',
        'LocalStorageModule'
    ])
    .config($routeProvider =>
        $routeProvider
        .when('/', {
            templateUrl: "home.html",
            controller: "HomeController"
        }).when('', {
            templateUrl: "home.html",
            controller: "HomeController"
        }).when('/search', {
            templateUrl: "search.html",
            controller: "SearchController"
        }).when('/e/:entryId*', {
            templateUrl: "entry.html",
            controller: "EntryController"
        }).when('/info', {
            templateUrl: "info.html",
            controller: "InfoController"
        }).when('/internal', {
            templateUrl: "internal.html",
            controller: "InternalController"
        }).otherwise({
            redirectTo: "/"
        })
    );
angular.module('app.services', []);


// Replace broken images with default one
brokenImage = img => {
    img.src = "/images/404.svg";
};
