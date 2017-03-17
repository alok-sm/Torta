'use strict';

angular.module('ngPlayerApp')
    .controller('EditorCtrl', function ($routeParams, $scope, bootbox, fileapi) {   
        function renderEventLog(eventLog){
            $scope.eventLog = eventLog;
        }

        $scope.saveChanges = function(){
            fileapi.writeWindows($routeParams.id, $scope.eventLog).then(function(){
                bootbox.alert('Saved!');
            });
        };

        $scope.disablePathCallback = function(path){
            $scope.globalDisabledPath = path;
        };
        
        $scope.recordingId = $routeParams.id;
        fileapi.readWindows($routeParams.id).then(renderEventLog);
    });
