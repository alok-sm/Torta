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

function getScreenCast(windowPosition){
	return "<center><video controls src='/recordings/" + sessionId + "/" + windowPosition.screencast + "'></video></center><br><br>";
}

function getCommands(windowPosition, eventLog){
	var commands = _.filter(eventLog.commands, function(command){
		return windowPosition.timestamp.start <= command.timestamp && command.timestamp <= windowPosition.timestamp.end;
	});

	if (commands.length == 0) {
		return "";
	}
	
	var str = "<h4>Commands</h4><pre>"

 	for (var i = 0; i < commands.length; i++) {
		str += "<p>" + commands[i].cmd + "</p>";
	}

	return str + "</pre>"

}

function getFiles(windowPosition, eventLog){
	var files = _.filter(eventLog.files, function(file){
		return file.syscall == 'open' && windowPosition.timestamp.start <= file.timestamp && file.timestamp <= windowPosition.timestamp.end;
	})
	console.log(files)

	var str = "<h4>Files</h4><ul>"

	for (var i = 0; i < files.length; i++) {
		file = files[i];
		str += "<ul><a href='/recordings/" + sessionId + "/filetrace/" + file.path.split("/").pop() + "." + file.key + "'>" + file.path + "</a></ul>";
	}
	return str + "</ul>"
}

function getContent(windowPosition, eventLog){
	getFiles(windowPosition, eventLog);
	return "<div class='jumbotron'><h3>" + 
		windowPosition.app + 
		"</h3><br><br>" + 
		getScreenCast(windowPosition) + 
		getCommands(windowPosition, eventLog) + 
		getFiles(windowPosition, eventLog) + 
		"</div>";
}

function onGetEventLog(eventLog){
	for (var i = 0; i < eventLog.window_positions.length; i++) {
		var windowPosition = eventLog.window_positions[i];
		$("#data-container").append(getContent(windowPosition, eventLog));
	}
}

$(document).ready(function(){
	$.getJSON("http://localhost:8080/recordings/" + sessionId + "/events.json", onGetEventLog);
});