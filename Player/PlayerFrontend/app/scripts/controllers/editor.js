'use strict';

angular.module('ngPlayerApp')
    .controller('EditorCtrl', function ($routeParams, $scope, bootbox, fileapi) {   
        function renderEventLog(windows){
            $scope.windows = windows;
        }

        $scope.saveChanges = function(){
            fileapi.writeWindows($routeParams.id, $scope.windows).then(function(){
                bootbox.alert('Saved!');
            });
        };
        
        $scope.recordingId = $routeParams.id;
        fileapi.readWindows($routeParams.id).then(renderEventLog);
    });
