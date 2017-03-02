'use strict';

angular.module('ngPlayerApp')
    .directive('fileTree', function ($log, fileapi, helpers) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/filetree.html',
            scope: {
                files: '=',
                collapsedDirectories: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';

                function renderTree(reRender){
                    fileapi.treeify($scope.files, $scope.collapsedDirectories, $scope.editable)
                        .then(function(tree){
                            $scope.tree = tree;
                            if(reRender){
                                $scope.treeConfig.version ++;
                            }
                        });
                }

                function contextMenu(node){
                    // Don't show options for viewer
                    if(!$scope.editable){
                        return {};
                    }

                    return {
                        enableItem: {
                            label: 'Enable',
                            action: function () {
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].disabled = false;
                                    }
                                }
                                renderTree(true);
                            }
                        },
                        disableItem: {
                            label: 'Disable',
                            action: function () {
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].disabled = true;
                                    }
                                 } 
                                 renderTree(true);
                            }
                        },
                        validate: {
                            label: 'Validate',
                            action: function(){
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].validate = true;
                                        $scope.files[i].validateExact = false;
                                    }
                                } 
                                renderTree(true);
                            }
                        },
                        validateExact: {
                            label: 'Validate Exact',
                            action: function(){
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].validate = true;
                                        $scope.files[i].validateExact = true;
                                    }
                                } 
                                renderTree(true);
                            }
                        },
                        validateNone: {
                            label: 'Don\'t validate',
                            action: function(){
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].validate = false;
                                        $scope.files[i].validateExact = false;
                                    }
                                }
                                renderTree(true);
                            }
                        }
                    };
                }

                $scope.onNodeClose = function(tree, event){
                    // Don't call API in viewer
                    if(!$scope.editable){
                        return;
                    }

                    var path = event.node.data.fullpath;
                    var index = $scope.collapsedDirectories.indexOf(path);

                    if(index < 0){
                        $scope.collapsedDirectories.push(path);
                    }
                };

                $scope.onNodeOpen = function(tree, event){
                    // Don't call API in viewer
                    if(!$scope.editable){
                        return;
                    }

                    var path = event.node.data.fullpath;
                    var index = $scope.collapsedDirectories.indexOf(path);

                    if(index >= 0){
                        $scope.collapsedDirectories.splice(index, 1);
                    }
                };

                renderTree(false);

                $scope.treeConfig = { 
                    'plugins' : [
                        'contextmenu'
                    ], 
                    'contextmenu': {
                        'items': contextMenu
                    },
                    'version': 1
                };
            }
        };
    });

