'use strict';

angular.module('ngPlayerApp')
    .controller('MainCtrl', function ($scope, $location) {
        $scope.goToEditor = function(){
            $location.path('/editor/' + $scope.recordingId);
        };

        $scope.goToViewer = function(){
            $location.path('/viewer/' + $scope.recordingId);
        };

        $scope.goToRunner = function(){
            $location.path('/viewer/' + $scope.recordingId).search({runnable : '1'});
        };
    });
