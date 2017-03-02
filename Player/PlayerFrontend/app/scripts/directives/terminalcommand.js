'use strict';

angular.module('ngPlayerApp')
    .directive('terminalCommand', function ($routeParams, $log, $localStorage, bootbox, fileapi, constants) {
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

                $scope.validate = function(){
                    if($scope.command.validationScript){
                        fileapi.runscript(
                            $localStorage[$scope.recordingId].home, 
                            $scope.command.validationScript
                        ).then(function(response){
                            if(response.returncode !== 0){
                                bootbox.dialog({
                                    title: 'Validation Failed :(',
                                    message:    '<h3>stdout:</h3>' + 
                                                '<pre>' + response.stdout + '</pre>' +
                                                '<h3>stderr:</h3>' + 
                                                '<pre>' + response.stderr + '</pre>'
                                });
                            }else{
                                bootbox.alert('Validation succeeded! :)');
                            }
                        });
                    }else{
                        bootbox.alert('Validation succeeded! :)');
                    }
                };

                if($scope.command.collapsedDirectories === undefined){
                    $scope.command.collapsedDirectories = [];
                }

                if($scope.command.summary === undefined){
                    $scope.command.summary = '';
                }

                if($scope.command.validationScript === undefined){
                    $scope.command.validationScript = '';
                }

                if(!$scope.command.visibility){
                    $scope.command.visibility = 'show';
                }
            }
        };
    });
