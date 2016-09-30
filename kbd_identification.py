import pyudev 
import evdev 
import functools
import re


context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem = 'input')

monitor.start()

def kbdIden():
	target_device_data = [] #list to store recieved data about device
	for device in iter(functools.partial(monitor.poll, 0), None):
			#print ('{0.action} on {0.device_path}'.format(device))

			target_device_data.append(device.device_path) #data collection
			try:
				if device.action == "add":
					for dev in target_device_data:
						splitted = dev.split('/')
						target = splitted[-1]
						if re.match('event[0-9+]',target): #check of event.. param.
							added_dev = str(evdev.InputDevice('/dev/input/{0}'.format(target))).split('/') #data collection about target device
							#print (added_dev)
							#re_addded_dev  = re.findall('.*name ".* Keyboard".*', added_dev[3])
							if re.match('.*name ".* Keyboard".*', added_dev[3]): #check if target device is keyboard
								#print ('Keyboard added')
								return True
			except Exception as e:
				print (e)

while True:
	while not kbdIden():
		if kbdIden():
			print 'Keyboard added'