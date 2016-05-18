import os
import webbrowser
from config import jira_url

# Using cecho for colored output
# http://www.codeproject.com/Articles/17033/Add-Colors-to-Batch-Files
cecho = "cecho.exe "

def coloredStatus(status):
	colors = {
		"simple" : "white",
		"Back Log" : "gray",
		"In Progress" : "yellow",
		"In Review" : "yellow",
		"DONE" : "lime",
		"To Do" : "teal",
		"Testing": "aqua"
	}
#	return colored(status["name"], colors.get(status["name"], "white"))
	return '{' + colors.get(status["name"], "white") + '}' + status["name"] + '{#}'

def coloredKey(key, issuetype):
	colors = {
		"Bug" : "red",
		"Task" : "teal"
	}
#	return colored(key, colors.get(issuetype["name"], "white"))
	return '{' + colors.get(issuetype["name"], "white") + '}' + key + '{#}'

def printTasks(tasks):
	for idx, task in enumerate(tasks):
		print str(idx) + ":",
		task.out()

class JiraTask:
	__json = None

	def __init__(self, dump):
		self.__json = dump

	def summary(self):
		return self.__json["fields"]["summary"]

	def assignee(self):
		if self.__json["fields"]["assignee"] is not None:
			return self.__json["fields"]["assignee"]["displayName"]
		else:
			return "Unassigned"

	def key(self):
		return self.__json["key"]

	def issuetype(self):
		return self.__json["fields"]["issuetype"]

	def statusName(self):
		return self.status()["name"]

	def status(self):
		return self.__json["fields"]["status"]

	def description(self):
		return self.__json["fields"]["description"]

	def openInBrowser(self):
		webbrowser.open_new_tab(jira_url + "browse/" + self.__json["key"])

	def printDetailed(self):
		os.system(cecho + 
			coloredKey(self.key(), self.issuetype()) + "\t" + 
			self.summary().encode("UTF-8") + "\t" + 
			coloredStatus(self.status()) + "\t")
		print "\nAssignee:\t", self.assignee()
		print ''
		print self.description()


	def out(self):
#		print coloredKey(self.key(), self.issuetype()), "\t", repr(self.summary()).ljust(65).encode("UTF-8"), "\t", coloredStatus(self.status())
		os.system(cecho + 
			coloredKey(self.key(), self.issuetype()) + "\t" + 
			repr(self.summary()).ljust(65).encode("UTF-8") + "\t" + 
			coloredStatus(self.status()) + "\t" +
			self.assignee())
		print ''