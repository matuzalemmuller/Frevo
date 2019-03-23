import AppKit
import sys
from tray_icon import TrayIcon

# To hide app from Mac dock
# info = AppKit.NSBundle.mainBundle().infoDictionary()
# info["LSBackgroundOnly"] = "1"

app = TrayIcon()
app.exec_()
app.setQuitOnLastWindowClosed(False)

sys.exit(app.exec())