import os
import sys
import shutil
import tempfile
import webbrowser
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QWidget, QHBoxLayout, QLabel, QComboBox, QTreeWidgetItem
from PySide6.QtCore import QStandardPaths, QProcess, Qt
from PySide6.QtGui import QPixmap
from lib.ca_elements.core.cafile import CAFile
from lib.ca_elements.core.calayer import CALayer
from .exportoptions_window import ExportOptionsDialog

class FileOperationsMixin:
    def openFile(self):
        self.ui.treeWidget.clear()
        self.ui.statesTreeWidget.clear()
        if sys.platform == "darwin":
            self.cafilepath = QFileDialog.getOpenFileName(
                self, "Select File", "", "All Supported Files (*.ca *.tendies);;Core Animation Files (*.ca);;Tendies Bundle (*.tendies)")[0]
        else:
            self.cafilepath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if self.cafilepath:
            if self.cafilepath.lower().endswith('.tendies'):
                self.open_tendies_file(self.cafilepath)
            else:
                self.open_ca_file(self.cafilepath)
        
        self.updateFilenameDisplay()

    def open_tendies_file(self, path):
        try:
            temp_dir = tempfile.mkdtemp()

            temp_zip = os.path.join(temp_dir, "temp.zip")
            shutil.copy2(path, temp_zip)

            shutil.unpack_archive(temp_zip, temp_dir, 'zip')

            ca_files = []
            for root, _, files in os.walk(temp_dir):
                for dirname in os.listdir(root):
                    if os.path.isdir(os.path.join(root, dirname)) and dirname.endswith('.ca'):
                        ca_files.append(os.path.join(root, dirname))
                    elif dirname.endswith('.wallpaper'):
                        wallpaper_dir = os.path.join(root, dirname)
                        for ca_dir in os.listdir(wallpaper_dir):
                            if ca_dir.endswith('.ca') and os.path.isdir(os.path.join(wallpaper_dir, ca_dir)):
                                ca_files.append(os.path.join(wallpaper_dir, ca_dir))
            
            if not ca_files:
                raise Exception("No .ca files found in the .tendies file")
            
            if len(ca_files) == 1:
                self.open_ca_file(ca_files[0])
                self.tendies_path = path
                self.ca_files_in_tendies = ca_files
                self.current_ca_index = 0
                # Store temporary directory for cleanup later
                self.tendies_temp_dir = temp_dir
                return
            
            selected_file, ok = QInputDialog.getItem(
                self, "Select .ca File", "Select a .ca file to open:", 
                [os.path.basename(f) for f in ca_files], 0, False)
            
            if ok and selected_file:
                selected_index = [os.path.basename(f) for f in ca_files].index(selected_file)
                self.open_ca_file(ca_files[selected_index])
                self.tendies_path = path
                self.ca_files_in_tendies = ca_files
                self.current_ca_index = selected_index
                
                self.tendies_temp_dir = temp_dir
                
                self.setupCaFileSelector()
            else:
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open .tendies file: {e}")
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir)

    def setupCaFileSelector(self):
        if not hasattr(self, 'ca_files_in_tendies') or not self.ca_files_in_tendies:
            return
            
        if hasattr(self, 'ca_file_selector_widget'):
            self.ui.horizontalLayout_header.removeWidget(self.ca_file_selector_widget)
            self.ca_file_selector_widget.deleteLater()
            
        self.ca_file_selector_widget = QWidget()
        selector_layout = QHBoxLayout(self.ca_file_selector_widget)
        selector_layout.setContentsMargins(5, 0, 5, 0)
        
        selector_label = QLabel("CA File:")
        selector_layout.addWidget(selector_label)
        
        self.ca_file_selector = QComboBox()
        self.ca_file_selector.addItems([os.path.basename(f) for f in self.ca_files_in_tendies])
        self.ca_file_selector.setCurrentIndex(self.current_ca_index)
        self.ca_file_selector.currentIndexChanged.connect(self.switchCaFile)
        selector_layout.addWidget(self.ca_file_selector)
        
        self.ui.horizontalLayout_header.insertWidget(3, self.ca_file_selector_widget)

    def switchCaFile(self, index):
        if not hasattr(self, 'ca_files_in_tendies') or index >= len(self.ca_files_in_tendies):
            return
            
        if getattr(self, 'isDirty', False):
            msg = QMessageBox()
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Would you like to save before switching files?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Yes)
            pix = QPixmap(":/assets/openposter.png")
            msg.setIconPixmap(pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            reply = msg.exec()
            
            if reply == QMessageBox.Cancel:
                self.ca_file_selector.blockSignals(True)
                self.ca_file_selector.setCurrentIndex(self.current_ca_index)
                self.ca_file_selector.blockSignals(False)
                return
            
            if reply == QMessageBox.Yes:
                self.saveFile()
        
        self.current_ca_index = index
        self.open_ca_file(self.ca_files_in_tendies[index])

    def open_ca_file(self, path):
        try:
            ca_file = CAFile(path)
            self.cafile = ca_file
            self.cafilepath = path
            
            if hasattr(self, '_assets'):
                self._assets.cafilepath = self.cafilepath
                self._assets.cachedImages = self.cachedImages
            
            self.populateLayersTreeWidget()
            self.populateStatesTreeWidget()
            self.renderPreview(self.cafile.rootlayer)
            self.fitPreviewToView()
            self.isDirty = False
            self.ui.addButton.setEnabled(True)
            self.updateFilenameDisplay()

            if hasattr(self, '_assets'):
                self.cachedImages = self._assets.cachedImages
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")
            self.markDirty()
    
    def saveFile(self):
        if not hasattr(self, 'cafile') or not self.cafile:
            QMessageBox.warning(self, "Save Error", "No file is open to save.")
            return False
        
        if hasattr(self, 'tendies_temp_dir') and self.tendies_temp_dir:
            try:
                dest, name = os.path.split(self.cafilepath)
                self.cafile.write_file(name, dest)
                self.statusBar().showMessage(f"File saved to {os.path.basename(self.cafilepath)}", 3000)
                self.isDirty = False
                return True
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save file to {self.cafilepath}:\n{e}")
                return False
        
        if hasattr(self, 'cafilepath') and self.cafilepath:
            try:
                dest, name = os.path.split(self.cafilepath)
                self.cafile.write_file(name, dest)
                self.statusBar().showMessage(f"File saved to {self.cafilepath}", 3000)
                self.isDirty = False
                return True
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save file to {self.cafilepath}:\n{e}")
                return False
        else:
            return self.saveFileAs()

    def saveFileAs(self):
        if not hasattr(self, 'cafile') or not self.cafile:
            QMessageBox.warning(self, "Save As Error", "No file is open to save.")
            return False

        if hasattr(self, 'newfile_name') and self.newfile_name:
            docs = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
            if not docs:
                docs = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
            initial_path = os.path.join(docs, f"{self.newfile_name}.ca")
        else:
            initial_path = self.cafilepath if hasattr(self, 'cafilepath') and self.cafilepath else QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
            if not initial_path:
                initial_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

        path, _ = QFileDialog.getSaveFileName(self, "Save As...", initial_path, "Core Animation Bundle (*.ca)")
        
        if not path:
            return False # User cancelled
            
        if not path.lower().endswith('.ca'):
            path += '.ca'
            
        try:
            dest, name = os.path.split(path)
            self.cafile.write_file(name, dest)
            self.cafilepath = path # Update current file path
            self.ui.filename.setText(path) # Update filename label
            self.setWindowTitle(f"OpenPoster - {name}") # Update window title
            self.statusBar().showMessage(f"File saved as {path}", 3000)
            self.isDirty = False
            return True
        except Exception as e:
            QMessageBox.critical(self, "Save As Error", f"Could not save file to {path}:\n{e}")
            return False

    def exportFile(self):
        if not hasattr(self, 'cafile') or not self.cafile:
            QMessageBox.warning(self, "No File Open", "Please open a file before exporting.")
            return

        dialog = ExportOptionsDialog(self, self.config_manager) # Pass config_manager
        if dialog.exec():
            choice = dialog.choice
            if choice == "copy":
                if self.isDirty:
                    self.saveFile()
                
                if hasattr(self, 'ca_files_in_tendies') and len(self.ca_files_in_tendies) > 1:
                    folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Export .ca Files")
                    if not folder_path:
                        return
                    
                    for ca_file_path in self.ca_files_in_tendies:
                        try:
                            basename = os.path.basename(ca_file_path)
                            dest_path = os.path.join(folder_path, basename)
                            shutil.copytree(ca_file_path, dest_path, dirs_exist_ok=True)
                        except Exception as e:
                            QMessageBox.warning(self, "Export Warning", f"Failed to export {basename}: {e}")
                    
                    self.statusBar().showMessage(f"Exported .ca files to {folder_path}", 3000)
                else:
                    path, _ = QFileDialog.getSaveFileName(self, "Save As", self.cafilepath, "Core Animation Bundle (*.ca)")
                    if not path:
                        return
                    dest, name = os.path.split(path)
                    self.cafile.write_file(name, dest)
                    self.cafilepath = path
                    self.ui.filename.setText(path)
                    self.statusBar().showMessage(f"Saved As {path}", 3000)
                    self.isDirty = False
                
            elif choice == 'tendies':
                if self.isDirty:
                    self.saveFile()
                
                path, _ = QFileDialog.getSaveFileName(self, "Save as .tendies", self.cafilepath, "Tendies Bundle (*.tendies)")
                if not path:
                    return
                
                if not path.lower().endswith('.tendies'):
                    path += '.tendies'

                temp_dir = tempfile.mkdtemp()
                try:
                    if hasattr(self, 'ca_files_in_tendies') and len(self.ca_files_in_tendies) > 1:
                        for ca_file_path in self.ca_files_in_tendies:
                            self._create_tendies_structure(temp_dir, ca_file_path)
                    else:
                        self._create_tendies_structure(temp_dir, self.cafilepath)

                    shutil.make_archive(path[:-len('.tendies')], 'zip', root_dir=temp_dir)
                    
                    os.rename(path[:-len('.tendies')] + '.zip', path)

                except Exception as e:
                     QMessageBox.critical(self, "Export Error", f"Failed to create .tendies file: {e}")
                finally:
                    shutil.rmtree(temp_dir)

            elif choice == 'nugget':
                if self.isDirty:
                    self.saveFile()
                
                temp_dir = tempfile.mkdtemp()
                try:
                    if hasattr(self, 'tendies_temp_dir') and self.tendies_temp_dir:
                        for ca_path in self.ca_files_in_tendies:
                            self._create_tendies_structure(temp_dir, ca_path)
                    else:
                        self._create_tendies_structure(temp_dir, self.cafilepath)

                    export_dir = os.path.join(self.config_manager.config_dir, 'nugget-exports')
                    os.makedirs(export_dir, exist_ok=True)
                    base_name = os.path.splitext(os.path.basename(self.cafilepath))[0]
                    archive_base = os.path.join(export_dir, base_name)
                    zip_file = shutil.make_archive(archive_base, 'zip', root_dir=temp_dir)
                    tendies_path = archive_base + '.tendies'
                    os.rename(zip_file, tendies_path)
                    target = tendies_path

                    nugget_exec = self.config_manager.get_nugget_exec_path()
                    if not nugget_exec:
                        QMessageBox.information(self, "Nugget Export", "Nugget executable path is not configured in settings.")
                        return
                    if not os.path.exists(nugget_exec):
                        QMessageBox.warning(self, "Nugget Error", f"Nugget executable not found at: {nugget_exec}")
                        return

                    if nugget_exec.lower().endswith(".py"):
                        program = sys.executable
                        args = [nugget_exec, target]
                    elif nugget_exec.endswith(".app") and self.isMacOS:
                        program = "open"
                        args = [nugget_exec, "--args", target]
                    else:
                        program = nugget_exec
                        args = [target]

                    print("Running Nugget:", program, *args)
                    self._run_nugget_export(program, args)
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", f"Failed during Nugget export preparation: {e}")
                finally:
                    shutil.rmtree(temp_dir)
    
    def _create_tendies_structure(self, base_dir, ca_source_path):
        try:
            root = sys._MEIPASS if hasattr(sys, '_MEIPASS') else (os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd())
            descriptors_src = os.path.join(root, "descriptors")
            if not os.path.exists(descriptors_src):
                raise FileNotFoundError("descriptors template directory not found")
                
            descriptors_dest = os.path.join(base_dir, "descriptors")
            shutil.copytree(descriptors_src, descriptors_dest, dirs_exist_ok=True)

            eid = next((d for d in os.listdir(descriptors_dest) if os.path.isdir(os.path.join(descriptors_dest, d)) and not d.startswith('.')), None)
            if not eid:
                raise FileNotFoundError("Could not find EID directory within descriptors template")

            contents_dir = os.path.join(descriptors_dest, eid, "versions", "0", "contents")
            wallpaper_dir = os.path.join(contents_dir, "OpenPoster.wallpaper")
            os.makedirs(wallpaper_dir, exist_ok=True)

            if not os.path.exists(ca_source_path):
                 raise FileNotFoundError(f".ca source path does not exist: {ca_source_path}")
            ca_basename = os.path.basename(ca_source_path)
            ca_dest_dir = os.path.join(wallpaper_dir, ca_basename)
            shutil.copytree(ca_source_path, ca_dest_dir)
            
        except Exception as e:
            print(f"Error creating tendies structure in {base_dir}: {e}")
            raise

    def _clear_nugget_exports_cache(self):
        export_dir = os.path.join(self.config_manager.config_dir, 'nugget-exports')
        if os.path.exists(export_dir):
            shutil.rmtree(export_dir)
        os.makedirs(export_dir, exist_ok=True)

    def open_project(self, path):
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Open Error", f"The file or folder does not exist: {path}")
            return
        self.ui.treeWidget.clear()
        self.ui.statesTreeWidget.clear()
        self.cafilepath = path
        self.setWindowTitle(f"OpenPoster - {os.path.basename(self.cafilepath)}")
        self.ui.filename.setText(self.cafilepath)
        self.ui.filename.setStyleSheet("font-style: normal; color: palette(text); border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px;")
        self.showFullPath = True
        self.cafile = CAFile(self.cafilepath)
        self.cachedImages = {}
        self.missing_assets = set()
        rootItem = QTreeWidgetItem([self.cafile.rootlayer.name, "Root", self.cafile.rootlayer.id, ""])
        self.ui.treeWidget.addTopLevelItem(rootItem)
        if len(self.cafile.rootlayer._sublayerorder) > 0:
            self.treeWidgetChildren(rootItem, self.cafile.rootlayer)
        self.populateStatesTreeWidget()
        if hasattr(self._applyAnimation, 'animations'):
            self._applyAnimation.animations.clear()
        self.animations = []
        self.scene.clear()
        self.currentZoom = 1.0
        self.ui.graphicsView.resetTransform()
        self.renderPreview(self.cafile.rootlayer)
        if hasattr(self._applyAnimation, 'animations'):
            self.animations = list(self._applyAnimation.animations)
        self.fitPreviewToView()
        self.isDirty = False

    def _run_nugget_export(self, program, args):
        process = QProcess(self)
        process.setProgram(program)
        process.setArguments(args)
        process.finished.connect(self._on_nugget_finished)
        process.errorOccurred.connect(lambda error: QMessageBox.critical(self, "Nugget Error", f"Nugget execution error: {error}"))
        process.start()

    def _on_nugget_finished(self, exitCode, exitStatus):
        process = self.sender()
        stdout = bytes(process.readAllStandardOutput()).decode()
        stderr = bytes(process.readAllStandardError()).decode()
        if exitCode == 0:
            self.statusBar().showMessage("Exported to Nugget successfully", 3000)
            self.isDirty = False
        else:
            error_message = f"Nugget execution failed (exit code {exitCode}).\n"
            if stdout:
                error_message += f"stdout:\n{stdout}\n"
            if stderr:
                error_message += f"stderr:\n{stderr}"
            print(error_message)
            QMessageBox.critical(self, "Nugget Error", f"Nugget execution failed. Check console for details.\nError: {stderr or stdout or 'Unknown error'}")

    def openDiscord(self):
        webbrowser.open("https://discord.gg/t3abQJjHm6")

    # Other file-related methods... 