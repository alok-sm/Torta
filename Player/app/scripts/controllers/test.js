'use strict';

/**
 * @ngdoc function
 * @name ngPlayerApp.controller:TestCtrl
 * @description
 * # TestCtrl
 * Controller of the ngPlayerApp
 */
angular.module('ngPlayerApp')
    .controller('TestCtrl', function ($scope) {
        $scope.windows = [
            {
                name: 'alok',
                age: 22
            },
            {
                name: 'adi',
                age: 18
            }
        ];
    });
