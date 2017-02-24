'use strict';

angular.module('ngPlayerApp')
    .directive('appWindow', function ($routeParams, $log, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/appwindow.html',
            scope: {
                window: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';
                $scope.recordingId = $routeParams.id;
                $scope.fileServerUrl = constants.fileServerUrl;

                if($scope.window.summary === undefined){
                    $scope.window.summary = '';
                }

                if(!$scope.window.visibility){
                    $scope.window.visibility = 'show';
                }
            }
        };
    });
