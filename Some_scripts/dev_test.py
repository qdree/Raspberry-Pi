import pyudev


try:
	import glib
except:
	from gi.repository import GLib

try:
    from pyudev.glib import MonitorObserver

    def device_event(observer, device):
        print ('event {0} on device {1}'.format(device.action, device))
except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

    def device_event(observer, action, device):
        print ('event {0} on device {1}'.format(action, device))




context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)

monitor.filter_by(subsystem='input')
observer = MonitorObserver(monitor)

observer.connect('device-event', device_event)

monitor.start()

glib.MainLoop().run()