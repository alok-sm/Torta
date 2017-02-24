'use strict';

angular.module('ngPlayerApp')
    .controller('RecordingCtrl', function ($routeParams, $scope, $log, bootbox, fileapi, constants) {

        // Move to preprocess.py soon
        // function preProcessFileTree(node){
        //     if(!node || !node.children){
        //         return 0;
        //     }
        //     if(node.children.length === 0){
        //         node.icon = 'glyphicon glyphicon-file color_green';
        //         delete node.children;
        //         return 1;
        //     }else{
        //         node.icon = 'glyphicon glyphicon-folder-open';
        //         var sum = 0;
        //         for (var i = 0; i < node.children.length; i++) {
        //             sum += preProcessFileTree(node.children[i]);
        //         }
        //         if(sum === 1){
        //             node.text = '[' + sum + ' new file] ' + node.text;
        //         }else{
        //             node.text = '[' + sum + ' new files] ' + node.text;    
        //         }
        //         return sum;
        //     }
        // }

        // function preProcessCommand(command){
        //     if(command.cmd === 'ls'){
        //         command.visible = false;
        //     }else{
        //         command.visible = true;
        //     }
        //     preProcessFileTree(command.filestructure);
        // }

        // function preProcessSingleWindow(appWindow){
        //     // appWindow.visible = true;
        //     appWindow.caption = '';
        //     preProcessFileTree(appWindow.filestructure);
        //     if(appWindow.commands){
        //         for (var i = 0; i < appWindow.commands.length; i++) {
        //             preProcessCommand(appWindow.commands[i]);
        //         }
        //     }
        // }

        // function preProcessWindows(windows){
        //     for (var i = 0; i < windows.length; i++) {
        //         preProcessSingleWindow(windows[i]);
        //         // windows[i].caption = '';
        //     }
        // }
        
        function renderEventLog(windows){
            windows[2].visible = false;
            $scope.windows = windows;
        }

        $scope.saveChanges = function(){
            bootbox.alert('Saved!');
        };

        fileapi.readWindows($routeParams.id).then(renderEventLog);
    });
