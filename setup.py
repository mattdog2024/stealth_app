from setuptools import setup

setup(
    name="StealthApp",
    version="1.0",
    description="Stealth application for Windows",
    author="xAI",
    packages=['src'],
    install_requires=[
        'pywin32==306',
        'psutil==5.9.8',
        'pynput==1.7.6',
        'pyinstaller==5.13.2'
    ]
)