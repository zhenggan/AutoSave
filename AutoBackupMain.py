#!/usr/bin/python

# A simple script to schedule backups
# Use Case: See README
# todo: add feature to filter by file type

import sys
import shutil
import datetime
import time
import schedule
import re

def connectSSH(source, destination):
    #todo: Make behavior more like local backup where there are multiple ones with timestamped names
    output = subprocess.call('scp -r source destination', shell = True)

def Backup(source, destination, sshBool):
	if sshBool == True:
		connectSSH(source, destination)
	else:
		shutil.copytree(source, destination + '/' + source + str(datetime.datetime.now())) #Uses current date as unique identifier of backup
	print ('Backup from ' + source + ' to ' + destination + ' completed')

#Converts civilian to military time
#Used by scheduler since scheduler uses military time but user enters civilian time
#params: int: hour
#		 int: minutes
#		 bool: true for am, false for pm		 
def civilianToMilitaryTime(hour, minutes, ampm):
	militaryHour = 0
	
	if ampm:
		if hour != 12:
			militaryHour = hour
		else:
			militaryHour = 0
	else:
		if hour == 12:
			militaryHour = hour
		else:
			militaryHour = hour + 12

	timeString = str(militaryHour) + ':' + str(minutes)
	return timeString

def main():
	#TODO: Implement regex to check inputs
	source = sys.argv[1]
	destination = sys.argv[2]
	ssh = sys.argv[3]
	if ssh != '0' and ssh != '1':
		print('Please enter if backup is SSH or not as 4th argument: 1 for yes, 0 for no')
		exit()

	sshBool = None
	if ssh == '1':
		sshBool = True 
	else:
		sshBool = False

	timeScheduled = 0
	if len(sys.argv) > 4:
		#Regex to make sure time is in correct format
		contents = re.findall('^([1-9]|1[0-2]):([0-5]?[0-9])(am|pm)$', sys.argv[4])
		if contents:
			contentscontents = contents[0]
			ampm = False
			if contentscontents[2] == 'am':
				ampm = True
			else:
				ampm = False
			timeScheduled = civilianToMilitaryTime(int(contentscontents[0]), int(contentscontents[1]), ampm)
		else:
			print('Please enter a proper time for scheduled backups in format Hour:MinuteAMPM, example: 08:30am')
			exit()
	else:
		Backup(source, destination, sshBool)
		exit() #If doing instant backup, exit now

	#if doing timed backups, don't exit, keep program running
	schedule.every().day.at(timeScheduled).do(Backup, source, destination, sshBool)
	print ('Backup from ' + source + ' to ' + destination + ' scheduled for ' + sys.argv[4])
	while 1:
		schedule.run_pending()
		time.sleep(10)

if __name__ == '__main__':
	main()
