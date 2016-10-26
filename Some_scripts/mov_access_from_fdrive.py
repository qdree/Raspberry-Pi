import os
import pyudev
import evdev
import re

def cleanContent(fName):
	fName.seek(0)
	fName.truncate()

def videoNameSet():
	#input of file name
	try:
		video_name = raw_input("Enter file name: ")
	except NameError:
		video_name = input("Enter file name: ")

	pure_name = video_name.split('.')[0].lower()

	try: #if logfile present
		with open('logfile.txt', 'r+') as logfile:
			for line in logfile: #iterate though logfile
				if line == pure_name: #check name is the same as in log
					return line
				else:
					#lambda logfile: logfile.seek(0), logfile.truncate() #func for file's content cleanup
					cleanContent(logfile) #func for file's content cleanup
					logfile.write(pure_name)
					logfile.flush()
					return pure_name

	except IOError: #if no logfile
		with open('logfile.txt', 'w') as logfile: #create file
			logfile.write(pure_name)
			logfile.flush() 
		return pure_name


def pathCreation(video_name):
	pattern = re.compile(r'(.*\.mp4) | (.*\.mpeg) | (.*\.avi) | (.*\.mkv)', flags = re.I | re.X | re.U) #pattern for regex
	os.chdir('/media/')
	try:
		for dirName, curdirList, fileList in os.walk(os.getcwd()): #iterate through generator of pathes
			for file in fileList:
				full_path = os.path.join(dirName, file) #full path to file creation
				re_file = str(pattern.findall(str(full_path))).split('/') #get all files matching the pattern 
				if len(re_file) > 1:
					file_full_name = re_file[-1].translate(None, ',()[]\'\"') #chars to avoid in name
					file_name = file_full_name.split('.')[0] #pure name without format
					print ("Found : {0} located in :{1}".format(file_full_name, full_path))

					print video_name, file_name
					if video_name == file_name.lower(): #check chosen file with files from a list
						print ('Path to target file : {0}'.format(full_path))
						return full_path

	except Exception as e:
		print (e)


pathCreation(videoNameSet())