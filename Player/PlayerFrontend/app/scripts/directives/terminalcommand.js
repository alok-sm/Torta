'use strict';

angular.module('ngPlayerApp')
    .directive('terminalCommand', function ($routeParams, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/terminalcommand.html',
            scope: {
                command: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';
                $scope.recordingId = $routeParams.id;
                $scope.fileServerUrl = constants.fileServerUrl;

                if($scope.command.summary === undefined){
                    $scope.command.summary = '';
                }

                if(!$scope.command.visibility){
                    $scope.command.visibility = 'show';
                }
            }
        };
    });
