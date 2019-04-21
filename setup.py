import sys

from cx_Freeze import setup, Executable

# cx_Freeze options, see documentation.
build_exe_options = {
    'packages': ['cffi', 'numpy'],
    'excludes': [],
    'include_files': ['src/data'],
}

# Hide the terminal on Windows apps.
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='Critical Keep',
    options={'build_exe': build_exe_options},
    executables=[Executable('src/engine.py', base=base, targetName='critical_keep.exe')],
)
