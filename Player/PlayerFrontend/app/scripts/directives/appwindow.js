'use strict';

angular.module('ngPlayerApp')
    .directive('appWindow', function ($routeParams, $log, $localStorage, bootbox, fileapi, constants) {
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

                $scope.validate = function(){
                    if($scope.window.validationScript){
                        fileapi.runscript(
                            $localStorage[$scope.recordingId].home, 
                            $scope.window.validationScript
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
                }

                if($scope.window.collapsedDirectories === undefined){
                    $scope.window.collapsedDirectories = [];
                }

                if($scope.window.validationScript === undefined){
                    $scope.window.validationScript = '';
                }

                if($scope.window.summary === undefined){
                    $scope.window.summary = '';
                }

                if(!$scope.window.visibility){
                    $scope.window.visibility = 'show';
                }
            }
        };
    });
