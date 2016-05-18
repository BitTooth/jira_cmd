from config import cache_path
import json
from task import *

filename = cache_path + '/jira_cache.json'


def saveToCache(tasks):
	f = open(filename, 'w')
	f.write(json.dumps(tasks, indent=4))

def loadFromCache():
	f = open(filename, 'r')
	data = json.loads(f.read())
	
	tasks = []
	for task in data["issues"]:
		temp = JiraTask(task)
		tasks.append(temp)

	return tasks