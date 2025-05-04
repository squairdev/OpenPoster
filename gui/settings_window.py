from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, QCheckBox, QLineEdit, QFileDialog, QTabWidget, QWidget, QKeySequenceEdit, QMessageBox
from PySide6.QtCore import Qt
import webbrowser
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class SettingsDialog(QDialog):
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Settings")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        tabs = QTabWidget()
        layout.addWidget(tabs)
        # UI Tab
        ui_tab = QWidget()
        ui_layout = QVBoxLayout(ui_tab)
        ui_layout.setAlignment(Qt.AlignTop)
        remember = QLabel("Remember window size and position")
        self.remember_window_checkbox = QCheckBox()
        self.remember_window_checkbox.setChecked(self.config_manager.get_window_geometry()["remember_size"])
        self.remember_window_checkbox.stateChanged.connect(lambda s: self.config_manager.set_remember_window_size(s == Qt.Checked))
        ui_row = QHBoxLayout(); ui_row.addWidget(remember); ui_row.addStretch(); ui_row.addWidget(self.remember_window_checkbox)
        ui_layout.addLayout(ui_row)
        reset_btn = QPushButton("Reset Panels")
        reset_btn.clicked.connect(lambda: [self.config_manager.save_splitter_sizes("mainSplitter", []), self.config_manager.save_splitter_sizes("layersSplitter", []), self.parent().apply_default_sizes()])
        reset_row = QHBoxLayout(); reset_row.addStretch(); reset_row.addWidget(reset_btn)
        ui_layout.addLayout(reset_row)
        tabs.addTab(ui_tab, "UI")
        # Nugget Tab
        nugget_tab = QWidget()
        nugget_layout = QVBoxLayout(nugget_tab)
        nugget_layout.setAlignment(Qt.AlignTop)
        path_lbl = QLabel("Nugget Executable:")
        self.nugget_path_lineedit = QLineEdit(self.config_manager.get_nugget_exec_path())
        browse = QPushButton("Browse")
        browse.clicked.connect(self.browse_nugget_executable)
        path_row = QHBoxLayout(); path_row.addWidget(path_lbl); path_row.addWidget(self.nugget_path_lineedit); path_row.addWidget(browse)
        nugget_layout.addLayout(path_row)
        tabs.addTab(nugget_tab, "Nugget")
        # Shortcuts Tab
        short_tab = QWidget()
        short_layout = QVBoxLayout(short_tab)
        short_layout.setAlignment(Qt.AlignTop)
        notice_lbl = QLabel("Please relaunch the app to apply new shortcuts.")
        notice_lbl.setStyleSheet("font-style: italic; color: gray;")
        short_layout.addWidget(notice_lbl)
        # Export Shortcut
        exp_row = QHBoxLayout()
        exp_lbl = QLabel("Export Shortcut:")
        self.exp_seq = QKeySequenceEdit()
        self.exp_seq.setFocusPolicy(Qt.ClickFocus)
        self.exp_seq.setKeySequence(self.config_manager.get_export_shortcut())
        self.exp_seq.keySequenceChanged.connect(self.on_export_seq_changed)
        exp_reset = QPushButton("Reset")
        exp_reset.clicked.connect(self.reset_export_shortcut)
        exp_row.addWidget(exp_lbl)
        exp_row.addWidget(self.exp_seq)
        exp_row.addWidget(exp_reset)
        short_layout.addLayout(exp_row)
        # Zoom In Shortcut
        zi_row = QHBoxLayout()
        zi_lbl = QLabel("Zoom In Shortcut:")
        self.zi_seq = QKeySequenceEdit()
        self.zi_seq.setFocusPolicy(Qt.ClickFocus)
        self.zi_seq.setKeySequence(self.config_manager.get_zoom_in_shortcut())
        self.zi_seq.keySequenceChanged.connect(self.on_zoom_in_seq_changed)
        zi_reset = QPushButton("Reset")
        zi_reset.clicked.connect(self.reset_zoom_in_shortcut)
        zi_row.addWidget(zi_lbl)
        zi_row.addWidget(self.zi_seq)
        zi_row.addWidget(zi_reset)
        short_layout.addLayout(zi_row)
        # Zoom Out Shortcut
        zo_row = QHBoxLayout()
        zo_lbl = QLabel("Zoom Out Shortcut:")
        self.zo_seq = QKeySequenceEdit()
        self.zo_seq.setFocusPolicy(Qt.ClickFocus)
        self.zo_seq.setKeySequence(self.config_manager.get_zoom_out_shortcut())
        self.zo_seq.keySequenceChanged.connect(self.on_zoom_out_seq_changed)
        zo_reset = QPushButton("Reset")
        zo_reset.clicked.connect(self.reset_zoom_out_shortcut)
        zo_row.addWidget(zo_lbl)
        zo_row.addWidget(self.zo_seq)
        zo_row.addWidget(zo_reset)
        short_layout.addLayout(zo_row)
        # Reset All Shortcuts
        all_reset = QPushButton("Reset All Shortcuts")
        all_reset.clicked.connect(self.reset_all_shortcuts)
        short_layout.addWidget(all_reset)
        tabs.addTab(short_tab, "Shortcuts")
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setContentsMargins(20, 40, 20, 20)
        title_lbl = QLabel("<h2>OpenPoster Beta</h2>")
        version_lbl = QLabel("Version: v0.0.2")
        gui_lbl = QLabel("GUI: PySide6")
        credits_lbl = QLabel("Credits:\nretronbv, enkei64, ItMe12s, superEVILFACE, AnhNguygenlost13, leminlimez")
        credits_lbl.setWordWrap(True)
        website_lbl = QLabel('<a href="https://openposter.pages.dev">openposter.pages.dev</a>')
        website_lbl.setOpenExternalLinks(True)
        license_lbl = QLabel('<a href="https://github.com/openposter/OpenPoster/blob/main/LICENSE">MIT License</a>')
        license_lbl.setOpenExternalLinks(True)
        discord_btn = QPushButton("Join Discord")
        discord_btn.setIcon(QIcon(":/icons/discord.svg"))
        discord_btn.setIconSize(QSize(24, 24))
        discord_btn.clicked.connect(lambda: webbrowser.open("https://discord.gg/t3abQJjHm6"))
        about_layout.addWidget(title_lbl)
        about_layout.addWidget(version_lbl)
        about_layout.addWidget(gui_lbl)
        about_layout.addWidget(credits_lbl)
        about_layout.addWidget(website_lbl)
        about_layout.addWidget(license_lbl)
        about_layout.addWidget(discord_btn)
        tabs.addTab(about_tab, "About")
        layout.setAlignment(tabs, Qt.AlignTop)

    def browse_nugget_executable(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Nugget Executable", "", "Applications (*.app);;Executables (*.exe);;All Files (*)")
        if path:
            self.nugget_path_lineedit.setText(path)
            self.config_manager.set_nugget_exec_path(path) 

    def on_export_seq_changed(self, seq):
        self.config_manager.set_export_shortcut(seq.toString())

    def reset_export_shortcut(self):
        default = self.config_manager.default_config["shortcuts"]["export"]
        self.exp_seq.setKeySequence(default)
        self.config_manager.set_export_shortcut(default)

    def on_zoom_in_seq_changed(self, seq):
        self.config_manager.set_zoom_in_shortcut(seq.toString())

    def reset_zoom_in_shortcut(self):
        default = self.config_manager.default_config["shortcuts"]["zoom_in"]
        self.zi_seq.setKeySequence(default)
        self.config_manager.set_zoom_in_shortcut(default)

    def on_zoom_out_seq_changed(self, seq):
        self.config_manager.set_zoom_out_shortcut(seq.toString())

    def reset_zoom_out_shortcut(self):
        default = self.config_manager.default_config["shortcuts"]["zoom_out"]
        self.zo_seq.setKeySequence(default)
        self.config_manager.set_zoom_out_shortcut(default)

    def reset_all_shortcuts(self):
        defaults = self.config_manager.default_config["shortcuts"]
        self.exp_seq.setKeySequence(defaults["export"])
        self.config_manager.set_export_shortcut(defaults["export"])
        self.zi_seq.setKeySequence(defaults["zoom_in"])
        self.config_manager.set_zoom_in_shortcut(defaults["zoom_in"])
        self.zo_seq.setKeySequence(defaults["zoom_out"])
        self.config_manager.set_zoom_out_shortcut(defaults["zoom_out"]) 