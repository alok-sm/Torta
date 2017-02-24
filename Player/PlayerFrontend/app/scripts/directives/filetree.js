'use strict';

//TODO: file statuses
function preProcessFileTree(node){
    if(!node || !node.children){
        return 0;
    }
    if(node.children.length === 0){
        node.icon = 'glyphicon glyphicon-file color_green';
        delete node.children;
        return 1;
    }else{
        node.icon = 'glyphicon glyphicon-folder-open';
        var sum = 0;
        for (var i = 0; i < node.children.length; i++) {
            sum += preProcessFileTree(node.children[i]);
        }
        if(sum === 1){
            node.text = '[' + sum + ' new file] ' + node.text;
        }else{
            node.text = '[' + sum + ' new files] ' + node.text;    
        }
        return sum;
    }
}

angular.module('ngPlayerApp')
    .directive('fileTree', function () {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/filetree.html',
            scope: {
                tree: '='
            },
            link: function postLink($scope, element, attributes) {
                $scope.editable = attributes.editable === 'true';
                
                if(!$scope.editable){
                    preProcessFileTree($scope.tree);    
                }

                $scope.treeConfig = { 
                    'plugins' : [
                        'contextmenu'
                    ], 
                    'contextmenu': {
                        'items': function(node){
                            var disabled = node.state.disabled;
                            var label = disabled? 'Show': 'Hide';
                            return {
                                deleteItem: {
                                    label: label,
                                    action: function () {
                                    }
                                }
                            };
                        }
                    }
                };
            }
        };
    });

