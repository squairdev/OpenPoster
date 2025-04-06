from sys import platform

import PyInstaller.__main__

args = [
    'app.py',
    '--onedir',
    '--noconfirm',
    '--name=OpenPoster',
    '--optimize=2'
]

# for some stupid reason it couldn't find pyside6 for me - anh
hacks = [
    '--hidden-import=PySide6.QtCore',
    '--hidden-import=PySide6.QtWidgets',
    '--hidden-import=PySide6.QtGui',
    '--collect-submodules=PySide6',
    '--collect-data=PySide6'
]
# args.extend(hacks)

if platform == "darwin":
    # add --windowed arg for macOS
    args.append('--windowed')
    args.append('--icon=assets/openposter.icns')
elif platform == "win32":
    args.append('--icon=assets/openposter.ico')

PyInstaller.__main__.run(args)
