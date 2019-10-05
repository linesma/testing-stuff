#!/usr/bin/python3

import os
from distutils.core import setup

setup(name="manjaroptimusindicator",
      version="0.9.0",
      description="Manjaro-Optimus Application Indicator",
      url='https://github.com/linesma/manjaroptimus-appindicator',
      author='Mark Lines',
      license='GPLv3',
      packages=["manjaroptimusindicator"],
      data_files=[
          ('/usr/share/icons/hicolor/symbolic/apps/', ['icons/manjaroptimus-symbolic.svg', 'icons/manjaroptimus-intel-symbolic.svg', 'icons/manjaroptimus-nvidia-symbolic.svg']),
          ('/usr/share/manjaroptimus-appindicator/scripts/', ['scripts/pkexec_nvidia', 'scripts/pkexec_intel']),
          ('/usr/local/bin/', ['gnome-script/set-intel', 'gnome-script/set-nvidia']),
          ('/usr/share/polkit-1/actions/', ['pkexec/org.freedesktop.policykit.set-intel.sh.policy', 'pkexec/org.freedesktop.policykit.set-nvidia.sh.policy']),
          ('/etc/xdg/autostart/', ['manjaroptimus-appindicator.desktop'])],
      scripts=["bin/manjaroptimus-appindicator"]
)

os.chmod ('/etc/xdg/autostart/manjaroptimus-appindicator.desktop', 0o755, '/usr/bin/manjaroptimus-appindicator', 0o755, '/usr/share/manjaroptimus-appindicator/scripts/scripts/pkexec_nvidia.sh', 0o755, '/usr/share/manjaroptimus-appindicator/scripts/scripts/pkexec_intel.sh', 0o755, '/usr/local/bin/set-intel.sh', 0o755, '/usr/local/bin/set-nvidia.sh', 0o755)

