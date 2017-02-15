function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}


function clean(node){
    if(node.children.length == 0){
        node.icon = "glyphicon glyphicon-file";
        delete node.children;
    }else{
        node.icon = "glyphicon glyphicon-folder-open"
        for (var i = 0; i < node.children.length; i++) {
            clean(node.children[i]);
        }
    }
}


function treeify(selector, data){
    if(isEmpty(data)){
        return;
    }
    clean(data);
    $(selector).jstree({ 
        'core' : {
            'data' : data
        },
        "plugins" : [
            "contextmenu"
        ], 
        "contextmenu": {
            "items": function(_node){
                var node = "#" + _node.id;
                var disabled = $(node).children('a').hasClass("jstree-disabled");
                var label = disabled? "Show": "Hide";
                return {
                    deleteItem: {
                        label: label,
                        action: function () {
                            if(disabled){
                                $(node).find('.jstree-anchor').removeClass('jstree-disabled')
                            }else{
                                $(node).find('.jstree-anchor').addClass('jstree-disabled')
                                $(node).addClass('jstree-closed')
                            }
                        }
                    }
                }
            }
        }
    }); 
}
