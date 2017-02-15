'use strict';

angular.module('ngPlayerApp')
    .service('fileapi', function ($http, constants) {
        return {
            readWindows: function(recordingId){
                return $http
                    .get(constants.fileApiUrl + recordingId + '/events.json')
                    .then(function(response){
                        return response.data;
                    });
            }
            // ,
            // redirect: function(recordingId, path){
                
            // },
            // writeWindows: function(recordingId, object){

            // }
        };
    });
