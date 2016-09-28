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
		with open('logfile.txt', 'r+') as logfile:
			logfile.write(video_name)
			logfile.flush()
			for line in logfile: #iterate though logfile
				splitted = line.split('.') #create pure video name - without format
				#print (splitted)
				if splitted[0] == video_name: #check name is the same as in log
					return splitted[0]
				else:
					video_name.split(".") #if not, create pure video name to return
					return video_name

	except IOError: #if no logfile
		with open('logfile.txt', 'w') as logfile: #create file
			video_name.split(".")
			logfile.write(video_name)
			logfile.flush() 
		return video_name

	


def pathCreation(video_name):
	pattern = re.compile(r'.*mp4 | .*mpeg | .*avi', flags = re.I | re.X | re.U) #pattern for regex
	os.chdir('/media/')
	try:
		for dirName, curdirList, fileList in os.walk(os.getcwd()): #iterate through generator of pathes
			for file in fileList:
				full_path = os.path.join(dirName, file) #full path to file creation
				re_file = str(pattern.findall(str(full_path))).split('/') #get all files matching the pattern 
				if len(re_file) > 1:
					file_name = re_file[-1].split('.')[0] #pure file name - without format
					print (file_name)
					if video_name == file_name: #check chosen file with gotten list
						print (full_path)
						return full_path

	except Exception as e:
		print (e)


pathCreation(videoNameSet())