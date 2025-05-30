from pynput import keyboard
from gui import SettingsGUI
from settings import Settings
from window_manager import WindowManager
from network_manager import NetworkManager
from logger import setup_logger
import ctypes
import sys
import os
#
def is_admin():
       try:
           return ctypes.windll.shell32.IsUserAnAdmin()
       except:
           return False

def run_as_admin():
       if not is_admin():
           ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
           sys.exit()

class HotkeyClient:
       def __init__(self):
           self.settings = Settings()
           self.logger = setup_logger()
           self.network_manager = NetworkManager(self.settings)
           self.window_manager = WindowManager(self.settings)
           self.is_hidden = False
           self.ctrl_pressed = False
           self.alt_pressed = False
           self.shift_pressed = False
           self.m_pressed = False
           self.one_pressed = False
           self.active_keys = set()

       def on_menu_hotkey(self):
           print("Menu hotkey triggered: Ctrl+Shift+M")
           self.logger.info("Menu hotkey triggered: Ctrl+Shift+M")
           SettingsGUI(self.settings).run()

       def on_hide_hotkey(self):
           print(f"Hide/Show hotkey triggered: Alt+1 (is_hidden: {self.is_hidden})")
           self.logger.info(f"Hide/Show hotkey triggered: Alt+1 (is_hidden: {self.is_hidden})")
           if not self.is_hidden:
               self.window_manager.hide_windows()
               self.network_manager.disable_network()
               self.is_hidden = True
           else:
               self.window_manager.restore_windows()
               self.network_manager.enable_network()
               self.is_hidden = False

       def on_press(self, key):
           try:
               print(f"Key pressed: {key}")
               self.logger.info(f"Key pressed: {key}")
               # 检测按下的键
               if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                   self.ctrl_pressed = True
                   self.active_keys.add('ctrl')
               elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                   self.alt_pressed = True
                   self.active_keys.add('alt')
               elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                   self.shift_pressed = True
                   self.active_keys.add('shift')
               elif hasattr(key, 'vk') and key.vk == 77:  # M 键的键码
                   self.m_pressed = True
                   self.active_keys.add('m')
               elif hasattr(key, 'vk') and key.vk == 49:  # 1 键的键码
                   self.one_pressed = True
                   self.active_keys.add('1')

               # 调试 active_keys
               print(f"Active keys: {self.active_keys}")
               self.logger.info(f"Active keys: {self.active_keys}")

               # 检查 Ctrl + Shift + M
               if self.ctrl_pressed and self.shift_pressed and self.m_pressed:
                   print(f"Ctrl+Shift+M condition: {self.active_keys == {'ctrl', 'shift', 'm'}}")
                   self.logger.info(f"Ctrl+Shift+M condition: {self.active_keys == {'ctrl', 'shift', 'm'}}")
                   if self.active_keys == {'ctrl', 'shift', 'm'}:
                       self.on_menu_hotkey()
                   self.m_pressed = False
                   self.active_keys.discard('m')

               # 检查 Alt + 1
               if self.alt_pressed and self.one_pressed and not self.ctrl_pressed:
                   print(f"Alt+1 condition: {self.active_keys == {'alt', '1'}}")
                   self.logger.info(f"Alt+1 condition: {self.active_keys == {'alt', '1'}}")
                   if self.active_keys == {'alt', '1'}:
                       self.on_hide_hotkey()
                   self.one_pressed = False
                   self.active_keys.discard('1')

           except AttributeError:
               pass

       def on_release(self, key):
           try:
               print(f"Key released: {key}")
               self.logger.info(f"Key released: {key}")
               if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                   self.ctrl_pressed = False
                   self.active_keys.discard('ctrl')
               elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                   self.alt_pressed = False
                   self.active_keys.discard('alt')
               elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                   self.shift_pressed = False
                   self.active_keys.discard('shift')
               elif hasattr(key, 'vk') and key.vk == 77:
                   self.m_pressed = False
                   self.active_keys.discard('m')
               elif hasattr(key, 'vk') and key.vk == 49:
                   self.one_pressed = False
                   self.active_keys.discard('1')
               print(f"Active keys after release: {self.active_keys}")
               self.logger.info(f"Active keys after release: {self.active_keys}")
           except AttributeError:
               pass

       def start(self):
           print("Starting hotkey listener...")
           self.logger.info("Starting hotkey listener...")
           with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
               listener.join()

if __name__ == '__main__':
       run_as_admin()
       client = HotkeyClient()
       client.start()