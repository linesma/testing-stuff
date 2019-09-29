#!/usr/bin/python3

import os
import signal
import json
import gi
import gettext

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import Gio as gio
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

gettext.bindtextdomain('optimus-switch-indicator', '/usr/share/locale')
gettext.textdomain('optimus-switch-indicator')
_ = gettext.gettext

APPINDICATOR_ID = 'optimus-switch-indicator'

intel_notif = _('Switching to Intel')
nvidia_notif = _('Switching to nVidia')
reboot_notif = _('Please reboot for changes to take effect')
error_head = _('Error occured')

drivers = {
    'nvidia': 'prime-indicator-nvidia-symbolic',
    'intel': 'prime-indicator-nvidia-symbolic',
    'other': 'prime-indicator-symbolic',
}

def curent_driver = get_check_current(drivers):
    # if curent_driver == "other" : exit(1) ??? user not have intel or nvidia, we exit
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()
    import subprocess
    try:
        proc = subprocess.Popen(['glxinfo','-B' ], text=True, stdout = subprocess.PIPE)
    except FileNotFoundError:
        return 'other'  # glxinfo not installed
    output = str(proc.communicate()[0]).split("\n")
    # or we can use `re`
    output = [ s.split(':')[1].strip().lower() for s in output if 'OpenGL vendor string' in s ]
    print(output) # debug
    for s in output:
        # list is not hard coded here, but use keys in array
        print('find', s, 'in', drivers.keys(), "...?" ) # debug
        if s in drivers.keys():
            return s
    return 'other' # not found

def build_menu():
    menu = gtk.Menu()
    if (check_current() != 'nvidia'):
        item_nvidia = gtk.MenuItem.new_with_label(_('Switch to Nvidia'))
        item_nvidia.connect('activate', nvidia)
        menu.append(item_nvidia)
    if (check_current() != 'intel'):
        item_intel = gtk.MenuItem.new_with_label(_('Switch to Intel'))
        item_intel.connect('activate', intel)
        menu.append(item_intel)
    menu.show_all()
    return menu

def nvidia(_):
    result, output, error, status = glib.spawn_command_line_sync('/usr/share/optimus-switch-indicator/scripts/pkexec_nvidia')
    if (error):
        notify.Notification.new(error_head, error.decode("utf-8"), 'dialog-warning').show()
    elif (result):
        notify.Notification.new(nvidia_notif, reboot_notif, 'prime-indicator-nvidia-symbolic').show()
    else:
        notify.Notification.new(error_head, output.decode("utf-8"), 'dialog-warning').show()

def intel(_):
    result, output, error, status = glib.spawn_command_line_sync('/usr/share/optimus-switch-indicator/scripts/pkexec_intel')
    if (error):
        notify.Notification.new(error_head, error.decode("utf-8"), 'dialog-warning').show()
    elif (result):
        notify.Notification.new(intel_notif, reboot_notif, 'prime-indicator-intel-symbolic').show()
    else:
        notify.Notification.new(error_head, output.decode("utf-8"), 'dialog-warning').show()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
