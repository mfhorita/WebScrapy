# PyInstaller para Python inferior a v3.3   (PyInstaller Scrapy.py)
    # Py2Exe para Python v3.3 ou v3.4           (Python setup.py py2exe)
# cx_Freeze para Python superior a v3.4     (Python setup.py build)
import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"excludes":["tkinter", "tk", "jupyter", "lxml"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='Scrapy',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Marcelo Horita',
    author_email='',
    options = {"build_exe": build_exe_options},
    description='Web Scraping - Site Anbima - VNA NTN-B, NTN-C e LFT',
    executables=[Executable(script='Scrapy.py', base=base, icon='document.ico')]
)