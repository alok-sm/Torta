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

var fileOperation = {
	"open": "write",
	"unlink": "delete",
	"close": "write",
	"rename": "rename"
}


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
		str += getFilesHtml(commands[i].files);
	}

	return str + "</pre>"

}

function pathIsHidden(path){
	for (var i = 0; i < eventLog.hidden_files.length; i++) {
		directoryStructure = eventLog.hidden_files[i].split("/");
		pathDirectoryStructure = path.split("/");

		var pathMatched = true;

		for (var i = 0; i < directoryStructure.length; i++) {
			if(directoryStructure[i] != pathDirectoryStructure[i]){
				pathMatched = false;
				break;
			}
		}

		if(pathMatched){
			return true;
		}
	}

	return false;
}

function getFileOperation(syscall){

}

function getNewPath(file){
	if(file["newpath"]){
		return " <span>to</span> " +
			"<a class='filepath' href='/recordings/" + sessionId + "/filetrace/" + file.newpath.split("/").pop() + "." + file.key + "' target='_blank'>" + file.newpath + "</a>";
	}
	return "";
}

function getFilesHtml(files){
	if(!files){
		return "";
	}
	// var str = "<ul>";

	// for (var i = 0; i < files.length; i++) {
	// 	file = files[i];
	// 	if(pathIsHidden(file.path)){
	// 		str += "<div class='file-row'>" +
	// 				"<button class='unhide-btn file-btn btn btn-default'>" +
	// 					"<span class='glyphicon glyphicon-plus'></span>" + 
	// 				"</button>" +
	// 				"<button class='btn btn-default'>" +
	// 					fileOperation[file.syscall] +
	// 				"</button>" +
	// 				"<span>&nbsp;&nbsp;&nbsp;</span>" +
	// 				"<strike>" +
	// 					"<a class='filepath' href='/recordings/" + sessionId + "/filetrace/" + file.path.split("/").pop() + "." + file.key + "' target='_blank'>" + file.path + "</a>" + 
	// 					getNewPath(file) +
	// 				"</strike>" +
	// 				"<br>" +
	// 			"</div>";
	// 	}else{
	// 		str += "<div class='file-row'>" +
	// 				"<button class='hide-btn file-btn btn btn-default'>" +
	// 					"<span class='glyphicon glyphicon-remove'></span>" + 
	// 				"</button>" +
	// 				"<button class='btn btn-default'>" +
	// 					fileOperation[file.syscall] +
	// 				"</button>" +
	// 				"<span>&nbsp;&nbsp;&nbsp;</span>" +
	// 				"<a class='filepath' href='/recordings/" + sessionId + "/filetrace/" + file.path.split("/").pop() + "." + file.key + "' target='_blank'>" + file.path + "</a>" + 
	// 				getNewPath(file) +
	// 				"<br>" +
	// 			"</div>";
	// 	}
	// }

	// str += 	"</ul>";

	return '<div id="jstree_div"></div>';
}

function getFiles(windowPosition){
	var files = _.filter(eventLog.files, function(file){
		return file.syscall == 'open' && windowPosition.timestamp.start <= file.timestamp && file.timestamp <= windowPosition.timestamp.end;
	});

	return "<h4>Files</h4>" + getFilesHtml(files)
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
	$("#data-container").html("");
	for (var i = 0; i < eventLog.window_positions.length; i++) {
		var windowPosition = eventLog.window_positions[i];
		$("#data-container").append(getContent(windowPosition, eventLog));
	}
	$('.hide-btn').click(hideButtonClick);

	$($('video')[0]).on('play',function(){
	    new Audio('out.mp3').play()
	});

	$($('video')[1]).on('play',function(){
	    new Audio('out2.mp3').play()
	});

	$($('.file-row')[460]).append('<img src="diff.png" style="width:100%"/>')
}

function onGetEventLog(_eventLog){
	eventLog = _eventLog;
	if(!eventLog.hiddenFiles){
		eventLog.hidden_files = [];
	}
	render();
}

function addEntitiyToBeHidden(path){
	path = path.replace(/\/$/, "");
	eventLog.hidden_files.push(path);
	render()
}

function hideButtonClick(){
	console.log(eventLog.hidden_files);
	var clickedHref = $(this).siblings('.filepath').text();
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

$(document).ready(function(){
	$.getJSON("http://localhost:8000/recordings/" + sessionId + "/events.json", onGetEventLog);
});
