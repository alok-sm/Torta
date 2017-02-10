$.urlParam = function(name){
    var results = new RegExp("[\?&]" + name + "=([^&#]*)").exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

var sessionId = $.urlParam("id");
var windowList = null;
var fileTrees = {};

function getScreenCast(appWindow){
	return "<center>" + 
				"<video controls src='/recordings/" + sessionId + "/" + appWindow.screencast + "'>" +
				"</video>" + 
			"</center>" + 
			"<br><br>";
}

function getFileTree(filestructure){
	if(!filestructure){
		return "";
	}

	var key = Math.random().toString(36).substr(2, 5);
	fileTrees["#jstree_" + key] = filestructure;
	return '<div id="jstree_' + key + '"></div>';
}

function renderTrees(){
	for (var key in fileTrees) {
		if (fileTrees.hasOwnProperty(key)) {
			console.log(key)
			console.log(fileTrees[key])
			treeify(key, fileTrees[key]);
		}
	}
}

function getCommandHTML(command){
	return "<pre>" + 
				"<p>" + command.cmd + "</p>" +
				getFileTree(command.filestructure) +
			"</pre>";
}

function getCommands(appWindow){
	if( (!appWindow) || (!appWindow.commands) || appWindow.commands == [] ){
		return "";
	}

	var str = "<h4>Commands</h4>"

	for (var i = 0; i < appWindow.commands.length; i++) {
		str += getCommandHTML(appWindow.commands[i]);
	}

	return str;
}

function getWindowHTML(appWindow){
	return "<div class='jumbotron'>" +
				"<h3>" + appWindow.app + "</h3>" + 
				"<br><br>" + 
				getScreenCast(appWindow) + 
				getCommands(appWindow) + 
				getFileTree(appWindow.filestructure) +
			"</div>";


}

function render(){
	for (var i = 0; i < windowList.length; i++) {
		$("#data-container").append(getWindowHTML(windowList[i]));
	}
	renderTrees();
}

function onGetEventLog(_windowList){
	windowList = _windowList;
	render();
}

$(document).ready(function(){
	$.getJSON("http://localhost:8000/recordings/" + sessionId + "/events.json", onGetEventLog);
});
