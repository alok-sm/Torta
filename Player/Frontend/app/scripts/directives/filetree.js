'use strict';

angular.module('ngPlayerApp')
    .directive('fileTree', function ($log, fileapi, helpers, _, $, bootbox) {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/filetree.html',
            scope: {
                files: '=',
                collapsedDirectories: '=',
                disablePathGlobal: '&',
                globalDisabledPath: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';
                $scope.runnable = attributes.runnable === 'true';
                
                $scope.numFiles = _.filter($scope.files, function(item, index){
                    return !item.disabled;
                }).length;

                function renderTree(reRender){
                    fileapi.treeify($scope.files, $scope.collapsedDirectories, $scope.editable)
                        .then(function(tree){
                            $scope.tree = tree;
                            if(reRender){
                                $scope.treeConfig.version ++;
                            }
                        });
                }

                $scope.$watch('globalDisabledPath', function(){
                    if($scope.globalDisabledPath){
                        for (var i = 0; i < $scope.files.length; i++) {
                            if(helpers.isParentDirectory($scope.globalDisabledPath, $scope.files[i].path)){
                                $scope.files[i].disabled = true;
                            }
                        } 
                        renderTree(true);
                    }
                });

                function contextMenu(node){
                    // Don't show options for viewer
                    if(!$scope.editable){
                        return {};
                    }

                    return {
                        _enableItem: {
                            label: 'Show',
                            action: function () {
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].disabled = false;
                                    }
                                }
                                renderTree(true);
                            }
                        },
                        _disableItem: {
                            label: 'Hide',
                            action: function () {
                                for (var i = 0; i < $scope.files.length; i++) {
                                    if(helpers.isParentDirectory(node.data.fullpath, $scope.files[i].path)){
                                        $scope.files[i].disabled = true;
                                    }
                                } 
                                renderTree(true);
                            }
                        },
                        _disablePathGlobal: {
                            label: 'Hide Globally',
                            action: function(){
                                $scope.disablePathGlobal({path: node.data.fullpath});
                            }
                        },
                        _validate: {
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
                        _validateExact: {
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
                        _validateNone: {
                            label: 'Don\'t Validate',
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

                $scope.onDoubleClick = function(event){
                    var targetIsFolder = $(
                        $(event.target)
                        .children()[0]
                    ).hasClass('glyphicon-folder-open');

                    if(!targetIsFolder){
                        var path = $(event.target)
                            .closest('li')
                            .jstree()
                            .element[0]
                            .innerText
                            .trim()
                            .split('\n')
                            .join('/')
                            .substr(1);
                        
                        var fileTexts = _
                            .chain($scope.files)
                            .filter(function(file){
                                return !file.disabled && file.path === path && file.text;
                            })
                            .map(function(file){
                                return file.text;
                            })
                            .value();

                        if(fileTexts.length > 0){
                            bootbox.dialog({
                                title: path.split('/').pop(),
                                message: '<pre>' + fileTexts[0] + '</pre>'
                            });
                        }
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
                    'core': {
                        'dblclick_toggle': false
                    },
                    'version': 1
                };
            }
        };
    });

