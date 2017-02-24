'use strict';

angular.module('ngPlayerApp')
    .service('fileapi', function ($http, constants) {
        
        function getEventlogApiEndpoint(recordingId){
            // URL hack to prevent caching of event log
            return constants.fileApiUrl + 'eventlog/' + recordingId + '?_=' + Math.random();
        }

        return {
            readWindows: function(recordingId){
                return $http
                    .get(getEventlogApiEndpoint(recordingId))
                    .then(function(response){
                        return response.data;
                    });
            },
            writeWindows: function(recordingId, windows){
                return $http
                    .post(getEventlogApiEndpoint(recordingId), windows).then(function(response){
                        return response.data;
                    });
            }
        };
    });
