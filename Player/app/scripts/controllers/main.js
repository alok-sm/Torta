'use strict';

angular.module('ngPlayerApp')
    .controller('MainCtrl', function ($scope, $location) {
        $scope.goToRecording = function(){
            $location.path('/recording/' + $scope.recordingId);
        };
    });
