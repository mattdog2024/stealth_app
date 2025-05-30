import tkinter as tk
from tkinter import messagebox
from settings import Settings
from logger import setup_logger

class SettingsGUI:
       def __init__(self, settings):
           self.settings = settings
           self.logger = setup_logger()
           self.root = tk.Tk()
           self.root.title("Settings")
           self.root.geometry("400x300")
           self.setup_widgets()

       def setup_widgets(self):
           tk.Label(self.root, text="Interface Name:").pack()
           self.interface_entry = tk.Entry(self.root)
           self.interface_entry.insert(0, self.settings.get('interface_name', '以太网'))
           self.interface_entry.pack()

           tk.Label(self.root, text="Hide/Show Hotkey (e.g., alt+`):").pack()
           self.hotkey_entry = tk.Entry(self.root)
           self.hotkey_entry.insert(0, self.settings.get('hide_hotkey', '<alt>+<`>'))
           self.hotkey_entry.pack()

           tk.Label(self.root, text="Target App (Title or Process):").pack()
           self.app_entry = tk.Entry(self.root)
           self.app_entry.pack()

           tk.Button(self.root, text="Add App", command=self.add_app).pack()
           tk.Button(self.root, text="Save", command=self.save_settings).pack()

       def add_app(self):
           app = {'title': self.app_entry.get(), 'process': self.app_entry.get().lower()}
           if not app['title']:
               messagebox.showerror("Error", "Target app cannot be empty")
               return
           apps = self.settings.get('target_apps', [])
           print(f"Before adding - Current target_apps: {apps}")
           apps.append(app)
           print(f"After adding - App to add: {app}")
           self.settings.set('target_apps', apps)
           print(f"After set - target_apps in settings: {self.settings.get('target_apps')}")
           try:
               self.settings.save()
               messagebox.showinfo("Success", "App added and saved")
           except Exception as e:
               messagebox.showerror("Error", f"Failed to save app: {str(e)}")

       def save_settings(self):
           self.settings.set('interface_name', self.interface_entry.get())
           modifier_keys = {'ctrl', 'alt', 'shift', 'cmd', 'win'}
           raw_hotkey = self.hotkey_entry.get().strip()
           if raw_hotkey:
               hotkey_parts = raw_hotkey.split('+')
               formatted_parts = []
               for part in hotkey_parts:
                   part = part.strip()
                   if part.lower() in modifier_keys and not (part.startswith('<') and part.endswith('>')):
                       formatted_parts.append(f"<{part}>")
                   elif part.startswith('<') and part.endswith('>') and part[1:-1].lower() in modifier_keys:
                       formatted_parts.append(part)
                   else:
                       formatted_parts.append(part)
               formatted_hotkey = '+'.join(formatted_parts)
               self.settings.set('hide_hotkey', formatted_hotkey)
           else:
               self.settings.set('hide_hotkey', '<alt>+<`>')
           try:
               self.settings.save()
               messagebox.showinfo("Success", "Settings saved")
           except Exception as e:
               messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
           self.root.destroy()

       def run(self):
           self.root.mainloop()