"""
Image Inserter for Vocabulary Cards - Anki Add-on
Automatically inserts relevant images into vocabulary cards
"""
from aqt import mw, gui_hooks
from aqt.qt import QAction
from aqt.utils import showInfo
import traceback

# Add-on metadata
__version__ = "1.0.0"


def show_image_inserter_dialog():
    """Show the main Image Inserter dialog"""
    try:
        # Try importing dependencies first
        try:
            import requests
        except ImportError:
            showInfo("Error: 'requests' module not found.\n\nPlease install: pip install requests")
            return

        try:
            from PIL import Image
        except ImportError:
            showInfo("Error: 'Pillow' module not found.\n\nPlease install: pip install Pillow")
            return

        from .ui_dialog import ImageInserterDialog

        # Load config
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            # Load from config.json
            import os
            import json
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
            except:
                config = {}

        # Create and show dialog
        dialog = ImageInserterDialog(mw, config)
        dialog.exec()

    except Exception as e:
        error_msg = f"Error opening Image Inserter:\n{str(e)}\n\n{traceback.format_exc()}"
        showInfo(error_msg)
        print(error_msg)


def setup_menu():
    """Add menu item to Anki's Tools menu"""
    try:
        # Create action
        action = QAction("Image Inserter for Vocabulary", mw)
        action.triggered.connect(show_image_inserter_dialog)

        # Add to Tools menu
        mw.form.menuTools.addAction(action)
        print("Image Inserter menu added successfully")
    except Exception as e:
        print(f"Error setting up menu: {e}")
        traceback.print_exc()


# Initialize add-on when Anki is ready
gui_hooks.main_window_did_init.append(setup_menu)
print("Image Inserter add-on loaded")
