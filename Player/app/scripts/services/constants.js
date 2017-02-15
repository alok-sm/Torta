'use strict';

angular.module('ngPlayerApp')
    .service('constants', function () {
        return {
            fileApiUrl: 'http://localhost:8000/recordings/'
        };
    });
