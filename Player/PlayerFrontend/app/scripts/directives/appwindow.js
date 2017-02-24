'use strict';

angular.module('ngPlayerApp')
    .directive('appWindow', function ($routeParams, $log, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/appwindow.html',
            scope: {
                window: '='
            },
            link: function postLink($scope) {
                $scope.recordingId = $routeParams.id;
                $scope.fileServerUrl = constants.fileServerUrl;

                if($scope.window.visible !== false){
                    $scope.window.visible = true;
                }
            }
        };
    });
