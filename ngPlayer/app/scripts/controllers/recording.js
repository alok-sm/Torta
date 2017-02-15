'use strict';

angular.module('ngPlayerApp')
    .controller('RecordingCtrl', function ($routeParams, $scope, $log, fileapi, constants) {
        
        // Move to preprocess.py soon
        function preProcessFileTree(node){
            if(!node || !node.children){
                return;
            }
            if(node.children.length === 0){
                node.icon = 'glyphicon glyphicon-file';
                delete node.children;
            }else{
                node.icon = 'glyphicon glyphicon-folder-open';
                for (var i = 0; i < node.children.length; i++) {
                    preProcessFileTree(node.children[i]);
                }
            }
        }

        function preProcessSingleWindow(window){
            preProcessFileTree(window.filestructure);
            if(window.commands){
                for (var i = 0; i < window.commands.length; i++) {
                    preProcessFileTree(window.commands[i].filestructure);
                }
            }
        }

        function preProcessWindows(windows){
            for (var i = 0; i < windows.length; i++) {
                preProcessSingleWindow(windows[i]);
                windows[i].caption = '';
            }
        }
        
        function renderEventLog(windows){
            preProcessWindows(windows);
            $scope.windows = windows;
        }

        $scope.saveChanges = function(){
            alert('saved!');
        };

        $scope.recordingId = $routeParams.id;
        $scope.fileApiUrl = constants.fileApiUrl;
        fileapi.readWindows($scope.recordingId).then(renderEventLog);
    });
