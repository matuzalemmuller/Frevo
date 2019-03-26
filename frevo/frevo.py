import AppKit
import sys
from Foundation import NSUserDefaults
from tray_icon import TrayIcon
from file_handler import ConfigHandler

# Detects if OSX is in dark mode to choose icon color
mode=NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle')

if ConfigHandler().isApp():
    if mode == "Dark":
        icon = "icon/logo-white.png"
    else:
        icon = "icon/logo-black.png"
    icon = ConfigHandler().resourcePath(icon)
else:
    if mode == "Dark":
        icon = "../icon/logo-white.png"
    else:
        icon = "../icon/logo-black.png"

# Creates tray icon
app = TrayIcon(icon)
app.exec_()
app.setQuitOnLastWindowClosed(False)

sys.exit(app.exec_())