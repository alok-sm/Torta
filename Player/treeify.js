function treeify(selector, data){
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
                                $(node).find('a').removeClass('jstree-disabled')
                            }else{
                                $(node).find('a').addClass('jstree-disabled')
                            }
                        }
                    }
                }
            }
        }
    }); 
}

function clean(node){
    if(node.children.length == 0){
        node.icon = "glyphicon glyphicon-file";
    }else{
        node.icon = "glyphicon glyphicon-folder-open"
        for (var i = 0; i < node.children.length; i++) {
            clean(node.children[i])
        }
    }
}