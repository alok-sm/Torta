'use strict';

angular.module('ngPlayerApp')
    .directive('fileTree', function () {
        return {
            restrict: 'E',
            templateUrl: 'views/directives/filetree.html',
            scope: {
                tree: '='
            },
            link: function postLink($scope, element, attrs) {
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
