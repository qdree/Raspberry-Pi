import pyudev 
import evdev 
import functools

target_device_data = [] #list to store recieved data about device

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem = 'input')

monitor.start()

while True:
	for device in iter(functools.partial(monitor.poll, 0), None):
		print ('{0.action} on {0.device_path}'.format(device))
		print (type(device.device_path))

		target_device_data.append(device.device_path) #data collection /// need improvement as statement to block list overloading
	#collected data output