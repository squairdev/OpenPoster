from PySide6.QtGui import QImage, QPixmap
import os

class Assets:
    def __init__(self):
        # overide later
        self.cafilepath = ""
        self.cachedImages = ""

    def loadImage(self, src_path):
        if not src_path:
            return None
        
        if src_path in self.cachedImages:
            return self.cachedImages[src_path]
        
        # from formating
        self.cafilepath = self.cafilepath
        asset_path = self.findAssetPath(src_path)

        if not asset_path or not os.path.exists(asset_path):
            print(f"Could not find asset: {src_path}")
            
            if not hasattr(self, 'missing_assets'):
                self.missing_assets = set()
            self.missing_assets.add(src_path)
            
            return None
        
        try:
            img = QImage(asset_path)
            if img.isNull():
                print(f"Failed to load image: {asset_path}")
                return None
            
            pixmap = QPixmap.fromImage(img)
            self.cachedImages[src_path] = pixmap
            print(f"Loaded image successfully: {asset_path}")
            return pixmap
        except Exception as e:
            print(f"Error loading image {asset_path}: {e}")
            return None

    def findAssetPath(self, src_path):
        if not src_path:
            return None
        
        try:
            import urllib.parse
            decoded_path = urllib.parse.unquote(src_path)
            if decoded_path != src_path:
                src_path = decoded_path
        except:
            pass
        
        if os.path.isabs(src_path) and os.path.exists(src_path):
            return src_path
        
        base_path = os.path.join(self.cafilepath, src_path)
        if os.path.exists(base_path):
            return base_path
        
        assets_path = os.path.join(self.cafilepath, "assets", os.path.basename(src_path))
        if os.path.exists(assets_path):
            return assets_path
        
        direct_path = os.path.join(self.cafilepath, os.path.basename(src_path))
        if os.path.exists(direct_path):
            return direct_path
        
        parent_path = os.path.join(os.path.dirname(self.cafilepath), os.path.basename(src_path))
        if os.path.exists(parent_path):
            return parent_path
        
        parent_assets_path = os.path.join(os.path.dirname(self.cafilepath), "assets", os.path.basename(src_path))
        if os.path.exists(parent_assets_path):
            return parent_assets_path
        
        filename = os.path.basename(src_path)
        assets_dir = os.path.join(self.cafilepath, "assets")
        if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
            for file in os.listdir(assets_dir):
                if file.lower() == filename.lower():
                    return os.path.join(assets_dir, file)
                
        parent_assets_dir = os.path.join(os.path.dirname(self.cafilepath), "assets")
        if os.path.exists(parent_assets_dir) and os.path.isdir(parent_assets_dir):
            for file in os.listdir(parent_assets_dir):
                if file.lower() == filename.lower():
                    return os.path.join(parent_assets_dir, file)
                
        if os.path.isdir(self.cafilepath):
            for file in os.listdir(self.cafilepath):
                if os.path.isfile(os.path.join(self.cafilepath, file)) and file.lower() == filename.lower():
                    return os.path.join(self.cafilepath, file)
                
        parent_dir = os.path.dirname(self.cafilepath)
        if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
            for file in os.listdir(parent_dir):
                if os.path.isfile(os.path.join(parent_dir, file)) and file.lower() == filename.lower():
                    return os.path.join(parent_dir, file)
        
        return self.findAssetRecursive(self.cafilepath, filename, max_depth=3)
    
    def findAssetRecursive(self, directory, filename, max_depth=3, current_depth=0):
        if current_depth > max_depth or not os.path.exists(directory) or not os.path.isdir(directory):
            return None
        
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            
            if os.path.isfile(full_path) and file.lower() == filename.lower():
                return full_path
            
            if os.path.isdir(full_path):
                result = self.findAssetRecursive(full_path, filename, max_depth, current_depth + 1)
                if result:
                    return result
        
        return None