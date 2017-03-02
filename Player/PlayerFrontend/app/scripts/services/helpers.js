'use strict';

angular.module('ngPlayerApp')
    .service('helpers', function ($log) {
        var _helpers = {
            strings: {}
        };

        _helpers.stringStripStart = function(string, prefix){
            if(string.startsWith(prefix)){
                return string.substring(prefix.length);
            }
            return string;
        };

        _helpers.stringStripEnd = function(string, postfix){
            if(string.endsWith(postfix)){
                return string.substring(0, string.length - postfix.length);
            }
            return string;
        };

        _helpers.stringStrip = function(string, character){
            return _helpers.stringStripStart(
                _helpers.stringStripEnd(
                    string, 
                    character), 
                character);
        };

        _helpers.addToObject = function(node, propertyList, value){
            var iterator = node;
            for (var i = 0; i < propertyList.length - 1; i++) {
                if(!iterator[propertyList[i]]){
                    iterator[propertyList[i]] = {};
                }
                iterator = iterator[propertyList[i]];
            }
            iterator[propertyList[i]] = value;
        };

        _helpers.isParentDirectory = function(parent, child){
            parent = _helpers.stringStripEnd(parent, '/');
            child = _helpers.stringStripEnd(child, '/');
            return parent === child || (child.startsWith(parent) && _helpers.stringStripStart(child, parent).startsWith('/'));
        };

        function _applyToNode(node, parent, functionToApply){
            $log.debug(node);
            for (var i = 0; i < node.children.length; i++) {
                _applyToNode(node.children[i], node, functionToApply);
            }

            functionToApply(node, parent);
        }

        _helpers.applyToNode = function(node, functionToApply){
            _applyToNode(node, null, functionToApply);
        };

        return _helpers;
    });
