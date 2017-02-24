'use strict';

angular.module('ngPlayerApp')
    .controller('RecordingCtrl', function ($routeParams, $scope, $log, bootbox, fileapi) {   
        function renderEventLog(windows){
            $scope.windows = windows;
        }

        $scope.saveChanges = function(){
            $log.debug($scope.windows);
            fileapi.writeWindows($routeParams.id, $scope.windows).then(function(){
                bootbox.alert('Saved!');
            })
        };

        fileapi.readWindows($routeParams.id).then(renderEventLog);
    });
