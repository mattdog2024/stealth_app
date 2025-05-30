import win32gui
import win32con
import psutil
from logger import setup_logger

class WindowManager:
       def __init__(self, settings):
           self.settings = settings
           self.logger = setup_logger()
           self.hidden_windows = []

       def enum_windows(self, hwnd, results):
           if win32gui.IsWindowVisible(hwnd):
               title = win32gui.GetWindowText(hwnd)
               for app in self.settings.get('target_apps', []):
                   if app['title'] in title or app['process'] in title.lower():
                       results.append(hwnd)

       def hide_windows(self):
           self.hidden_windows = []
           win32gui.EnumWindows(self.enum_windows, self.hidden_windows)
           for hwnd in self.hidden_windows:
               win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
               self.logger.info(f"Hidden window: {win32gui.GetWindowText(hwnd)}")

       def restore_windows(self):
           for hwnd in self.hidden_windows:
               win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
               self.logger.info(f"Restored window: {win32gui.GetWindowText(hwnd)}")
           self.hidden_windows = []