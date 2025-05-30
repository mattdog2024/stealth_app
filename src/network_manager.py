import subprocess
import psutil
from logger import setup_logger

class NetworkManager:
       def __init__(self, settings):
           self.settings = settings
           self.logger = setup_logger()
           self.interface_name = self.settings.get('interface_name', '以太网')
           print(f"NetworkManager initialized with interface: {self.interface_name}")

       def set_static_ip(self):
           print("Setting static IP...")
           try:
               cmd = f'netsh interface ip set address name="{self.interface_name}" source=static addr=192.168.1.100 mask=255.255.255.0'
               print(f"Executing command: {cmd}")
               subprocess.run(cmd, shell=True, check=True)
               self.logger.info("Static IP set to 192.168.1.100")
               print("Static IP set successfully")
           except subprocess.CalledProcessError as e:
               self.logger.error(f"Failed to set static IP: {e}")
               print(f"Failed to set static IP: {e}")
               raise

       def disable_network(self):
           print("Disabling network...")
           try:
               subprocess.run(f'netsh interface set interface "{self.interface_name}" admin=disable', shell=True, check=True)
               self.logger.info("Network disabled")
               print("Network disabled successfully")
           except subprocess.CalledProcessError as e:
               self.logger.error(f"Failed to disable network: {e}")
               print(f"Failed to disable network: {e}")

       def enable_network(self):
           print("Enabling network...")
           try:
               subprocess.run(f'netsh interface set interface "{self.interface_name}" admin=enable', shell=True, check=True)
               self.set_static_ip()
               self.logger.info("Network enabled")
               print("Network enabled successfully")
           except subprocess.CalledProcessError as e:
               self.logger.error(f"Failed to enable network: {e}")
               print(f"Failed to enable network: {e}")