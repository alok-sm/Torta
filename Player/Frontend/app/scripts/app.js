'use strict';

angular
    .module('ngPlayerApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'ngJsTree',
        'rzModule',
        'ngclipboard',
        'ngStorage'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .when('/error404', {
              templateUrl: 'views/error404.html',
              controller: 'Error404Ctrl',
              controllerAs: 'error404'
            })
            .when('/editor/:id', {
              templateUrl: 'views/editor.html',
              controller: 'EditorCtrl',
              controllerAs: 'editor'
            })
            .when('/viewer/:id', {
              templateUrl: 'views/viewer.html',
              controller: 'ViewerCtrl',
              controllerAs: 'viewer'
            })
            .otherwise({
                redirectTo: '/error404'
            });
    });
