'use strict';

angular.module('ngPlayerApp')
    .directive('screencast', function ($log, $routeParams, constants) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/screencast.html',
            scope: {
                screencast: '='
            },
            link: function postLink($scope, element) {
                var videoPlayer = element.children('video')[0];
                $scope.videoSrc = constants.fileServerUrl + $routeParams.id + '/' + $scope.screencast.src;
                
                $scope.sliderConfig = {
                    showTicks: true,
                    stepsArray: [
                        {value: 0.5,    legend: '½ x'},
                        {value: 0.75,   legend: '¾ x'},
                        {value: 1,      legend: '1 x'},
                        {value: 1.25,   legend: '1¼ x'},
                        {value: 1.5,    legend: '1½ x'},
                        {value: 1.75,   legend: '1¾ x'},
                        {value: 2,      legend: '2 x'}
                    ]
                };

                $scope.$watch('screencast.playbackrate', function(playbackRate){
                    videoPlayer.playbackRate = playbackRate;
                });
            }
        };
    });
