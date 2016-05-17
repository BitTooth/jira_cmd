import requests as r
from requests.auth import HTTPBasicAuth
import json
from task import *
import sys
from config import login, password, jira_url, custom_names

r.packages.urllib3.disable_warnings()

auth = HTTPBasicAuth(login, password)
basic_url = jira_url + "/rest/api/2/"

commands = {
	'anphd':' project = "ANPHD" ',
	'me':' assignee="' + login + '"',
	'open':' status not in ("Back Log", DONE, Closed, Resolved) ',
	'bl':' status = "Back Log" ',
	'pr':' component in (Programming, "Programming - Build", "Programming - Game Assets", "Programming - Game Mechanics", "Programming - Online: Client ", "Programming - Online: Server ", "Programming - Optimization", "Programming - Scripts", "Programming - Tools/Libs", "Programming - Tracking/Antihacking", "Programming - UI") ',
	'and':' AND ',
	'or':' OR ',
}

def printHelp():
	print 'me - my opened tasks'
	print 'me_all - all my tasks'
	print 'anphd - all anphd project opened tasks'
	print 'anphd_pr - opened anphd programming tasks'
	print 'anphd_bl - task in backlog of anphd project' 
	print 'anphd_pr_bl - programming tasks in backlog'
	print 'jql - the rest of the command line is jql so parse it'

def getAndPrintTasks(jql):
	params = {
		'jql':jql
	}

	resp = r.get(basic_url + 'search', params=params, auth=auth, verify=False)
	data = json.loads(resp.text)

	#print data

	tasks = []
	for task in data["issues"]:
		temp = JiraTask(task)
		tasks.append(temp)

	#print json.dumps(data["issues"][0], indent=4, sort_keys=True)
	if len(tasks) > 0:
		printTasks(tasks)
	else:
		print 'Tasks not found'


def printMyTasks():
	jql = commands['me']
	getAndPrintTasks(jql)

def printMyOpenedTasks():
	jql = commands['me'] + commands['and'] + commands['open']
	getAndPrintTasks(jql)

def printAnphdBacklog():
	jql = commands['anphd'] + commands['and'] + commands['bl']
	getAndPrintTasks(jql)

def printAllAnphdOpened():
	jql = commands['anphd'] + commands['and'] + commands['open']
	getAndPrintTasks(jql)

def printProgrammingOpened():
	jql = commands['anphd'] + commands['and'] + commands['open'] + commands['and'] + commands['pr']
	getAndPrintTasks(jql)

def printProgrammingBacklog():
	jql = commands['anphd'] + commands['and'] + commands['bl'] + commands['and'] + commands['pr']
	getAndPrintTasks(jql)

def parseJql():
	cmds = dict(commands.items() + custom_names.items())
	jql = ''
	for param in sys.argv[2:]:
		try:
			jql = jql + cmds[param.lower()]
		except:
			print 'Unknown command', param
			return
	getAndPrintTasks(jql)



if __name__ == '__main__':	

	if len(sys.argv) == 1:
		printMyTasks()
		exit()

	arg = sys.argv[1]
	if arg == 'me_all': printMyTasks()
	elif arg == 'me': printMyOpenedTasks()
	elif arg == 'anphd_bl': printAnphdBacklog()
	elif arg == 'anphd' : printAllAnphdOpened()
	elif arg == 'anphd_pr' : printProgrammingOpened()
	elif arg == 'anphd_pr_bl': printProgrammingBacklog()
	elif arg == 'jql' : parseJql()
	elif arg == 'help': printHelp()
