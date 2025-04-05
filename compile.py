from sys import platform

import PyInstaller.__main__

args = [
    'app.py',
    '--onedir',
    '--noconfirm',
    '--name=OpenPoster',
    '--optimize=2'
]

if platform == "darwin":
    # add --windowed arg for macOS
    args.append('--windowed')
    args.append('--icon=assets/openposter.icns')
elif platform == "win32":
    args.append('--icon=assets/openposter.ico')

PyInstaller.__main__.run(args)
