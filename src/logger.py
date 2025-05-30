import os
import sys
from datetime import datetime

class SimpleLogger:
       def __init__(self):
           # 使用 %USERPROFILE% 目录存储日志
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
           self.log_path = os.path.join(base_dir, 'logs', 'app.log')
           self.debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           try:
               os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
               with open(self.debug_log_path, 'a') as f:
                   f.write(f"SimpleLogger initialized at: {self.log_path}\n")
                   f.flush()
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to initialize logger: {str(e)}\n")
                   f.flush()

       def info(self, message):
           timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           log_line = f"{timestamp} - INFO - {message}\n"
           try:
               with open(self.log_path, 'a') as f:
                   f.write(log_line)
                   f.flush()
               with open(self.debug_log_path, 'a') as f:
                   f.write(log_line)
                   f.flush()
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to write info log: {str(e)}\n")
                   f.flush()

       def error(self, message):
           timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           log_line = f"{timestamp} - ERROR - {message}\n"
           try:
               with open(self.log_path, 'a') as f:
                   f.write(log_line)
                   f.flush()
               with open(self.debug_log_path, 'a') as f:
                   f.write(log_line)
                   f.flush()
           except Exception as e:
               with open(self.error_log_path, 'a') as f:
                   f.write(f"Failed to write error log: {str(e)}\n")
                   f.flush()

def setup_logger():
       return SimpleLogger()