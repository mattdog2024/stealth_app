from pynput import keyboard
from gui import SettingsGUI
from logger import setup_logger
import os

class HotkeyManager:
    def __init__(self, settings, network_manager, window_manager):
        self.settings = settings
        self.network_manager = network_manager
        self.window_manager = window_manager
        self.logger = setup_logger()
        self.is_hidden = False
        debug_log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs', 'debug.log')
        with open(debug_log_path, 'a') as f:
            f.write("HotkeyManager initialized\n")

    def on_menu_hotkey(self):
        debug_log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs', 'debug.log')
        with open(debug_log_path, 'a') as f:
            f.write("Menu hotkey triggered\n")
        SettingsGUI(self.settings).run()

    def on_hide_hotkey(self):
        debug_log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs', 'debug.log')
        with open(debug_log_path, 'a') as f:
            f.write("Hide/Show hotkey triggered\n")
        if not self.is_hidden:
            self.window_manager.hide_windows()
            self.network_manager.disable_network()
            self.is_hidden = True
        else:
            self.window_manager.restore_windows()
            self.network_manager.enable_network()
            self.is_hidden = False

    def start(self):
        debug_log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs', 'debug.log')
        with open(debug_log_path, 'a') as f:
            f.write("Starting hotkey listener...\n")
        try:
            with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+m': self.on_menu_hotkey,
                self.settings.get('hide_hotkey', '<ctrl>+<alt>+h>'): self.on_hide_hotkey
            }) as h:
                with open(debug_log_path, 'a') as f:
                    f.write("Hotkey listener started\n")
                h.join()
        except Exception as e:
            with open(debug_log_path, 'a') as f:
                f.write(f"Error in hotkey listener: {str(e)}\n")
            raise