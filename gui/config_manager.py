import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(Path.home(), ".openposter")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "ui": {
                "splitters": {
                    "mainSplitter": [],
                    "layersSplitter": []
                },
                "window": {
                    "size": [1200, 800],
                    "position": [100, 100],
                    "maximized": False,
                    "remember_size": True
                }
            },
            "shortcuts": {
                "export": "Ctrl+E",
                "zoom_in": "Ctrl+=",
                "zoom_out": "Ctrl+-"
            },
            "nugget": {
                "exe_path": "",
                "open_after_export": False
            }
        }
        self.config = {}
        self.ensure_config_dir()
        self.load_config()
    
    def ensure_config_dir(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    
                self.ensure_default_keys()
            else:
                self.config = self.default_config.copy()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self.default_config.copy()
    
    def ensure_default_keys(self):
        def update_nested_dict(d, u):
            for k, v in u.items():
                if k not in d:
                    d[k] = v
                elif isinstance(v, dict) and isinstance(d[k], dict):
                    update_nested_dict(d[k], v)
        
        update_nested_dict(self.config, self.default_config)
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_splitter_sizes(self, splitter_name):
        try:
            return self.config.get("ui", {}).get("splitters", {}).get(splitter_name, [])
        except:
            return []
    
    def save_splitter_sizes(self, splitter_name, sizes):
        if "ui" not in self.config:
            self.config["ui"] = {}
        if "splitters" not in self.config["ui"]:
            self.config["ui"]["splitters"] = {}
        
        self.config["ui"]["splitters"][splitter_name] = sizes
        self.save_config()
    
    def get_window_geometry(self):
        try:
            window = self.config.get("ui", {}).get("window", {})
            return {
                "size": window.get("size", self.default_config["ui"]["window"]["size"]),
                "position": window.get("position", self.default_config["ui"]["window"]["position"]),
                "maximized": window.get("maximized", self.default_config["ui"]["window"]["maximized"]),
                "remember_size": window.get("remember_size", self.default_config["ui"]["window"]["remember_size"])
            }
        except:
            return {
                "size": self.default_config["ui"]["window"]["size"],
                "position": self.default_config["ui"]["window"]["position"],
                "maximized": self.default_config["ui"]["window"]["maximized"],
                "remember_size": self.default_config["ui"]["window"]["remember_size"]
            }
    
    def save_window_geometry(self, size, position, maximized):
        if "ui" not in self.config:
            self.config["ui"] = {}
        if "window" not in self.config["ui"]:
            self.config["ui"]["window"] = {}
        
        remember = self.config["ui"]["window"].get("remember_size", True)
        if remember:
            self.config["ui"]["window"]["size"] = size
            self.config["ui"]["window"]["position"] = position
            self.config["ui"]["window"]["maximized"] = maximized
            self.save_config()
    
    def set_remember_window_size(self, remember):
        if "ui" not in self.config:
            self.config["ui"] = {}
        if "window" not in self.config["ui"]:
            self.config["ui"]["window"] = {}
        
        self.config["ui"]["window"]["remember_size"] = remember
        self.save_config()
    
    def reset_to_defaults(self):
        self.config = self.default_config.copy()
        self.save_config()

    # Nugget Stuff
    def get_nugget_exec_path(self):
        """Get the configured path to the Nugget executable."""
        return self.config.get("nugget", {}).get("exe_path", "")

    def set_nugget_exec_path(self, path):
        """Set the path to the Nugget executable."""
        if "nugget" not in self.config:
            self.config["nugget"] = {}
        self.config["nugget"]["exe_path"] = path
        self.save_config()

    def get_open_in_nugget(self):
        """Return whether to open exported file in Nugget automatically."""
        return self.config.get("nugget", {}).get("open_after_export", False)

    def set_open_in_nugget(self, open_after):
        """Set whether to open exported file in Nugget automatically."""
        if "nugget" not in self.config:
            self.config["nugget"] = {}
        self.config["nugget"]["open_after_export"] = open_after
        self.save_config()

    def get_export_shortcut(self):
        return self.config.get("shortcuts", {}).get("export", "Ctrl+E")

    def set_export_shortcut(self, sequence):
        if "shortcuts" not in self.config:
            self.config["shortcuts"] = {}
        self.config["shortcuts"]["export"] = sequence
        self.save_config()

    def get_zoom_in_shortcut(self):
        return self.config.get("shortcuts", {}).get("zoom_in", "Ctrl+=")

    def set_zoom_in_shortcut(self, seq):
        if "shortcuts" not in self.config:
            self.config["shortcuts"] = {}
        self.config["shortcuts"]["zoom_in"] = seq
        self.save_config()

    def get_zoom_out_shortcut(self):
        return self.config.get("shortcuts", {}).get("zoom_out", "Ctrl+-")

    def set_zoom_out_shortcut(self, seq):
        if "shortcuts" not in self.config:
            self.config["shortcuts"] = {}
        self.config["shortcuts"]["zoom_out"] = seq
        self.save_config() 