#!/usr/bin/python3

# Right now this is just a simple script to backup files
# Use Case: ./AutoBackupMain.py source destination ssh(bool) 
# todo: add timing feature so that backup occurs at the same time each day
# todo: add feature to filter by file type
# todo: add user interface
# todo: add ssh support using ssh key
# todo: add ssh support using ssh password
# todo: add error checking

import sys
import shutil
import datetime

#TODO: Implement
def connectSSH(source, destination):
	pass

#Currently only supports backup to directory on local machine
def Backup(source, destination, sshBool):
	print ('source: ' + source)
	print ('destination: ' + destination)
	if sshBool == True:
		connectSSH(source, destination)
	else:
		shutil.copytree(source, destination + '/' + source + str(datetime.datetime.now())) #Uses current date as unique identifier of backup

#Currently this program does a backup everytime it is ran, future support will be added for automated periodic backups
def main():
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

	Backup(source, destination, sshBool)

if __name__ == '__main__':
	main()