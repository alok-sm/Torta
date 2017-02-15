'use strict';

angular
    .module('ngPlayerApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'ngJsTree'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .when('/about', {
                templateUrl: 'views/about.html',
                controller: 'AboutCtrl',
                controllerAs: 'about'
            })
            .when('/error404', {
              templateUrl: 'views/error404.html',
              controller: 'Error404Ctrl',
              controllerAs: 'error404'
            })
            .when('/recording/:id', {
              templateUrl: 'views/recording.html',
              controller: 'RecordingCtrl',
              controllerAs: 'recording'
            })
            .otherwise({
                redirectTo: '/error404'
            });
    });
