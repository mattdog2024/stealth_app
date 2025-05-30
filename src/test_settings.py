from settings import Settings

def test_save():
       settings = Settings()
       settings.set('test_key', 'test_value')
       settings.set('target_apps', [{'title': 'notepad.exe', 'process': 'notepad.exe'}])
       settings.save()
       print("Test save completed")

if __name__ == '__main__':
       test_save()