'use strict';

angular.module('ngPlayerApp')
    .directive('terminalCommand', function ($routeParams, $log, $localStorage, bootbox, fileapi, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/terminalcommand.html',
            scope: {
                command: '=',
                disablePathGlobal: '&',
                globalDisabledPath: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';
                $scope.runnable = attributes.runnable === 'true';
                $scope.recordingId = $routeParams.id;
                $scope.fileServerUrl = constants.fileServerUrl;

                $scope.disablePathGlobalIndireciton = function(path){
                    $scope.disablePathGlobal({path: path});
                };

                $scope.validate = function(){
                    if($scope.command.validationScript){
                        fileapi.validate(
                            $localStorage[$scope.recordingId].home, 
                            $scope.command.validationScript
                        ).then(function(response){
                            if(response.returncode !== 0){
                                bootbox.dialog({
                                    title: 'Validation Failed :(',
                                    message:    '<h3>Validation Script:</h3>' +
                                                '<pre>' + $scope.command.validationScript + '</pre>' +
                                                '<h3>stdout:</h3>' + 
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

                $scope.run = function(){
                    fileapi.runCommand($scope.command.cmd, $scope.command.pwd, $scope.command.user);
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
