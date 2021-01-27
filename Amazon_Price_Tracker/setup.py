from setuptools import setup

APP = ['amazon.py']
DATA_FILES = ['gui/amazonGUI.py']
OPTIONS = {
#  'iconfile':'logoapp.icns',
 'argv_emulation': True,
 'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)