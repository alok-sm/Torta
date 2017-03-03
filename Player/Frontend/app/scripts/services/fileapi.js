'use strict';

angular.module('ngPlayerApp')
    .service('fileapi', function ($http, constants) {
        return {
            readWindows: function(recordingId){
                return $http.get(constants.fileApiUrl + 'eventlog/' + 
                    recordingId + '?_=' + Math.random()
                ).then(function(response){
                    return response.data;
                });
            },
            writeWindows: function(recordingId, windows){
                return $http.post(constants.fileApiUrl + 'eventlog/' + 
                    recordingId, 
                    windows
                ).then(function(response){
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
            validate: function(home, script){
                return $http.post(constants.fileApiUrl + 'validate', {
                    home: home,
                    script: script,
                }).then(function(response){
                    return response.data;
                });
            },
            runCommand: function(command, cwd, user){
                return $http.post(constants.fileApiUrl + 'runcommand', {
                    command: command,
                    cwd: cwd,
                    user: user
                }).then(function(response){
                    return response.data;
                });
            }
        };
    });
