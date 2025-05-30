import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
from logger import setup_logger
from settings import Settings

class TestService(win32serviceutil.ServiceFramework):
      _svc_name_ = "TestService"
      _svc_display_name_ = "Test Service"
      _svc_description_ = "A minimal test service"

      def __init__(self, args):
          self.debug_log = r"B:\stealth_app\logs\test_debug.log"
          with open(self.debug_log, "a") as f:
              f.write("Initializing TestService...\n")
          win32serviceutil.ServiceFramework.__init__(self, args)
          self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
          with open(self.debug_log, "a") as f:
              f.write("Creating logger...\n")
          self.logger = setup_logger()
          with open(self.debug_log, "a") as f:
              f.write("Logger created successfully\n")
          self.settings = Settings()
          with open(self.debug_log, "a") as f:
              f.write("Settings loaded successfully\n")
          with open(self.debug_log, "a") as f:
              f.write("TestService initialized\n")

      def SvcStop(self):
          with open(self.debug_log, "a") as f:
              f.write("Stopping TestService...\n")
          self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
          win32event.SetEvent(self.hWaitStop)

      def SvcDoRun(self):
          with open(self.debug_log, "a") as f:
              f.write("Starting TestService...\n")
          servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                (self._svc_name_, ''))
          self.logger.info("TestService started")
          win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
          with open(self.debug_log, "a") as f:
              f.write("TestService stopped\n")

if __name__ == '__main__':
      if len(sys.argv) == 1:
          servicemanager.Initialize()
          servicemanager.PrepareToHostSingle(TestService)
          servicemanager.StartServiceCtrlDispatcher()
      else:
          win32serviceutil.HandleCommandLine(TestService)