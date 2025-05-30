import json
import os
import sys

class Settings:
       def __init__(self):
           # 使用 %USERPROFILE% 目录存储配置文件
           userprofile_dir = os.getenv('USERPROFILE')
           if not userprofile_dir:
               userprofile_dir = os.path.expanduser("~")
           base_dir = os.path.join(userprofile_dir, 'StealthApp')
           # 程序所在目录，用于临时错误日志
           if getattr(sys, 'frozen', False):
               exe_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               exe_dir = os.path.dirname(script_dir)
           self.error_log_path = os.path.join(exe_dir, 'error.log')
           self.config_path = os.path.join(base_dir, 'config', 'settings.json')
           self.debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           # 确保 self.settings 始终初始化
           self.settings = {}
           try:
               os.makedirs(os.path.dirname(self.debug_log_path), exist_ok=True)
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"Config path resolved to: {self.config_path}\n")
                   f.flush()
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to write debug log: {e}\n")
                   f.flush()
           # 加载设置
           self.load_settings()

       def load_settings(self):
           try:
               if os.path.exists(self.config_path):
                   with open(self.config_path, 'r', encoding='utf-8') as f:
                       self.settings = json.load(f)
                       with open(self.debug_log_path, 'a') as f:
                           f.write(f"Loaded settings: {self.settings}\n")
                           f.flush()
                       print(f"Loaded settings: {self.settings}")
                       return
               with open(self.debug_log_path, 'a') as f:
                   f.write("No config file found, starting with empty settings\n")
                   f.flush()
               print("No config file found, starting with empty settings")
               self.settings = {}
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to load settings: {e}\n")
                   f.flush()
               print(f"Failed to load settings: {e}")
               self.settings = {}

       def save(self):
           try:
               os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"Attempting to save settings: {self.settings}\n")
                   f.flush()
               print(f"Attempting to save settings: {self.settings}")
               with open(self.config_path, 'w', encoding='utf-8') as f:
                   json.dump(self.settings, f, indent=4, ensure_ascii=False)
                   f.flush()
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"Settings saved to {self.config_path}: {self.settings}\n")
                   f.flush()
               print(f"Settings saved to {self.config_path}: {self.settings}")
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to save settings: {e}\n")
                   f.flush()
               print(f"Failed to save settings: {e}")
               raise

       def get(self, key, default=None):
           value = self.settings.get(key, default)
           try:
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"Getting key '{key}': {value}\n")
                   f.flush()
               print(f"Getting key '{key}': {value}")
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to write debug log in get: {e}\n")
                   f.flush()
           return value

       def set(self, key, value):
           self.settings[key] = value
           try:
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"Setting key '{key}' to: {value}\n")
                   f.flush()
               print(f"Setting key '{key}' to: {value}")
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to write debug log in set: {e}\n")
                   f.flush()