"""
 Commands:
	hubot help - Display help message
"""

config = require('../config.json')

import stuff

def init(robot):
	
	helpString = robot.helpCommands().join('\n').replace('hubot', robot.name)

	def sendHelp(msg):
		msg.send(helpString)

	robot.respond('help', sendHelp)

	def announce():
		robot.messageRoom(config.hipchat.room, 'Im back')
		robot.messageRoom(config.hipchat.room, helpString)

	setTimeout(announce, 1000)

module.exports = init