import os
import pyudev
import evdev
import re

def videoNameSet():
	#input of file name
	try:
		video_name = raw_input("Enter file name: ")
	except NameError:
		video_name = input("Enter file name: ")

	try: #if logfile present
		with open('logfile.txt', 'r') as logfile:
			for line in logfile: #iterate though logfile
				splitted = line.split('.') #create pure video name - without format
				if splitted[0] == video_name: #check name is the same as in log
					return splitted[0]
				else:
					video_name.split(".") #if not, create pure video name to return
					return video_name

	except FileNotFoundError: #if no logfile
		with open('logfile.csv', 'w'): #create file
			logfile.write(video_name)
		video_name.split(".") 
		return video_name


def pathCreation(video_name):
	pattern = re.compile(r'.*mp4 | .*mpeg | .*avi', flags = re.I | re.X | re.U) # pattern for regex
	os.chdir('/media/')
	try:
		for file in os.walk(os.getcwd()): #iter through generator of pathes
			re_file = pattern.findall(file).split('/') #pull of last file in dir and subdir
			file_name = re.file[-1].split('.') #create pure video name - without format
			if video_name == file_name: #check chosen file with gotten list
				# return re_file[-1]
				cwd = os.getcwd() #current working directory
				path_to_video = cwd + re_file
				return path_to_video

	except Exception as e:
		print (e)