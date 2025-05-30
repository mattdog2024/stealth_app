import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
import traceback
from network_manager import NetworkManager
from window_manager import WindowManager
from settings import Settings
from logger import setup_logger

class StealthService(win32serviceutil.ServiceFramework):
       _svc_name_ = "StealthAppService"
       _svc_display_name_ = "System Config Service"
       _svc_description_ = "System configuration utility"

       def __init__(self, args):
           # 动态计算项目根目录
           if getattr(sys, 'frozen', False):
               base_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               base_dir = os.path.dirname(script_dir)
           debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           with open(debug_log_path, 'a') as f:
               f.write("Initializing StealthService...\n")
               f.flush()
           try:
               win32serviceutil.ServiceFramework.__init__(self, args)
               self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
               with open(debug_log_path, 'a') as f:
                   f.write("Creating logger...\n")
                   f.flush()
               self.logger = setup_logger()
               self.logger.info("Logger initialized in service")
               with open(debug_log_path, 'a') as f:
                   f.write("Logger created successfully\n")
                   f.flush()
               self.settings = Settings()
               self.network_manager = NetworkManager(self.settings)
               self.window_manager = WindowManager(self.settings)
               with open(debug_log_path, 'a') as f:
                   f.write("Service initialization complete\n")
                   f.flush()
               self.logger.info("Service initialization complete")
           except Exception as e:
               with open(debug_log_path, 'a') as f:
                   f.write(f"Error during initialization: {str(e)}\n")
                   f.write(traceback.format_exc() + "\n")
                   f.flush()
               raise

       def SvcStop(self):
           if getattr(sys, 'frozen', False):
               base_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               base_dir = os.path.dirname(script_dir)
           debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           with open(debug_log_path, 'a') as f:
               f.write("Stopping service...\n")
               f.flush()
           try:
               self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
               win32event.SetEvent(self.hWaitStop)
               with open(debug_log_path, 'a') as f:
                   f.write("Stop signal sent\n")
                   f.flush()
           except Exception as e:
               with open(debug_log_path, 'a') as f:
                   f.write(f"Error during SvcStop: {str(e)}\n")
                   f.write(traceback.format_exc() + "\n")
                   f.flush()
               raise

       def SvcDoRun(self):
           if getattr(sys, 'frozen', False):
               base_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               base_dir = os.path.dirname(script_dir)
           debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           with open(debug_log_path, 'a') as f:
               f.write("Starting service...\n")
               f.flush()
           try:
               servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                     servicemanager.PYS_SERVICE_STARTED,
                                     (self._svc_name_, ''))
               self.logger.info("Service started in SvcDoRun")
               with open(debug_log_path, 'a') as f:
                   f.write("Service started in SvcDoRun\n")
                   f.flush()
               self.main()
           except Exception as e:
               with open(debug_log_path, 'a') as f:
                   f.write(f"Error during SvcDoRun: {str(e)}\n")
                   f.write(traceback.format_exc() + "\n")
                   f.flush()
               raise

       def main(self):
           if getattr(sys, 'frozen', False):
               base_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               base_dir = os.path.dirname(script_dir)
           debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           with open(debug_log_path, 'a') as f:
               f.write("Entering main loop...\n")
               f.flush()
           try:
               self.logger.info("Service started - main loop entry")
               with open(debug_log_path, 'a') as f:
                   f.write("Service started - main loop entry\n")
                   f.flush()
               win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
               with open(debug_log_path, 'a') as f:
                   f.write("Exiting main loop...\n")
                   f.flush()
               self.logger.info("Service stopped")
           except Exception as e:
               with open(debug_log_path, 'a') as f:
                   f.write(f"Error in main loop: {str(e)}\n")
                   f.write(traceback.format_exc() + "\n")
                   f.flush()
               raise

if __name__ == '__main__':
       try:
           if len(sys.argv) == 1:
               servicemanager.Initialize()
               servicemanager.PrepareToHostSingle(StealthService)
               servicemanager.StartServiceCtrlDispatcher()
           else:
               win32serviceutil.HandleCommandLine(StealthService)
       except Exception as e:
           if getattr(sys, 'frozen', False):
               base_dir = os.path.dirname(os.path.abspath(sys.executable))
           else:
               script_dir = os.path.dirname(os.path.abspath(__file__))
               base_dir = os.path.dirname(script_dir)
           debug_log_path = os.path.join(base_dir, 'logs', 'debug.log')
           with open(debug_log_path, 'a') as f:
               f.write(f"Error in main execution: {str(e)}\n")
               f.write(traceback.format_exc() + "\n")
               f.flush()