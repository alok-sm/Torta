'use strict';

angular.module('ngPlayerApp')
    .directive('appWindow', function ($routeParams, $log, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/appwindow.html',
            scope: {
                window: '='
            },
            link: function postLink($scope, element, attrs) {
                $scope.recordingId = $routeParams.id;
                $scope.fileApiUrl = constants.fileApiUrl;

                if($scope.window.visible !== false){
                    $scope.window.visible = true;
                }
            }
        };
    });
