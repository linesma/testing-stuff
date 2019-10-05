import gi
from gi.repository import Notify as notify

intel_notif = ('Switching to the Intel iGPU')
reboot_notif = ('Please reboot for changes to take effect')

notify.init("App Name")
notify.Notification.new(intel_notif, reboot_notif, '/usr/share/icons/hicolor/symbolic/apps/manjaroptimus-intel-symbolic.svg').show()