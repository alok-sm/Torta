'use strict';

angular.module('ngPlayerApp')
    .service('constants', function () {
        return {
            fileServerUrl: 'http://localhost:7000/recordings/',
            fileApiUrl: 'http://localhost:8000/'
        };
    });
