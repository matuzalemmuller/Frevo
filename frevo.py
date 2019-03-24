import AppKit
import sys
from tray_icon import TrayIcon
from Foundation import NSUserDefaults

# To hide app from Mac dock
# info = AppKit.NSBundle.mainBundle().infoDictionary()
# info["LSBackgroundOnly"] = "1"

# Detects if OSX is in dark mode to choose icon color
mode=NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle')
if mode == "Dark":
    icon = "icon/logo-white.png"
else:
    icon = "icon/logo-black.png"

# Creates tray icon
app = TrayIcon(icon)
app.exec_()
app.setQuitOnLastWindowClosed(False)

sys.exit(app.exec_())