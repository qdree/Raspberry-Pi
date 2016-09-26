import pyudev 
import evdev 
import functools
import re

target_device_data = [] #list to store recieved data about device

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem = 'input')

monitor.start()

while True:
	for device in iter(functools.partial(monitor.poll, 0), None):
		#print ('{0.action} on {0.device_path}'.format(device))
		#print (type(device.action))

		target_device_data.append(device.device_path) #data collection /// need improvement as statement to block list overloading
		try:
			if device.action == "add":
				for dev in target_device_data:
					splitted = dev.split('/')
					target = splitted[-1]
					if re.match('event[0-9+]',target):
						added_dev = str(evdev.InputDevice('/dev/input/{0}'.format(target))).split('/')
						#print (added_dev)
						#re_addded_dev  = re.findall('.*name ".* Keyboard".*', added_dev[3])
						if re.match('.*name ".* Keyboard".*', added_dev[3]):
							print ('Keyboard added')
		except Exception as e:
			print (e)
	#collected data output