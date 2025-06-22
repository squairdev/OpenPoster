from PySide6 import QtWidgets, QtGui
import sys
from gui.mainwindow import MainWindow
# when the imposter is sus
# from configparser import ConfigParser
from gui.config_manager import ConfigManager
from PySide6.QtCore import QTranslator
from gui.welcome import WelcomeWindow
import os

# class MyApp(QtWidgets.QApplication):
#     translator: QTranslator

if __name__ == "__main__":
    app = QtWidgets.QApplication([])


    # ─── Localization ───────────────────────────────────
    config = ConfigManager()  
    translator = QTranslator()
    lang = config.get_current_language()
    translator.load(f"languages/app_{lang}.qm")
    app.translator = translator # type: ignore
    app.installTranslator(translator)
    # ────────────────────────────────────────────────────
    
    # ─── Application Properties ─────────────────────────
    app.setApplicationName("OpenPoster")
    app_icon = QtGui.QIcon(":/assets/openposter.ico")
    app.setWindowIcon(app_icon)
    # ─────────────────────────────────────────────────────

    # ─── Global QSS theme ───────────────────────────────
    palette = app.palette()
    text_color = palette.color(QtGui.QPalette.Active, QtGui.QPalette.WindowText)
    is_dark = text_color.lightness() > 128
    qss_file = "themes/dark_style.qss" if is_dark else "themes/light_style.qss"
    qss_path = os.path.join(os.path.dirname(__file__), qss_file)
    if os.path.exists(qss_path):
        try:
            with open(qss_path, "r") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Could not load global QSS '{qss_path}': {e}")
    else:
        print(f"Global QSS file not found: {qss_path}")
    # ────────────────────────────────────────────────────

    # ─── Welcome Window ─────────────────────────────────
    welcome = WelcomeWindow()
    welcome.exec()
    action = getattr(welcome, 'result', None)
    if action is None:
        sys.exit()
    # ────────────────────────────────────────────────────

    # ─── Main Window ────────────────────────────────────
    widget = MainWindow(config, translator)
    widget.resize(1600, 900)
    widget.show()
    widget.config_manager = config
    widget.translator = translator
    # Load or create file after window is shown for correct preview scaling
    if action[0] == "open":
        widget.openFile()
    elif action[0] == "new":
        project_root = os.path.dirname(__file__)
        template_path = os.path.join(project_root, "assets", "openposter.ca")
        widget.open_ca_file(template_path)
    # ────────────────────────────────────────────────────

    sys.exit(app.exec())