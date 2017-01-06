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
var eventLog = null;

function getScreenCast(windowPosition){
	return "<center><video controls src='/recordings/" + sessionId + "/" + windowPosition.screencast + "'></video></center><br><br>";
}

function getCommands(windowPosition){
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

function getFiles(windowPosition){
	var files = _.filter(eventLog.files, function(file){
		return file.syscall == 'open' && windowPosition.timestamp.start <= file.timestamp && file.timestamp <= windowPosition.timestamp.end;
	});

	var str = 	"<h4>Files</h4>"
	str += 		"<ul>"

	for (var i = 0; i < files.length; i++) {
		file = files[i];
		str += "<div class='file-row'>" +
					"<button class='hide-btn btn btn-default'>" +
						"<span class='glyphicon glyphicon-remove'></span>" + 
					"</button>" +
					"<span>&nbsp;&nbsp;&nbsp;</span>" +
					"<a class='filepath' href='/recordings/" + sessionId + "/filetrace/" + file.path.split("/").pop() + "." + file.key + "' target='_blank'>" + file.path + "</a>" + 
					"<br>" +
				"</div>";
	}

	str += 		"</ul>"

	return str;
}

function getContent(windowPosition){
	getFiles(windowPosition, eventLog);
	return "<div class='jumbotron'><h3>" + 
		windowPosition.app + 
		"</h3><br><br>" + 
		getScreenCast(windowPosition) + 
		getCommands(windowPosition, eventLog) + 
		getFiles(windowPosition, eventLog) + 
		"</div>";
}

function render(){
	for (var i = 0; i < eventLog.window_positions.length; i++) {
		var windowPosition = eventLog.window_positions[i];
		$("#data-container").append(getContent(windowPosition, eventLog));
	}
	$('.hide-btn').click(hideButtonClick);
}

function onGetEventLog(_eventLog){
	eventLog = _eventLog;
	if(!eventLog.hiddenFiles){
		eventLog.hidden_files = [];
	}
	render();
}

function addEntitiyToBeHidden(path){
	path = path.replace(/\/$/, "") + "/";
	eventLog.hidden_files.push(path);
	render()
}

function hideButtonClick(){
	var clickedHref = $(this).siblings('.filepath').attr('href');
	bootbox.confirm({
		title: "Remove a file entry",
		message: "What do you want to remove?",
		buttons: {
		    cancel: {
		        label: "<span class='glyphicon glyphicon-folder-open'></span>&nbsp;&nbsp;&nbsp; Remove Folder"
		    },
		    confirm: {
		        label: "<span class='glyphicon glyphicon-file'></span>&nbsp;&nbsp;&nbsp; Remove File"
		    }
		},
		callback: function (removeFile) {
		    if(removeFile == true){
				addEntitiyToBeHidden(clickedHref);
			}

			if(removeFile == false){
				bootbox.prompt({
					title: "What folder do you want to remove?",
					value: clickedHref,
					callback: function(result) {
						addEntitiyToBeHidden(result);
					}
				});
			}
		}
	});
}

$(function(){
	$.getJSON("http://localhost:8000/recordings/" + sessionId + "/events.json", onGetEventLog);
});
