'use strict';

angular.module('ngPlayerApp')
    .controller('ViewerCtrl', function ($routeParams, $scope, fileapi) {
        function renderEventLog(windows){
            $scope.windows = windows;
        }

        $scope.recordingId = $routeParams.id;
        fileapi.readWindows($routeParams.id).then(renderEventLog);
    });
