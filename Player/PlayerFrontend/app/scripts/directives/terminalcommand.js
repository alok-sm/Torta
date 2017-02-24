'use strict';

angular.module('ngPlayerApp')
    .directive('terminalCommand', function ($routeParams, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/terminalcommand.html',
            scope: {
                command: '='
            },
            link: function postLink($scope) {
                $scope.recordingId = $routeParams.id;
                $scope.fileServerUrl = constants.fileServerUrl;

                if($scope.command.visible !== false){
                    $scope.command.visible = true;
                }
            }
        };
    });
