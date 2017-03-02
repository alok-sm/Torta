'use strict';

angular.module('ngPlayerApp')
    .service('fileapi', function ($http, constants) {
        
        function getEventlogApiEndpoint(recordingId){
            // URL hack to prevent caching of event log
            return constants.fileApiUrl + 'eventlog/' + recordingId + '?_=' + Math.random();
        }

        return {
            readWindows: function(recordingId){
                return $http.get(getEventlogApiEndpoint(recordingId))
                    .then(function(response){
                        return response.data;
                    });
            },
            writeWindows: function(recordingId, windows){
                return $http.post(getEventlogApiEndpoint(recordingId), windows)
                    .then(function(response){
                        return response.data;
                    });
            },
            treeify: function(files, collapsedDirectories, editable){
                return $http.post(constants.fileApiUrl + 'treeify', {
                    files: files,
                    collapsedDirectories: collapsedDirectories,
                    editable: editable
                }).then(function(response){
                    return response.data;
                });
            },
            runscript: function(home, script){
                return $http.post(constants.fileApiUrl + 'runscript', {
                    home: home,
                    script: script,
                }).then(function(response){
                    return response.data;
                });
            }
        };
    });
