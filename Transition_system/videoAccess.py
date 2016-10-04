import os
import re

def nameCheck(fName):
	try: #if logfile present
		with open('logfile.txt', 'r+') as logfile:
			for line in logfile: #iterate though logfile
				if line == fName or len(fName) < 1:
					return line
				else:
					logfile.seek(0)
					logfile.truncate() #cleanup
					logfile.write(fName)
					logfile.flush()
					return fName

	except IOError: #if no logfile
		with open('logfile.txt', 'w') as logfile: #create file
			logfile.write(fName)
			logfile.flush() 
		return fName

def pathCreation(vName):
	video_name = str(vName).split('.')[0].lower()
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
					
					if video_name == file_name.lower(): #check chosen file with files from a list
						print ('Path to target file : {0}'.format(full_path))
						return full_path
					else:
						print ("Found : {0} located in :{1}".format(file_full_name, full_path))
	except Exception as e:
		print (e)