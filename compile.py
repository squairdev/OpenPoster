from sys import platform

import PyInstaller.__main__

args = [
    'app.py',
    '--onedir',
    '--noconfirm',
    '--name=OpenPoster',
    '--icon=assets/openposter.icns',
    '--optimize=2'
]

if platform == "darwin":
    # add --windowed arg for macOS
    args.append('--windowed')

PyInstaller.__main__.run(args)
