//
// Commands:
//	hubot help - Display help message
//


config = require("../config.json");
/* IMPORTS DONT WORK */

function init () {
	helpString = robot.helpCommands().join("\n").replace("hubot", robot.name);
	
	function sendHelp () {
		msg.send(helpString);
	}
	robot.respond("help", sendHelp);
	
	function announce () {
		robot.messageRoom(config.hipchat.room, "Im back");
		robot.messageRoom(config.hipchat.room, helpString);
	}
	setTimeout(announce, 1000);
}
module.exports = init;
